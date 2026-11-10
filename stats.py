"""Auditoria de ingestão: estatísticas da knowledge base.

Módulo puro (sem rede): reutiliza `chunking.py` para inspecionar quantos
arquivos há, quais falharam/estão vazios/duplicados, e como ficaram
distribuídos os chunks gerados. Pensado para ser usado desde `ingest.py`
(antes de subir nada ao Pinecone) e desde o endpoint `GET /stats` da API.
"""

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from chunking import KNOWLEDGE_DIR, chunk_markdown, document_records, infer_module_topic, iter_markdown_files, read_markdown


@dataclass
class DocumentIssue:
    path: str
    reason: str


@dataclass
class KnowledgeBaseStats:
    documents_discovered: int = 0
    documents_indexed: int = 0
    failed: list[DocumentIssue] = field(default_factory=list)
    empty: list[DocumentIssue] = field(default_factory=list)
    duplicates: list[tuple[str, str]] = field(default_factory=list)  # (arquivo, duplicado_de)

    chunks_created: int = 0
    chunks_per_document: dict[str, int] = field(default_factory=dict)
    chunk_lengths: list[int] = field(default_factory=list)

    @property
    def avg_chunks_per_document(self) -> float:
        if not self.chunks_per_document:
            return 0.0
        return self.chunks_created / len(self.chunks_per_document)

    @property
    def min_chunk_length(self) -> int:
        return min(self.chunk_lengths) if self.chunk_lengths else 0

    @property
    def max_chunk_length(self) -> int:
        return max(self.chunk_lengths) if self.chunk_lengths else 0

    @property
    def avg_chunk_length(self) -> float:
        if not self.chunk_lengths:
            return 0.0
        return sum(self.chunk_lengths) / len(self.chunk_lengths)

    def as_dict(self) -> dict:
        return {
            "documents_discovered": self.documents_discovered,
            "documents_indexed": self.documents_indexed,
            "failed": len(self.failed),
            "empty": len(self.empty),
            "duplicates": len(self.duplicates),
            "chunks_created": self.chunks_created,
            "avg_chunks_per_document": round(self.avg_chunks_per_document, 1),
            "min_chunk_length": self.min_chunk_length,
            "max_chunk_length": self.max_chunk_length,
            "avg_chunk_length": round(self.avg_chunk_length, 1),
        }


def compute_stats(root: Path = KNOWLEDGE_DIR) -> KnowledgeBaseStats:
    return scan_corpus(root)[0]


def scan_corpus(
    root: Path, module: str | None = None, *, collect_records: bool = False,
) -> tuple[KnowledgeBaseStats, list[dict]]:
    """Valida e fragmenta o corpus uma vez para o relatório e o upsert."""
    stats = KnowledgeBaseStats()
    records = []
    seen_hashes: dict[str, str] = {}  # hash de conteúdo normalizado -> primeiro arquivo com esse hash

    files = [p for p in iter_markdown_files(root) if module is None or infer_module_topic(p, root)[0] == module]
    stats.documents_discovered = len(files)

    for path in files:
        rel = str(path.relative_to(root))
        try:
            text = read_markdown(path)
        except (OSError, UnicodeError, ValueError) as exc:
            reason = str(exc) if type(exc) is ValueError else type(exc).__name__
            stats.failed.append(DocumentIssue(rel, reason))
            continue

        if not text.strip():
            stats.empty.append(DocumentIssue(rel, "arquivo vazio ou só whitespace"))
            continue

        normalized = " ".join(text.split()).lower()
        content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        if content_hash in seen_hashes:
            stats.duplicates.append((rel, seen_hashes[content_hash]))
        else:
            seen_hashes[content_hash] = rel

        chunks = chunk_markdown(text)
        stats.documents_indexed += 1
        stats.chunks_per_document[rel] = len(chunks)
        stats.chunks_created += len(chunks)
        stats.chunk_lengths.extend(len(c["chunk_text"]) for c in chunks)
        if collect_records:
            records.extend(document_records(path, root, chunks))

    return stats, records


def format_report(stats: KnowledgeBaseStats) -> str:
    """Formata as estatísticas como o relatório legível pedido na Fase 2."""
    lines = [
        "Knowledge Base Statistics",
        "",
        f"Documents discovered: {stats.documents_discovered}",
        f"Valid documents: {stats.documents_indexed}",
        f"Failed: {len(stats.failed)}",
        f"Empty: {len(stats.empty)}",
        f"Potential duplicates: {len(stats.duplicates)}",
        "",
        f"Chunks created: {stats.chunks_created}",
        f"Average chunks/document: {stats.avg_chunks_per_document:.1f}",
        "",
        f"Average chunk length: {stats.avg_chunk_length:.0f} chars",
        f"Min chunk length: {stats.min_chunk_length} chars",
        f"Max chunk length: {stats.max_chunk_length} chars",
    ]
    if stats.failed:
        lines += ["", "Failed documents:"] + [f"  - {i.path}: {i.reason}" for i in stats.failed]
    if stats.empty:
        lines += ["", "Empty documents:"] + [f"  - {i.path}" for i in stats.empty]
    if stats.duplicates:
        lines += ["", "Potential duplicates:"] + [f"  - {a} ~= {b}" for a, b in stats.duplicates]
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_report(compute_stats()))
