"""Native Gemini contracts, safety, usage and local schema/citation validation."""

import json
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import httpx
import pytest

import learning_service
import llm
import rag
from chunking import build_records
from config import settings
from learning_models import GenerateRequest, ReviewRequest
from learning_service import LearningService
from learning_store import LearningStore
from providers import ServiceError


def result(payload, **updates):
    return {"modelVersion": "gemini-fixture", "usageMetadata": {"promptTokenCount": 50, "candidatesTokenCount": 20, "totalTokenCount": 70},
            "candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": json.dumps(payload)}]}}], **updates}


@pytest.fixture
def gemini(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "gemini")
    monkeypatch.setattr(settings, "gemini_timeout", 37)
    monkeypatch.setenv("GEMINI_API_KEY", "fixture-secret")
    monkeypatch.setenv("PINECONE_API_KEY", "fixture")
    response = httpx.Response(200, json=result({"answer": "Use o staging.", "citations": ["S1"]}))
    post = Mock(return_value=response)
    monkeypatch.setattr(llm.httpx, "post", post)
    return post


def test_native_gemini_json_and_usage(gemini):
    trace = rag.RunTrace()
    output = llm.generate_json(rag.GroundedAnswer, "instruction", {"question": "Oi"}, trace, 1200)
    assert output.stopped and not output.refused
    options = gemini.call_args.kwargs
    assert options["timeout"] == 37
    assert options["headers"] == {"x-goog-api-key": "fixture-secret"}
    assert "fixture-secret" not in gemini.call_args.args[0]
    config = options["json"]["generationConfig"]
    assert config["responseMimeType"] == "application/json" and "responseJsonSchema" in config
    assert config["maxOutputTokens"] == 1200
    assert "messages" not in options["json"] and "store" not in options["json"]
    assert trace.llm_usage == {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70}
    assert trace.openai_usage == {} and trace.llm_provider == "gemini"


@pytest.mark.parametrize("status,expected", [(429, 429), (403, 503), (404, 503), (500, 502)])
def test_gemini_errors_are_sanitized(gemini, caplog, status, expected):
    gemini.return_value = httpx.Response(status, text="private content fixture-secret")
    with pytest.raises(ServiceError) as exc:
        llm.generate_json(rag.GroundedAnswer, "instruction", {}, rag.RunTrace(), 1200)
    assert exc.value.status == expected
    assert "private content" not in str(exc.value) + caplog.text
    assert "fixture-secret" not in str(exc.value) + caplog.text
    gemini.assert_called_once()


def test_gemini_timeout_and_truncated_response(gemini):
    gemini.side_effect = httpx.ReadTimeout("private", request=httpx.Request("POST", "https://example.com"))
    with pytest.raises(ServiceError) as exc:
        llm.generate_json(rag.GroundedAnswer, "instruction", {}, rag.RunTrace(), 1200)
    assert exc.value.status == 504
    gemini.side_effect = None
    gemini.return_value = httpx.Response(200, json=result({}, candidates=[{"finishReason": "MAX_TOKENS", "content": {"parts": [{"text": "{}"}]}}]))
    with pytest.raises(ServiceError):
        rag._generate("Oi", '[{"id":"S1","text":"text"}]', {"S1": object()})


def test_gemini_safety_abstention_and_foreign_citations(gemini):
    gemini.return_value = httpx.Response(200, json=result({}, promptFeedback={"blockReason": "SAFETY"}))
    assert rag._generate("Oi", "[]", {})["status"] == "insufficient_evidence"
    gemini.return_value = httpx.Response(200, json=result({"answer": "Inventado", "citations": ["S99"]}))
    with pytest.raises(ServiceError):
        rag._generate("Oi", "[]", {})


def test_gemini_full_rag_generation_and_recall(gemini, monkeypatch, tmp_path):
    from test_learning import CARD, EVALUATION
    record = next(r for r in build_records() if r.get("module") == "devmind" and r.get("topic") == "git" and "--staged" in r["chunk_text"])
    hit = SimpleNamespace(fields=record, score=0.95)
    monkeypatch.setattr(learning_service, "retrieve", lambda *a, **k: [hit])
    monkeypatch.setattr(rag, "retrieve", lambda *a, **k: [hit])
    answer = rag.answer_question("Como retirar do staging?")
    assert answer["sources"][0]["source"] == record["source"]
    gemini.return_value = httpx.Response(200, json=result({"cards": [CARD]}))
    service = LearningService(LearningStore(tmp_path / "gemini.sqlite3", user_id=str(uuid4())))
    deck = service.generate(GenerateRequest(request_id=uuid4(), module="devmind", topic="git", count=1))
    gemini.return_value = httpx.Response(200, json=result(EVALUATION))
    review = service.review(deck["cards"][0]["id"], ReviewRequest(request_id=uuid4(), answer="Preservar edições com restore --staged"))
    assert review["grade"] == "correct" and review["schedule"]["reviews"] == 1
    rated = service.store.rate(review["review_id"], "easy")
    assert rated["schedule"]["interval_days"] == 3
    assert service.store.progress()["attempts"] == 1
