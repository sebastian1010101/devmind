import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from openai import APITimeoutError
from httpx2 import Request
from pinecone import ApiError

import rag
from providers import ServiceError


def hit(source, score=0.9, section="Topic", text="Evidence", chunk_id=0):
    return SimpleNamespace(score=score, fields={
        "source": source, "section": section, "chunk_text": text, "chunk_id": chunk_id,
    })


def completion(content=None, *, finish_reason="stop", refusal=None):
    return SimpleNamespace(choices=[SimpleNamespace(
        finish_reason=finish_reason, message=SimpleNamespace(content=content, refusal=refusal),
    )])


@pytest.fixture
def clients(monkeypatch):
    monkeypatch.setenv("PINECONE_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    index, model = Mock(), Mock()
    index.search_records.return_value = SimpleNamespace(result=SimpleNamespace(hits=[]))
    monkeypatch.setattr(rag, "pinecone_index", lambda: index)
    monkeypatch.setattr(rag, "openai_client", lambda: model)
    monkeypatch.setattr(rag, "settings", rag.settings.model_copy(update={
        "top_k": 3, "score_threshold": 0.40, "context_chars": 10_000, "temperature": None,
    }))
    return index, model.chat.completions.create


def test_retrieval_filters_score_and_sets_scope(clients):
    index, _ = clients
    hits = [hit("a.md", 0.40), hit("b.md", 0.39)]
    index.search_records.return_value.result.hits = hits
    assert rag.retrieve("python", 2, 0.4, "python", "listas", source="a.md") == hits[:1]
    assert index.search_records.call_args.kwargs["filter"] == {
        "module": {"$eq": "python"}, "topic": {"$eq": "listas"}, "source": {"$eq": "a.md"},
    }


def test_context_counts_serialized_chars_and_preserves_text_as_data():
    content = 'text "\n{\\} ##!'
    hits = [hit("big.md", text="x" * 1000), hit("empty.md", text=" "), hit("a.md", text=content)]
    context, included = rag.build_context(hits, 70)
    assert len(context) <= 70
    assert json.loads(context) == [{"id": "S1", "text": content}]
    assert included == {"S1": hits[2]}


def test_no_evidence_abstains_without_generation(clients):
    index, generate = clients
    index.search_records.return_value.result.hits = [hit("weak.md", 0.2)]
    trace = rag.RunTrace()
    result = rag.answer_question("Como conto caracteres?", trace=trace)
    assert result == {"status": "insufficient_evidence", "answer": rag.NOT_FOUND_MESSAGE, "sources": []}
    generate.assert_not_called()
    assert trace.retrieved[0]["source"] == "weak.md"
    assert trace.retrieval_completed and trace.generation_ms is None


def test_model_can_abstain_with_relevant_hits(clients):
    index, generate = clients
    index.search_records.return_value.result.hits = [hit("a.md")]
    generate.return_value = completion('{"answer":null,"citations":[]}')
    assert rag.answer_question("Qual opção devo usar?")["status"] == "insufficient_evidence"
    generate.assert_called_once()


def test_only_cited_sections_are_returned_and_eval_rank_does_not_expand_context(clients):
    index, generate = clients
    index.search_records.return_value.result.hits = [
        hit("a.md", 0.92, "Introduction"),
        hit("a.md", 0.88, "Second section", "Second evidence", chunk_id=1),
        hit("b.md", 0.85),
        hit("d.md", 0.81),
    ]
    generate.return_value = completion('{"answer":"Com base na segunda seção.","citations":["S2","S2"]}')
    trace = rag.RunTrace()
    result = rag.answer_question("Pergunta técnica", trace=trace, retrieval_k=5)
    assert result["sources"] == [{
        "source": "a.md", "section": "Second section", "score": 0.88, "chunk_id": 1, "excerpt": "Second evidence",
    }]
    kwargs = generate.call_args.kwargs
    assert len(trace.retrieved) == 4 and len(trace.context_sources) == 3
    assert len(json.loads(kwargs["messages"][1]["content"])["evidence"]) == 3
    assert "temperature" not in kwargs and kwargs["store"] is False
    index.search_records.assert_called_once()


@pytest.mark.parametrize("content,finish_reason", [
    ("not json", "stop"),
    (None, "stop"),
    ('{"answer":"texto","citations":[]}', "stop"),
    ('{"answer":"texto","citations":["S99"]}', "stop"),
    ('{"answer":null,"citations":["S1"]}', "stop"),
    ('{"answer":"texto","citations":["S1"]}', "length"),
])
def test_reject_invalid_model_payloads(clients, content, finish_reason):
    index, generate = clients
    index.search_records.return_value.result.hits = [hit("a.md")]
    generate.return_value = completion(content, finish_reason=finish_reason)
    with pytest.raises(ServiceError) as exc:
        rag.answer_question("Pergunta")
    assert (exc.value.status, exc.value.code) == (502, "invalid_response")


def test_provider_refusal_is_safe_abstention(clients):
    index, generate = clients
    index.search_records.return_value.result.hits = [hit("a.md")]
    generate.return_value = completion(refusal="provider content")
    result = rag.answer_question("Pergunta")
    assert result["status"] == "insufficient_evidence" and not result["sources"]


def test_rate_limit_is_sanitized_and_skips_openai(clients, caplog):
    index, generate = clients
    index.search_records.side_effect = ApiError("secret response", 429)
    with pytest.raises(ServiceError) as exc:
        rag.answer_question("Pergunta")
    assert exc.value.status == 429 and "secret response" not in str(exc.value)
    assert "secret response" not in caplog.text
    generate.assert_not_called()


def test_generation_timeout_preserves_retrieval_trace(clients):
    index, generate = clients
    index.search_records.return_value.result.hits = [hit("a.md")]
    generate.side_effect = APITimeoutError(request=Request("POST", "https://example.invalid"))
    trace = rag.RunTrace()
    with pytest.raises(ServiceError) as exc:
        rag.answer_question("Pergunta", trace=trace)
    assert exc.value.status == 504
    assert trace.retrieval_completed and trace.generation_ms is not None


def test_missing_key_is_checked_before_network(clients, monkeypatch):
    index, generate = clients
    monkeypatch.delenv("OPENAI_API_KEY")
    with pytest.raises(ServiceError) as exc:
        rag.answer_question("Pergunta")
    assert exc.value.code == "missing_credentials"
    index.search_records.assert_not_called()
    generate.assert_not_called()
