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

import auth
from config import settings
import jwt
from cryptography.hazmat.primitives.asymmetric import ec
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException
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
        elif "question" in payload:
            result = {"answer": "Provedor simulado: use git restore --staged README.md e preserve as edições locais.", "citations": ["S1"]}
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

    signing_key = ec.generate_private_key(ec.SECP256R1())
    accounts = {}

    def session(user):
        now = int(datetime.now(timezone.utc).timestamp())
        token = jwt.encode({"sub": user["id"], "email": user["email"], "iss": "https://fixture.supabase.co/auth/v1",
                            "aud": "authenticated", "role": "authenticated", "iat": now, "exp": now + 600},
                           signing_key, algorithm="ES256", headers={"kid": "fixture-key"})
        return {"access_token": token, "refresh_token": user["id"], "expires_in": 600,
                "user": {**user, "email_confirmed_at": "2026-11-16"}}

    def mock_auth(method, endpoint, *, payload=None, token=None):
        payload = payload or {}
        email = payload.get("email", "")
        if endpoint == "signup":
            accounts.setdefault(email, {"id": str(uuid4()), "email": email, "verified": False})
            return {}
        if endpoint == "verify":
            user = accounts.get(email)
            if not user or payload.get("token") != "123456":
                raise HTTPException(400, "Código de teste inválido.")
            user["verified"] = True
            return session(user)
        if endpoint == "token?grant_type=password":
            user = accounts.get(email)
            if not user or not user["verified"] or payload.get("password") != "test-password-1234":
                raise HTTPException(400, "Confira os dados e a confirmação de email.")
            return session(user)
        if endpoint == "token?grant_type=refresh_token":
            user = next((item for item in accounts.values() if item["id"] == payload.get("refresh_token")), None)
            if not user:
                raise HTTPException(401, "Sessão expirada.")
            return session(user)
        return {}

    model = Mock()
    model.chat.completions.create.side_effect = complete
    with tempfile.TemporaryDirectory(prefix="devmind-browser-") as directory:
        with patch.dict(os.environ, {"LEARNING_DB_PATH": str(Path(directory) / "study.sqlite3"),
                                   "PINECONE_API_KEY": "fixture", "OPENAI_API_KEY": "fixture", "DATABASE_URL": "",
                                   "SUPABASE_URL": "https://fixture.supabase.co", "SUPABASE_PUBLISHABLE_KEY": "fixture",
                                   "AUTH_REQUESTS_PER_MINUTE": "1000", "USER_REQUESTS_PER_MINUTE": "1000",
                                   "FRONTEND_ORIGIN": "http://127.0.0.1:3036,http://localhost:3035,http://127.0.0.1:3035"}), \
                patch.object(settings, "llm_provider", "openai"), \
                patch("auth.auth_call", side_effect=mock_auth), \
                patch("auth.jwks_client", return_value=SimpleNamespace(get_signing_key_from_jwt=lambda token: SimpleNamespace(key=signing_key.public_key()))), \
                patch("rag.retrieve", return_value=[SimpleNamespace(fields=record, score=0.95)]), \
                patch("rag.openai_client", return_value=model), \
                patch("learning_service.retrieve", return_value=[SimpleNamespace(fields=record, score=0.95)]), \
                patch("learning_service.openai_client", return_value=model):
            print("QA local: provedores simulados; nenhum consumo de IA.", flush=True)
            uvicorn.run(app, host="127.0.0.1", port=args.port, proxy_headers=False)


if __name__ == "__main__":
    main()
