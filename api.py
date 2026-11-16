"""API FastAPI do DevMind. Execute com uvicorn api:app."""

import os
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, StringConstraints

from config import Question, TopK
from guide import guide_as_list, read_guide_document
from learning_api import get_store, user_store, router as learning_router
from auth import router as auth_router
from security import RequestBodyLimit, ai_slot, client_ip, csrf_check, rate_limit
from providers import ServiceError
from rag import answer_question
from stats import compute_stats

app = FastAPI(title="DevMind", description="Assistente de estudos com fontes rastreáveis.", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGIN", "http://localhost:3035,http://127.0.0.1:3035").split(",")
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", "X-DevMind-CSRF"],
    allow_credentials=True,
)
app.add_middleware(RequestBodyLimit)
app.include_router(auth_router)
app.include_router(learning_router)


@app.middleware("http")
async def security_boundary(request: Request, call_next):
    path = request.url.path.removeprefix(request.scope.get("root_path", "")) or "/"
    try:
        csrf_check(request)
        if path.startswith(("/auth/", "/learning/")) or path == "/ask":
            # SQLite/driver work stays off the event loop.
            from starlette.concurrency import run_in_threadpool
            bucket = "auth" if request.method == "POST" and path.startswith("/auth/") else "api"
            limit = int(os.getenv("AUTH_REQUESTS_PER_MINUTE", "10")) if bucket == "auth" else int(os.getenv("IP_REQUESTS_PER_MINUTE", "120"))
            await run_in_threadpool(lambda: rate_limit(get_store(), f"ip:{bucket}:{client_ip(request)}", limit))
        response = await call_next(request)
    except HTTPException as exc:
        response = JSONResponse(status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers)
    except ServiceError as exc:
        response = JSONResponse(status_code=exc.status, content={"detail": str(exc), "code": exc.code})
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    if path.startswith(("/auth/", "/learning/")) or path == "/ask":
        response.headers["Cache-Control"] = "no-store"
    return response

Scope = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: Question
    top_k: TopK | None = None
    module: Scope | None = None
    topic: Scope | None = None
    source: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=512)] | None = None


class SourceItem(BaseModel):
    source: str
    section: str
    chunk_id: int | None = None
    score: float
    excerpt: str


class AskResponse(BaseModel):
    status: Literal["answered", "insufficient_evidence"]
    answer: str
    sources: list[SourceItem]


@app.exception_handler(RequestValidationError)
def invalid_request(_request: Request, _exc: RequestValidationError):
    # A resposta padrão inclui a entrada que falhou. Não devolvemos a pergunta ou o corpo.
    return JSONResponse(status_code=422, content={
        "detail": "Entrada inválida. Use textos de 1 a 1200 caracteres, IDs de solicitação UUID, 1 a 3 cartões e top-k de 1 a 20.",
    })


@app.exception_handler(ServiceError)
def service_error(_request: Request, exc: ServiceError):
    return JSONResponse(status_code=exc.status, content={"detail": str(exc), "code": exc.code})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def stats():
    return compute_stats().as_dict()


@app.get("/guide")
def guide():
    return guide_as_list()


@app.get("/guide/document")
def guide_document(source: str = "") -> dict[str, str]:
    markdown = read_guide_document(source)
    if markdown is None:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")
    return {"markdown": markdown}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, store=Depends(user_store)):
    from rag import RunTrace
    from time import perf_counter
    from uuid import uuid4

    trace, started, error = RunTrace(), perf_counter(), None
    with ai_slot(store):
        store.charge_chat()
        try:
            return answer_question(
                request.question, top_k=request.top_k, module=request.module, topic=request.topic, source=request.source,
                trace=trace,
            )
        except ServiceError as exc:
            error = exc.code
            raise
        finally:
            trace.total_ms = (perf_counter() - started) * 1000
            store.record_trace("chat", str(uuid4()), trace, error)
