"""Avalia o pipeline compartilhado. Modo padrão: provedores simulados."""

import argparse
import hashlib
import json
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chunking import KNOWLEDGE_DIR, chunk_markdown, read_markdown  # noqa: E402
from config import settings  # noqa: E402
from providers import ServiceError, require_key  # noqa: E402
from rag import RunTrace, answer_question  # noqa: E402

QUESTIONS_PATH = Path(__file__).resolve().parent / "questions.json"
K_VALUES = (1, 3, 5)


def hit_at_k(expected_sources: list[str], retrieved_sources: list[str | None], k: int) -> bool:
    return any(source in retrieved_sources[:k] for source in expected_sources)


def attributed(citations: list[dict], context: list[dict]) -> bool:
    def identity(item):
        return item["source"], item["section"], item["chunk_id"]

    allowed = {identity(item) for item in context}
    return bool(citations) and all(identity(citation) in allowed for citation in citations)


def summarize_usage(rows: list[dict]) -> dict:
    totals = {}
    for provider, fields in {
        "pinecone": ("read_units", "embed_total_tokens"),
        "openai": ("prompt_tokens", "completion_tokens", "total_tokens", "cached_tokens"),
    }.items():
        totals[provider] = {}
        for name in fields:
            values = [row.get("usage", {}).get(provider, {}).get(name) for row in rows]
            measured = [value for value in values if isinstance(value, int)]
            totals[provider][name] = {"total": sum(measured) if measured else None, "samples": len(measured)}
    return totals


def measure(rows: list[dict]) -> dict:
    def rate(values):
        return {"passed": sum(values), "total": len(values), "rate": sum(values) / len(values) if values else None}

    succeeded = [row for row in rows if row["error"] is None]
    generated = [row for row in succeeded if row["status"] == "answered"]
    labeled_citations = [
        item["source"] in row["expected_sources"]
        for row in generated if row["expected_sources"] for item in row["sources"]
    ]
    retrieval_cases = [row for row in rows if row["expected_sources"] and row["retrieval_completed"]]
    latencies = {}
    for phase in ("retrieval", "generation", "total"):
        values = [row["latency_ms"][phase] for row in succeeded if row["latency_ms"][phase] is not None]
        latencies[phase] = {
            "median_ms": round(statistics.median(values), 2) if values else None,
            "samples": len(values),
        }
    return {
        "retrieval_hit_at_k": {str(k): rate([
            hit_at_k(row["expected_sources"], row["retrieved_sources"], k) for row in retrieval_cases
        ]) for k in K_VALUES},
        "abstention_accuracy": rate([
            (row["status"] == "answered") == row["should_answer"] for row in succeeded
        ]),
        "correct_rejection": rate([row["status"] == "insufficient_evidence" for row in succeeded if not row["should_answer"]]),
        "source_attribution": rate([attributed(row["sources"], row["context_sources"]) for row in generated]),
        "expected_source_cited": rate([
            any(item["source"] in row["expected_sources"] for item in row["sources"])
            for row in succeeded if row["expected_sources"]
        ]),
        "labeled_source_precision": rate(labeled_citations),
        "latency": latencies,
        "error_rate": rate([row["error"] is not None for row in rows]),
    }


def _run(question: dict, *, namespace: str | None = None) -> dict:
    trace = RunTrace()
    result = {}
    error = None
    try:
        result = answer_question(question["query"], trace=trace, retrieval_k=max(K_VALUES), namespace=namespace)
    except ServiceError as exc:
        error = exc.code
    return {
        **question,
        "status": result.get("status"),
        "answer": result.get("answer"),
        "sources": result.get("sources", []),
        "retrieval_completed": trace.retrieval_completed,
        "retrieved_sources": [hit.fields.get("source") for hit in trace.hits],
        "context_sources": trace.context_sources,
        "latency_ms": {
            "retrieval": trace.retrieval_ms, "generation": trace.generation_ms, "total": trace.total_ms,
        },
        "error": error,
        "usage": {"pinecone": trace.pinecone_usage, "openai": trace.openai_usage},
        "generation_model": trace.generation_model,
    }


def _mock_run(questions: list[dict]) -> list[dict]:
    """Fixtures rotuladas verificam o fluxo, sem estimar qualidade semântica."""
    index = Mock()
    model = Mock()
    distractor = SimpleNamespace(score=0.2, fields={
        "source": "fixture.md", "section": "Irrelevante", "chunk_id": 0, "chunk_text": "Trecho auxiliar.",
    })
    rows = []
    with (
        patch("rag.pinecone_index", return_value=index),
        patch("rag.openai_client", return_value=model),
        patch.dict(os.environ, {"PINECONE_API_KEY": "fixture", "OPENAI_API_KEY": "fixture"}),
    ):
        for q in questions:
            hits = [distractor]
            payload = {"answer": None, "citations": []}
            if q["expected_sources"]:
                source = q["expected_sources"][0]
                chunks = chunk_markdown(read_markdown(KNOWLEDGE_DIR / source))
                chunk_id, chunk = max(enumerate(chunks), key=lambda entry: len(entry[1]["chunk_text"]))
                hits.insert(0, SimpleNamespace(score=1.0, fields={**chunk, "source": source, "chunk_id": chunk_id}))
                payload = {"answer": "Resposta de teste do provedor simulado.", "citations": ["S1"]}
            elif q["type"] == "ambigua":
                hits = [SimpleNamespace(score=1.0, fields=distractor.fields)]
            index.search_records.return_value = SimpleNamespace(result=SimpleNamespace(hits=hits))
            model.chat.completions.create.return_value = SimpleNamespace(choices=[SimpleNamespace(
                finish_reason="stop", message=SimpleNamespace(refusal=None, content=json.dumps(payload)),
            )])
            rows.append(_run(q))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Autoriza consultas a Pinecone e geração na OpenAI.")
    parser.add_argument("--portfolio", action="store_true", help="Usa os 11 casos do corpus autoral.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--namespace", help="Namespace de avaliação, sem alterar a configuração local.")
    args = parser.parse_args()
    if args.namespace:
        # Use the same validation as the application's environment configuration.
        settings.__class__(namespace=args.namespace)

    dataset = QUESTIONS_PATH.read_bytes()
    questions = [q for q in json.loads(dataset) if not args.portfolio or q.get("portfolio")]
    if args.live:
        try:
            require_key("PINECONE_API_KEY")
            require_key("OPENAI_API_KEY")
        except ServiceError as exc:
            parser.error(str(exc))
        rows = []
        for question in questions:
            row = _run(question, namespace=args.namespace)
            rows.append(row)
            print(f"{row['id']:02}: {row['error'] or row['status']}", flush=True)
    else:
        rows = _mock_run(questions)

    mode = "live" if args.live else "mock"
    report = {
        "mode": mode,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_sha256": hashlib.sha256(dataset).hexdigest(),
        "subset": "portfolio" if args.portfolio else "all",
        "config": {**settings.model_dump(), "namespace": args.namespace or settings.namespace},
        "questions_evaluated": len(rows),
        "metrics": measure(rows),
        "usage": summarize_usage(rows),
        "per_question": rows,
    }
    default_name = "results-real-local.json" if args.live else "results-mock-local.json"
    output = args.output or QUESTIONS_PATH.with_name(default_name)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{mode}: {len(rows)} perguntas. Relatório salvo em {output}.")
    print(json.dumps(report["metrics"], indent=2))
    return int(any(row["error"] for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
