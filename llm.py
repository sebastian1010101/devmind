"""Provider-specific structured generation, with a small normalized result."""

import json
import logging
from dataclasses import dataclass

import httpx

from config import settings
from providers import ServiceError, openai_client, provider_errors, require_key

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Generation:
    content: str | None
    stopped: bool
    refused: bool


def require_llm_key():
    return require_key("GEMINI_API_KEY" if settings.llm_provider == "gemini" else "OPENAI_API_KEY")


def generate_json(schema, prompt, payload, trace, max_tokens, *, openai_factory=openai_client, schema_name=None):
    trace.llm_provider = settings.llm_provider
    if settings.llm_provider == "gemini":
        return gemini_generate(schema, prompt, payload, trace, max_tokens)
    options = {} if settings.temperature is None else {"temperature": settings.temperature}
    with provider_errors("OpenAI"):
        completion = openai_factory().chat.completions.create(
            model=settings.model,
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            response_format={"type": "json_schema", "json_schema": {
                "name": schema_name or schema.__name__, "strict": True, "schema": schema.model_json_schema(),
            }}, max_completion_tokens=max_tokens, store=False, **options,
        )
    usage = getattr(completion, "usage", None)
    for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, name, None)
        if isinstance(value, int):
            trace.openai_usage[name] = value
    cached = getattr(getattr(usage, "prompt_tokens_details", None), "cached_tokens", None)
    if isinstance(cached, int):
        trace.openai_usage["cached_tokens"] = cached
    trace.llm_usage = dict(trace.openai_usage)
    trace.generation_model = completion.model if isinstance(getattr(completion, "model", None), str) else settings.model
    try:
        choice = completion.choices[0]
        return Generation(choice.message.content, choice.finish_reason == "stop",
                          bool(choice.message.refusal) or choice.finish_reason == "content_filter")
    except (IndexError, AttributeError, TypeError):
        raise ServiceError("invalid_response", "A resposta recebida da IA não pôde ser validada.", 502) from None


def gemini_generate(schema, prompt, payload, trace, max_tokens):
    config = {"responseMimeType": "application/json", "responseJsonSchema": schema.model_json_schema(),
              "maxOutputTokens": max_tokens}
    if settings.temperature is not None:
        config["temperature"] = settings.temperature
    # Native generateContent preserves Google's safety/finish/usage contracts.
    try:
        response = httpx.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent",
            headers={"x-goog-api-key": require_key("GEMINI_API_KEY")},
            json={"systemInstruction": {"parts": [{"text": prompt}]},
                  "contents": [{"role": "user", "parts": [{"text": json.dumps(payload, ensure_ascii=False)}]}],
                  "generationConfig": config}, timeout=settings.gemini_timeout, follow_redirects=False,
        )
    except httpx.TimeoutException:
        raise ServiceError("provider_timeout", "Gemini demorou a responder. Tente novamente.", 504) from None
    except httpx.RequestError:
        raise ServiceError("provider_error", "Gemini está indisponível. Tente novamente.", 502) from None
    if response.status_code >= 400:
        logger.warning("llm_failure provider=gemini status=%s", response.status_code)
        if response.status_code == 429:
            raise ServiceError("provider_limit", "Gemini atingiu um limite de uso. Tente mais tarde.", 429)
        if response.status_code in {400, 401, 403, 404}:
            raise ServiceError("provider_config", "Verifique as credenciais, o modelo e a disponibilidade regional do Gemini.", 503)
        raise ServiceError("provider_error", "Gemini está indisponível. Tente novamente.", 502)
    try:
        data = response.json()
        usage = data.get("usageMetadata", {})
        for source, target in [("promptTokenCount", "prompt_tokens"), ("candidatesTokenCount", "completion_tokens"),
                               ("totalTokenCount", "total_tokens"), ("thoughtsTokenCount", "thinking_tokens"),
                               ("cachedContentTokenCount", "cached_tokens")]:
            if isinstance(usage.get(source), int):
                trace.llm_usage[target] = usage[source]
        trace.generation_model = data.get("modelVersion") or settings.gemini_model
        candidates = data.get("candidates", [])
        block_reason = data.get("promptFeedback", {}).get("blockReason")
        blocked = bool(block_reason and block_reason != "BLOCK_REASON_UNSPECIFIED")
        if blocked:
            return Generation(None, False, True)
        candidate = candidates[0]
        finish = candidate.get("finishReason")
        refused = finish in {"SAFETY", "RECITATION", "BLOCKLIST", "PROHIBITED_CONTENT", "SPII"}
        parts = candidate.get("content", {}).get("parts", [])
        content = "".join(part.get("text", "") for part in parts if not part.get("thought"))
        return Generation(content, finish == "STOP", refused)
    except (ValueError, KeyError, IndexError, TypeError, AttributeError):
        raise ServiceError("invalid_response", "A resposta recebida do Gemini não pôde ser validada.", 502) from None
