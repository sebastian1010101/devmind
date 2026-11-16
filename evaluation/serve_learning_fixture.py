"""Servidor de QA local com provedores simulados e SQLite temporário.

Uso explícito: python evaluation/serve_learning_fixture.py --mock --port 8007
Não envia chamadas externas. As mensagens da IA identificam a simulação.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx  # noqa: E402
import uvicorn  # noqa: E402
from openai import APITimeoutError  # noqa: E402

from api import app  # noqa: E402
from chunking import KNOWLEDGE_DIR, chunk_markdown, document_records, read_markdown  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mock", action="store_true", required=True)
    parser.add_argument("--port", type=int, default=8007)
    args = parser.parse_args()
    path = next((KNOWLEDGE_DIR / "DEVMIND" / "Git").glob("*.md"))
    record = next(r for r in document_records(path, KNOWLEDGE_DIR, chunk_markdown(read_markdown(path))) if "--staged" in r["chunk_text"])
    failed = False

    def complete(**kwargs):
        nonlocal failed
        payload = json.loads(kwargs["messages"][-1]["content"])
        if "student_answer" in payload:
            if "timeout de teste" in payload["student_answer"] and not failed:
                failed = True
                raise APITimeoutError(request=httpx.Request("POST", "https://example.invalid"))
            result = {"grade": "correct", "present_concepts": ["Comando restore --staged", "Preservação das edições"],
                      "missing_concepts": [], "errors": [], "feedback": "Provedor simulado: sua resposta identifica o comando e a preservação das edições.", "citations": ["S1"]}
        else:
            result = {"cards": [{
                "question": question, "reference_answer": "Use git restore --staged README.md para retirar do staging sem descartar suas edições.",
                "explanation": "Provedor simulado: o comando modifica o índice e preserva o diretório de trabalho.",
                "concepts": ["Comando restore --staged", "Preservação das edições"], "difficulty": "medium", "citations": ["S1"],
            } for question in ["Como retirar README.md do staging preservando suas edições?",
                               "Qual é o efeito de restore --staged sobre o diretório de trabalho?",
                               "Qual comando permite inspecionar o estado dos arquivos no Git?"][:payload["count"]]]}
        return SimpleNamespace(model="fixture-model", usage=None, choices=[SimpleNamespace(
            finish_reason="stop", message=SimpleNamespace(refusal=None, content=json.dumps(result)))])

    model = Mock()
    model.chat.completions.create.side_effect = complete
    with tempfile.TemporaryDirectory(prefix="devmind-browser-") as directory:
        with patch.dict(os.environ, {"LEARNING_DB_PATH": str(Path(directory) / "study.sqlite3"),
                                   "PINECONE_API_KEY": "fixture", "OPENAI_API_KEY": "fixture",
                                   "FRONTEND_ORIGIN": "http://127.0.0.1:3036,http://localhost:3035,http://127.0.0.1:3035"}), \
                patch("learning_service.retrieve", return_value=[SimpleNamespace(fields=record, score=0.95)]), \
                patch("learning_service.openai_client", return_value=model):
            print("QA local: provedores simulados; nenhum consumo de IA.", flush=True)
            uvicorn.run(app, host="127.0.0.1", port=args.port, proxy_headers=False)


if __name__ == "__main__":
    main()
