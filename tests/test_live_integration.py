"""Opt-in live test. Uses only a synthetic document and a unique namespace."""

import os
from time import monotonic, sleep
from uuid import uuid4

import pytest

from chunking import build_records
from ingest import upsert
from providers import pinecone_index, provider_errors
from rag import answer_question

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("DEVMIND_ALLOW_LIVE") != "1"
        or not all(os.getenv(name) for name in ("PINECONE_API_KEY", "OPENAI_API_KEY")),
        reason="Requer DEVMIND_ALLOW_LIVE=1 e ambas as chaves.",
    ),
]


def test_markdown_to_live_answer(tmp_path):
    doc = tmp_path / "guia-farol.md"
    doc.write_text("# Guia do farol Neblina\nO código de validação do farol Neblina é LARANJA-274.", encoding="utf-8")
    records = build_records(tmp_path)
    ids = [record["_id"] for record in records]
    namespace = f"devmind-test-{uuid4().hex}"
    with provider_errors("Pinecone"):
        index = pinecone_index()
    try:
        upsert(index, records, namespace)
        deadline = monotonic() + 60
        with provider_errors("Pinecone"):
            while not index.fetch(ids=ids, namespace=namespace).vectors:
                if monotonic() >= deadline:
                    pytest.fail("O documento ainda não estava visível após 60 s.")
                sleep(2)
        result = answer_question("Qual é o código de validação do farol Neblina?", namespace=namespace)
        assert result["status"] == "answered"
        assert "LARANJA-274" in result["answer"]
        assert result["sources"][0]["source"] == doc.name
    finally:
        with provider_errors("Pinecone"):
            index.delete(ids=ids, namespace=namespace)
