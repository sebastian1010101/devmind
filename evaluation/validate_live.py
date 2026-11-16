"""Validate real providers in a unique namespace using only the authorial corpus."""

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic, sleep
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from api import app  # noqa: E402
from chunking import KNOWLEDGE_DIR  # noqa: E402
from config import settings  # noqa: E402
from evaluation.evaluate import QUESTIONS_PATH, _run, measure, summarize_usage  # noqa: E402
from ingest import upsert  # noqa: E402
from providers import (  # noqa: E402
    ServiceError, openai_client, pinecone_client, pinecone_index, provider_errors, require_key,
)
from rag import SYSTEM_PROMPT, retrieve  # noqa: E402
from stats import scan_corpus  # noqa: E402


def wait_until(predicate, seconds: int) -> None:
    deadline = monotonic() + seconds
    while not predicate():
        if monotonic() >= deadline:
            raise ServiceError("consistency_timeout", "A visibilidade dos registros não convergiu.", 504)
        sleep(2)


def listed_ids(index, namespace: str) -> set[str]:
    with provider_errors("Pinecone"):
        return {item.id for page in index.list(namespace=namespace) for item in page.vectors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Autoriza consumo real dos dois provedores.")
    parser.add_argument("--output", type=Path, default=QUESTIONS_PATH.with_name("validation-real-local.json"))
    parser.add_argument("--wait-seconds", type=int, default=60)
    args = parser.parse_args()
    if not args.live or not 1 <= args.wait_seconds <= 180:
        parser.error("Use --live e um tempo de espera entre 1 e 180 segundos.")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    dataset = QUESTIONS_PATH.read_bytes()
    questions = [question for question in json.loads(dataset) if question.get("portfolio")]
    stats, records = scan_corpus(KNOWLEDGE_DIR, "devmind", collect_records=True)
    if stats.failed or not records or len(records) > 90:
        parser.error("O corpus autoral deve ser válido e caber em um lote de até 90 fragmentos.")

    namespace = f"devmind-validation-{uuid4().hex}"
    previous_namespace = settings.namespace
    # Every imported caller shares this Settings instance in this standalone process.
    settings.namespace = namespace
    report = {
        "mode": "live",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "git_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
        "code_sha256": {
            name: hashlib.sha256((KNOWLEDGE_DIR.parent / name).read_bytes()).hexdigest()
            for name in ("rag.py", "config.py", "providers.py", "ingest.py", "chunking.py", "api.py",
                         "evaluation/evaluate.py", "evaluation/validate_live.py")
        },
        "python": platform.python_version(),
        "config": settings.model_dump(),
        "dataset_sha256": hashlib.sha256(dataset).hexdigest(),
        "corpus_sha256": hashlib.sha256(json.dumps(records, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
        "documents": stats.documents_indexed,
        "chunks": len(records),
        "upsert_text_characters_per_pass": sum(len(record["chunk_text"]) for record in records),
        "checks": {},
        "system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "per_question": [],
        "error": None,
        "cleanup": {"attempted": False, "verified": False},
    }
    index = None
    writes_attempted = False
    ids = {record["_id"] for record in records}
    try:
        require_key("PINECONE_API_KEY")
        require_key("OPENAI_API_KEY")
        with provider_errors("Pinecone"):
            description = pinecone_client().describe_index(settings.index_name)
            fields = description.to_dict()["schema"]["fields"]
            text = fields.get("chunk_text", {})
            read_dimension = text.get("read_parameters", {}).get("dimension")
            write_dimension = text.get("write_parameters", {}).get("dimension")
            report["index"] = {
                "ready": description.status.ready,
                "text_field": text,
            }
            if not (
                description.status.ready and text.get("type") == "semantic_text"
                and text.get("model") == "llama-text-embed-v2"
                and read_dimension and read_dimension == write_dimension
            ):
                raise ServiceError("incompatible_index", "Verifique o esquema integrado do índice.", 503)
            index = pinecone_index()
        with provider_errors("OpenAI"):
            report["openai_model"] = openai_client().models.retrieve(settings.model).id
        report["checks"]["provider_authentication_and_index"] = True

        if listed_ids(index, namespace):
            raise ServiceError("namespace_not_empty", "O namespace de teste deve estar vazio.", 503)
        writes_attempted = True
        upsert(index, records, namespace)
        wait_until(lambda: listed_ids(index, namespace) == ids, args.wait_seconds)
        report["record_count_after_first_upsert"] = len(listed_ids(index, namespace))
        upsert(index, records, namespace)
        wait_until(lambda: listed_ids(index, namespace) == ids, args.wait_seconds)
        report["record_count_after_second_upsert"] = len(listed_ids(index, namespace))
        report["checks"]["idempotent_reingestion"] = True
        first = questions[0]
        wait_until(lambda: any(
            hit.fields.get("source") in first["expected_sources"]
            for hit in retrieve(first["query"], 5, namespace=namespace)
        ), args.wait_seconds)

        for question in questions:
            row = _run(question, namespace=namespace)
            report["per_question"].append(row)
            print(f"{row['id']}: {row['error'] or row['status']}", flush=True)
        rows = report["per_question"]
        report["metrics"] = measure(rows)
        report["usage"] = summarize_usage(rows)
        report["checks"]["evaluation_without_errors"] = all(row["error"] is None for row in rows)
        report["checks"]["answer_and_abstention_decisions"] = all(
            row["error"] is None and (row["status"] == "answered") == row["should_answer"] for row in rows
        )
        report["checks"]["structural_source_attribution"] = report["metrics"]["source_attribution"]["rate"] == 1
        report["checks"]["expected_sources_cited"] = report["metrics"]["expected_source_cited"]["rate"] == 1

        # Real ASGI request/response validation, with both provider clients untouched.
        report["api"] = []
        with TestClient(app) as client:
            for question in (questions[0], next(q for q in questions if q["type"] == "sin_respuesta")):
                payload = {"question": question["query"]}
                if question["expected_sources"]:
                    payload["source"] = question["expected_sources"][0]
                response = client.post("/ask", json=payload)
                body = response.json()
                report["api"].append({"request": payload, "http_status": response.status_code, "response": body})
                report["checks"][f"api_question_{question['id']}"] = (
                    response.status_code == 200
                    and body.get("status") == ("answered" if question["should_answer"] else "insufficient_evidence")
                    and (bool(body.get("sources")) == question["should_answer"])
                    and all(item["source"] == payload["source"] for item in body.get("sources", []))
                )
    except ServiceError as exc:
        report["error"] = {"code": exc.code, "http_status": exc.status}
    except Exception as exc:
        # External exceptions can contain headers or request bodies. Persist only the class.
        report["error"] = {"type": type(exc).__name__}
    finally:
        if writes_attempted:
            report["cleanup"]["attempted"] = True
            try:
                with provider_errors("Pinecone"):
                    index.delete(namespace=namespace, ids=sorted(ids))
                wait_until(lambda: not listed_ids(index, namespace), args.wait_seconds)
                report["cleanup"]["verified"] = True
            except ServiceError as exc:
                report["cleanup"]["error"] = exc.code
            except Exception as exc:
                report["cleanup"]["error_type"] = type(exc).__name__
        settings.namespace = previous_namespace
        report["passed"] = (
            report["error"] is None and bool(report["checks"]) and all(report["checks"].values())
            and report["cleanup"]["verified"]
        )
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "error": report["error"], "cleanup": report["cleanup"],
                      "report": str(args.output)}, ensure_ascii=False, indent=2))
    return int(not report["passed"])


if __name__ == "__main__":
    raise SystemExit(main())
