"""Testes das funções puras de rag.py (não requerem Pinecone/OpenAI:
rag.py conecta de forma preguiçosa, então apenas importar o módulo e usar
seus helpers de pós-processamento não dispara nenhuma chamada de rede)."""

from types import SimpleNamespace

from rag import dedupe_sources, format_debug_hits


def _hit(source, chunk_id, score, section="General", text="texto"):
    return SimpleNamespace(
        score=score,
        fields={"source": source, "chunk_id": chunk_id, "section": section, "chunk_text": text},
    )


def test_dedupe_sources_collapses_same_source_keeping_best_score():
    hits = [
        _hit("a.md", 1, 0.91),
        _hit("a.md", 2, 0.85),
        _hit("b.md", 0, 0.80),
    ]
    result = dedupe_sources(hits)
    by_source = {r["source"]: r for r in result}
    assert set(by_source) == {"a.md", "b.md"}
    assert by_source["a.md"]["score"] == 0.91
    assert by_source["a.md"]["chunk_id"] == 1


def test_dedupe_sources_empty_input():
    assert dedupe_sources([]) == []


def test_format_debug_hits_includes_score_source_and_chunk_id():
    hits = [_hit("dependency-injection.md", 4, 0.89, section="DI")]
    output = format_debug_hits(hits)
    assert "Score: 0.8900" in output
    assert "Source: dependency-injection.md" in output
    assert "Chunk: 4" in output


def test_format_debug_hits_handles_no_hits():
    assert "No relevant" in format_debug_hits([])
