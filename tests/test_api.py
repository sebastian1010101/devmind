import json
from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient
import pytest

import api
import rag
from chunking import build_records
from ingest import upsert
from providers import ServiceError

client = TestClient(api.app)


def test_local_endpoints_do_not_need_provider_credentials(monkeypatch):
    monkeypatch.delenv("PINECONE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/stats").json()["documents_indexed"] > 0
    guide = client.get("/guide")
    assert guide.status_code == 200
    assert any(module["id"] == "devmind" for module in guide.json())
    response = client.post("/ask", json={"question": "Como funciona o Git?"})
    assert response.status_code == 503
    assert response.json() == {"detail": "Configure PINECONE_API_KEY no servidor."}


@pytest.mark.parametrize("payload", [
    {"question": "   "},
    {"question": "sensitive-input" * 100},
    {"question": "ok", "top_k": 0},
    {"question": "ok", "top_k": 21},
    {"question": "ok", "top_k": "3"},
])
def test_ask_rejects_invalid_payloads_without_echo(payload):
    response = client.post("/ask", json=payload)
    assert response.status_code == 422
    assert "sensitive-input" not in response.text


def test_ask_returns_sections_and_passes_the_backend_default(monkeypatch):
    def answer(question, *, top_k, module, topic, source):
        assert (question, top_k, module, topic, source) == ("Pergunta?", None, "devmind", "git", "DEVMIND/Git/a.md")
        return {"status": "answered", "answer": "Resposta", "sources": [
            {"source": source, "section": "Seção", "excerpt": "Evidência", "score": 0.8, "chunk_id": 1},
        ]}

    monkeypatch.setattr(api, "answer_question", answer)
    response = client.post("/ask", json={
        "question": " Pergunta? ", "module": "devmind", "topic": "git", "source": "DEVMIND/Git/a.md",
    })
    assert response.status_code == 200
    assert response.json()["sources"][0]["section"] == "Seção"


def test_ask_preserves_public_provider_status(monkeypatch):
    def timeout(*args, **kwargs):
        raise ServiceError("provider_timeout", "Pinecone demorou a responder.", 504)

    monkeypatch.setattr(api, "answer_question", timeout)
    response = client.post("/ask", json={"question": "Pergunta?"})
    assert response.status_code == 504
    assert response.json()["detail"] == "Pinecone demorou a responder."


def test_markdown_to_api_answer_with_mock_providers(tmp_path, monkeypatch):
    doc = tmp_path / "M" / "Git" / "guia.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("## Staging\nUse git restore --staged para retirar o arquivo do staging.", encoding="utf-8")
    stored = {}
    index, model = Mock(), Mock()

    def put(*, namespace, records):
        for record in records:
            stored[namespace, record["_id"]] = record

    def search(*, namespace, **_kwargs):
        hits = [SimpleNamespace(fields=record, score=0.95) for (ns, _id), record in stored.items() if ns == namespace]
        return SimpleNamespace(result=SimpleNamespace(hits=hits))

    def generate(**kwargs):
        evidence = json.loads(kwargs["messages"][-1]["content"])["evidence"]
        assert "git restore --staged" in evidence[0]["text"]
        message = SimpleNamespace(refusal=None, content=json.dumps({
            "answer": "Use git restore --staged.", "citations": [evidence[0]["id"]],
        }))
        return SimpleNamespace(choices=[SimpleNamespace(finish_reason="stop", message=message)])

    monkeypatch.setenv("PINECONE_API_KEY", "mock")
    monkeypatch.setenv("OPENAI_API_KEY", "mock")
    monkeypatch.setattr(rag, "pinecone_index", lambda: index)
    monkeypatch.setattr(rag, "openai_client", lambda: model)
    monkeypatch.setattr(rag, "settings", rag.settings.model_copy(update={
        "namespace": "fixture", "score_threshold": 0.40, "context_chars": 10_000,
    }))
    index.upsert_records.side_effect = put
    index.search_records.side_effect = search
    model.chat.completions.create.side_effect = generate
    records = build_records(tmp_path)
    upsert(index, records, "fixture")
    upsert(index, records, "fixture")
    assert len(stored) == 1

    response = client.post("/ask", json={"question": "Como retiro um arquivo do staging?"})
    assert response.status_code == 200
    assert response.json()["status"] == "answered"
    assert response.json()["sources"][0]["source"] == "M/Git/guia.md"
    assert response.json()["sources"][0]["section"] == "Staging"
