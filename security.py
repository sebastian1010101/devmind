"""Origin/CSRF checks and persistent rate and concurrency limits."""

import hashlib
import ipaddress
import os
from contextlib import contextmanager
from datetime import timedelta
from uuid import uuid4

from fastapi import HTTPException, Request

from config import settings
from providers import ServiceError
from review_schedule import stamp


def origins():
    return {value.strip().rstrip("/") for value in os.getenv(
        "FRONTEND_ORIGIN", "http://localhost:3035,http://127.0.0.1:3035",
    ).split(",") if value.strip()}


def csrf_check(request: Request):
    origin = request.headers.get("origin")
    if origin and origin not in origins():
        raise HTTPException(403, "Origem não autorizada.")
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        bearer = request.headers.get("authorization", "").lower().startswith("bearer ")
        if not bearer and (not origin or request.headers.get("x-devmind-csrf") != "1"):
            raise HTTPException(403, "Requisição inválida. Recarregue a página e tente novamente.")


def client_ip(request):
    peer = request.client.host if request.client else "unknown"
    trusted = [ipaddress.ip_network(value.strip()) for value in os.getenv("TRUSTED_PROXY_CIDRS", "").split(",") if value.strip()]
    chain = [item.strip() for item in request.headers.get("x-forwarded-for", "").split(",") if item.strip()] + [peer]
    # Walk from the TCP peer toward the client, stopping at the first untrusted hop.
    for address in reversed(chain):
        try:
            parsed = ipaddress.ip_address(address)
        except ValueError:
            return "unknown"
        if not any(parsed in network for network in trusted):
            return str(parsed)
    return chain[0]


def rate_limit(store, key, limit, window=60):
    now = int(store.clock().timestamp())
    start = now - now % window
    hashed = hashlib.sha256(key.encode()).hexdigest()
    with store.connection(write=True) as db:
        db.execute("DELETE FROM rate_buckets WHERE window_start<?", (start - 86400,))
        row = db.execute("SELECT window_start,calls FROM rate_buckets WHERE bucket_key=?", (hashed,)).fetchone()
        calls = row[1] if row and row[0] == start else 0
        if calls >= limit:
            raise HTTPException(429, "Muitas solicitações. Aguarde antes de continuar.", headers={"Retry-After": str(window - now % window)})
        db.execute("INSERT INTO rate_buckets VALUES (?, ?, 1) ON CONFLICT(bucket_key) DO UPDATE SET "
                   "window_start=excluded.window_start,calls=CASE WHEN rate_buckets.window_start=excluded.window_start "
                   "THEN rate_buckets.calls+1 ELSE 1 END", (hashed, start))


@contextmanager
def ai_slot(store):
    lease = uuid4().hex
    now = store.clock()
    with store.connection(write=True) as db:
        db.execute("DELETE FROM ai_leases WHERE expires_at<=?", (stamp(now),))
        total = db.execute("SELECT count(*) FROM ai_leases").fetchone()[0]
        own = db.execute("SELECT count(*) FROM ai_leases WHERE user_id=?", (store.user_id,)).fetchone()[0]
        if own >= int(os.getenv("AI_USER_CONCURRENCY", "1")) or total >= int(os.getenv("AI_GLOBAL_CONCURRENCY", "4")):
            raise ServiceError("concurrency_limit", "Há operações de IA em andamento. Aguarde e tente novamente.", 429)
        db.execute("INSERT INTO ai_leases VALUES (?, ?, ?)", (lease, store.user_id, stamp(now + timedelta(seconds=max(120, settings.timeout * 3 + 30)))))
    try:
        yield
    finally:
        with store.connection(write=True) as db:
            db.execute("DELETE FROM ai_leases WHERE id=? AND user_id=?", (lease, store.user_id))


class RequestBodyLimit:
    """Bound request buffering even when Content-Length is absent or incorrect."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        size = 0

        async def limited_receive():
            nonlocal size
            message = await receive()
            if message["type"] == "http.request":
                size += len(message.get("body", b""))
                if size > 32 * 1024:
                    raise HTTPException(413, "A solicitação excede o tamanho permitido.")
            return message

        if scope["type"] == "http" and scope["method"] in {"POST", "PUT", "PATCH"}:
            await self.app(scope, limited_receive, send)
        else:
            await self.app(scope, receive, send)
