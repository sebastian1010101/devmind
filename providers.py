"""Conexões preguiçosas e erros públicos sem detalhes dos provedores."""

import logging
import os
from contextlib import contextmanager
from functools import lru_cache

from openai import APIError, APITimeoutError, OpenAI
from pinecone import Pinecone, PineconeError, PineconeTimeoutError, RetryConfig

from config import settings

logger = logging.getLogger(__name__)


class ServiceError(RuntimeError):
    def __init__(self, code: str, message: str, status: int):
        super().__init__(message)
        self.code = code
        self.status = status


def require_key(name: str) -> str:
    key = os.getenv(name, "").strip()
    if not key:
        raise ServiceError("missing_credentials", f"Configure {name} no servidor.", 503)
    return key


@lru_cache(maxsize=1)
def pinecone_client():
    return Pinecone(
        api_key=require_key("PINECONE_API_KEY"),
        timeout=settings.timeout,
        retry_config=RetryConfig(max_retries=1, max_wait=2),
    )


@lru_cache(maxsize=1)
def pinecone_index():
    return pinecone_client().index(name=settings.index_name)


@lru_cache(maxsize=1)
def openai_client():
    return OpenAI(api_key=require_key("OPENAI_API_KEY"), timeout=settings.timeout, max_retries=0)


@contextmanager
def provider_errors(provider: str):
    try:
        yield
    except (APIError, PineconeError) as exc:
        status = getattr(exc, "status_code", None)
        logger.warning("%s falhou (%s, status=%s)", provider, type(exc).__name__, status)
        if isinstance(exc, (APITimeoutError, PineconeTimeoutError)) or status in {408, 504}:
            raise ServiceError("provider_timeout", f"{provider} demorou a responder. Tente novamente.", 504) from None
        if status == 402 or getattr(exc, "code", None) == "insufficient_quota":
            raise ServiceError("provider_limit", f"Verifique o saldo e os limites de {provider}.", 503) from None
        if status == 429:
            raise ServiceError("provider_limit", f"{provider} atingiu um limite de uso. Tente mais tarde.", 429) from None
        if status in {400, 401, 403, 404}:
            raise ServiceError("provider_config", f"Verifique as credenciais e a configuração de {provider}.", 503) from None
        raise ServiceError("provider_error", f"{provider} está indisponível. Tente novamente.", 502) from None
