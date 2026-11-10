"""Configuração compartilhada, validada no início de cada processo."""

import os
from typing import Annotated

from dotenv import load_dotenv
from pydantic import BaseModel, Field, StringConstraints

load_dotenv()

MAX_QUESTION_CHARS = 1200
MAX_TOP_K = 20
TopK = Annotated[int, Field(ge=1, le=MAX_TOP_K, strict=True)]
Question = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=MAX_QUESTION_CHARS)]


class Settings(BaseModel):
    index_name: str = Field(default="kenzie-knowledge", pattern=r"^[a-z0-9][a-z0-9-]{0,44}$")
    namespace: str = Field(default="devmind", pattern=r"^[A-Za-z0-9_-]{1,80}$")
    top_k: int = Field(default=3, ge=1, le=MAX_TOP_K)
    score_threshold: float = Field(default=0.40, ge=0, le=1)
    model: str = Field(default="gpt-4o", pattern=r"^\S{1,150}$")
    temperature: float | None = Field(default=None, ge=0, le=2)
    context_chars: int = Field(default=10_000, ge=256, le=40_000)
    timeout: float = Field(default=15, ge=1, le=60)


_ENV = {
    "index_name": "PINECONE_INDEX_NAME",
    "namespace": "PINECONE_NAMESPACE",
    "top_k": "RAG_TOP_K",
    "score_threshold": "RAG_SCORE_THRESHOLD",
    "model": "RAG_MODEL",
    "temperature": "RAG_TEMPERATURE",
    "context_chars": "RAG_CONTEXT_CHARS",
    "timeout": "RAG_TIMEOUT_SECONDS",
}
settings = Settings(**{field: os.environ[name] for field, name in _ENV.items() if os.getenv(name)})
