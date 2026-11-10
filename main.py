"""Inicializa o índice serverless do DevMind com embeddings integrados."""

from config import settings
from providers import ServiceError, pinecone_client, provider_errors


def main() -> int:
    try:
        with provider_errors("Pinecone"):
            pc = pinecone_client()
            if not pc.has_index(settings.index_name):
                pc.create_index_for_model(
                    name=settings.index_name,
                    cloud="aws",
                    region="us-east-1",
                    embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}},
                    timeout=120,
                )
    except ServiceError as exc:
        print(exc)
        return 1
    print(f"Índice '{settings.index_name}' disponível. Use ingest.py para carregar os documentos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
