"""API FastAPI do DevMind. Execute com uvicorn api:app."""

import os
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, StringConstraints

from config import Question, TopK
from guide import guide_as_list, read_guide_document
from learning_api import get_store, router as learning_router
from local_access import local_demo_access
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
    allow_headers=["Content-Type"],
)
app.include_router(learning_router)

Scope = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class AskRequest(BaseModel):
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


@app.post("/ask", response_model=AskResponse, dependencies=[Depends(local_demo_access)])
def ask(request: AskRequest):
    get_store().charge_chat()
    try:
        return answer_question(
            request.question, top_k=request.top_k, module=request.module, topic=request.topic, source=request.source,
        )
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status, detail=str(exc)) from None
