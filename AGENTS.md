# Notas do projeto (devmind)

## Setup local

Não há `pip` no sistema; usar `uv` para criar o ambiente e instalar dependências:

```bash
uv venv .venv
uv pip install -p .venv/bin/python -r requirements.txt
```

Copiar `.env.example` para `.env` e preencher `PINECONE_API_KEY` / `OPENAI_API_KEY` antes de:
- `python ingest.py` (sem `--dry-run`)
- `python search.py`
- `python evaluation/evaluate.py`
- `uvicorn api:app --reload` (o endpoint `POST /ask` requer as duas chaves; `/health`, `/stats` e `/guide` não)

Frontend: `cd frontend && npm run dev` (porta 3035; espera a API em `NEXT_PUBLIC_API_URL`, default `http://localhost:8000`).

## Verificação

- Lógica pura (sem rede): `python -m pytest tests/ -v`
- Estatísticas de ingestão sem tocar o Pinecone: `python ingest.py --dry-run`
- Smoke test da API sem chaves (`/health`, `/stats`, `/guide`): funcionam; `/ask` requer `.env`.
- Frontend: `npx eslint .`, `npx tsc --noEmit`, `npm run build`.

## Arquitetura

`knowledge/<MODULE>/<TOPIC>/arquivo.md` → `chunking.py` (chunking + metadata) → `ingest.py` (sobe ao Pinecone,
que gera os embeddings via integrated inference com `llama-text-embed-v2`) → `rag.py` (retrieval +
grounding + geração com OpenAI `gpt-4o`, compartilhado por `search.py`, `api.py` e `evaluation/evaluate.py`).

`stats.py` e `guide.py` são puros (não requerem rede): `stats.py` se usa em `ingest.py` e `GET /stats`;
`guide.py` constrói a hierarquia Module → Section → Document para `GET /guide` (navegação GUIDE do
frontend) e para o filtro de scope de `/ask` (`rag.py::build_scope_filter`, metadata `module`/`topic`).
