"""Valida Markdown e atualiza o namespace configurado no Pinecone."""

import argparse
from pathlib import Path

from chunking import KNOWLEDGE_DIR, record_prefix
from config import settings
from providers import ServiceError, pinecone_index, provider_errors
from stats import format_report, scan_corpus

BATCH_SIZE = 90


def upsert(index, records: list[dict], namespace: str, *, prune: bool = False, module: str | None = None) -> None:
    stale_ids = []
    with provider_errors("Pinecone"):
        if prune:
            prefix = record_prefix(module)
            current = {record["_id"] for record in records}
            stale_ids = sorted({
                item.id
                for page in index.list(namespace=namespace, prefix=prefix)
                for item in page.vectors
                if item.id.startswith(prefix) and item.id not in current
            })

        for start in range(0, len(records), BATCH_SIZE):
            batch = records[start:start + BATCH_SIZE]
            index.upsert_records(namespace=namespace, records=batch)
            print(f"Upsert {start + 1}–{start + len(batch)}/{len(records)}")

        for start in range(0, len(stale_ids), 1000):
            index.delete(namespace=namespace, ids=stale_ids[start:start + 1000])
        if prune:
            print(f"Fragmentos obsoletos removidos: {len(stale_ids)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=KNOWLEDGE_DIR, help="Diretório que contém o corpus completo.")
    parser.add_argument("--module", type=str.lower, help="Limita o upsert e a limpeza a este módulo.")
    parser.add_argument("--dry-run", action="store_true", help="Valida e conta fragmentos sem acesso à rede.")
    parser.add_argument("--prune", action="store_true", help="Remove IDs DevMind ausentes do corpus após o upsert.")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("O diretório do corpus não existe.")

    stats, records = scan_corpus(args.root, args.module, collect_records=not args.dry_run)
    print(format_report(stats))
    if stats.failed or not stats.chunks_created:
        print("Ingestão cancelada. Corrija os arquivos inválidos ou use um corpus com conteúdo.")
        return 1
    if args.dry_run:
        print("\nDry-run: nada foi enviado ao Pinecone.")
        return 0

    try:
        with provider_errors("Pinecone"):
            index = pinecone_index()
        upsert(index, records, settings.namespace, prune=args.prune, module=args.module)
    except ServiceError as exc:
        print(f"Ingestão interrompida. {exc} Execute o mesmo comando para retomar.")
        return 1
    print(f"Ingestão concluída: {stats.documents_indexed} documentos, {len(records)} fragmentos em {settings.namespace}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
