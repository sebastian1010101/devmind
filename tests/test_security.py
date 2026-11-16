"""Real cryptographic JWT checks and multi-account authorization through HTTP."""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

import api
import auth
import learning_api
from learning_models import Evaluation, GeneratedCard
from learning_store import LearningStore, digest
from providers import ServiceError
from security import ai_slot, rate_limit

A, B = str(uuid4()), str(uuid4())
SOURCE = "DEVMIND/Git/staging.md"
CARD = GeneratedCard(question="Como preservar as edições?", reference_answer="Retire do staging.",
                     explanation="Preserve as edições locais.", concepts=["Preservar edições"],
                     citations=["S1"], difficulty="medium")
EVAL = Evaluation(grade="correct", present_concepts=["Preservar edições"], missing_concepts=[], errors=[],
                  feedback="Você preservou as edições.", citations=["S1"])


@pytest.fixture
def identity(monkeypatch, tmp_path):
    key = ec.generate_private_key(ec.SECP256R1())
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_PUBLISHABLE_KEY", "public-test-key")
    monkeypatch.setattr(auth, "jwks_client", lambda url: SimpleNamespace(
        get_signing_key_from_jwt=lambda token: SimpleNamespace(key=key.public_key())))
    store = LearningStore(tmp_path / "accounts.sqlite3")
    monkeypatch.setattr(api, "get_store", lambda: store)
    monkeypatch.setattr(learning_api, "get_store", lambda: store)
    def token(user=A, **updates):
        now = int(datetime.now(timezone.utc).timestamp())
        claims = {"sub": user, "iss": "https://example.supabase.co/auth/v1", "aud": "authenticated", "role": "authenticated",
                  "email": f"{user}@example.com", "iat": now, "exp": now + 600}
        claims.update(updates)
        return jwt.encode(claims, key, algorithm="ES256", headers={"kid": "test-key"})
    client = TestClient(api.app)
    return SimpleNamespace(client=client, token=token, store=store, key=key)


def seed(store, request_id=None):
    request_id = request_id or str(uuid4())
    scope = {"module": "devmind", "topic": "git", "count": 1}
    claim = store.claim("generation", request_id, scope)
    evidence = {"S1": {"source": SOURCE, "section": "Staging", "chunk_id": 0, "chunk_text": "Preserve as edições locais.",
                        "text_sha256": digest("Preserve as edições locais."), "index_name": "shared", "namespace": "public", "score": 0.9}}
    return store.save_cards(request_id, claim["token"], [CARD], evidence, scope, "fixture", "v1")["cards"][0]


def bearer(s, user=A, **claims):
    return {"Authorization": f"Bearer {s.token(user, **claims)}"}


@pytest.mark.parametrize("path,method", [("/ask", "POST"), ("/learning/cards", "POST"), ("/learning/progress", "GET"),
    ("/learning/due", "GET"), ("/learning/daily", "GET"), (f"/learning/cards/{uuid4()}", "GET"),
    (f"/learning/cards/{uuid4()}/reviews", "POST"), (f"/learning/reviews/{uuid4()}/recall", "POST"), ("/auth/me", "GET")])
def test_private_endpoints_reject_missing_identity(identity, path, method):
    response = identity.client.request(method, path, json={}, headers={"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"})
    assert response.status_code == 401


@pytest.mark.parametrize("updates", [{"exp": 1}, {"iss": "https://attacker.example/auth/v1"}, {"aud": "other"},
    {"role": "anon"}, {"sub": "local-demo"}, {"is_anonymous": True}, {"iat": 9999999999}])
def test_reject_expired_wrong_issuer_audience_subject_and_role(identity, updates):
    response = identity.client.get("/learning/progress", headers=bearer(identity, **updates))
    assert response.status_code == 401


def test_valid_signed_jwt_and_tampered_signature(identity):
    assert identity.client.get("/learning/progress", headers=bearer(identity)).status_code == 200
    token = identity.token()
    other = ec.generate_private_key(ec.SECP256R1())
    forged = jwt.encode(jwt.decode(token, options={"verify_signature": False}), other, algorithm="ES256", headers={"kid": "test-key"})
    assert identity.client.get("/auth/me", headers={"Authorization": f"Bearer {forged}"}).status_code == 401
    unsigned = jwt.encode({"sub": A}, "", algorithm="none")
    assert identity.client.get("/auth/me", headers={"Authorization": f"Bearer {unsigned}"}).status_code == 401


def test_all_learning_objects_are_isolated_and_survive_restart(identity):
    s = identity
    a, b = s.store.for_user(A), s.store.for_user(B)
    request_id = str(uuid4())
    card = seed(a, request_id)
    review_id = str(uuid4())
    reservation = a.claim("review", review_id, {"card_id": card["id"], "answer": "Resposta privada de A"}, card["id"])
    result = a.save_review(review_id, reservation["token"], EVAL, "fixture", {})
    daily_a = a.daily()
    assert LearningStore(a.path, user_id=A).progress()["attempts"] == 1
    assert LearningStore(a.path, user_id=A).card(card["id"])["latest_attempt"]["answer"] == "Resposta privada de A"
    h = bearer(s, B)
    assert s.client.get(f"/learning/cards/{card['id']}", headers=h).status_code == 404
    assert s.client.post(f"/learning/cards/{card['id']}/reviews", headers=h, json={"request_id": str(uuid4()), "answer": "tentativa"}).status_code == 404
    assert s.client.post(f"/learning/reviews/{result['review_id']}/recall", headers=h, json={"recall": "good"}).status_code == 404
    assert s.client.get("/learning/due", headers=h).json()["cards"] == []
    assert s.client.get("/learning/progress", headers=h).json()["total"] == 0
    assert s.client.get("/learning/daily", headers=h).json()["id"] != daily_a["id"]
    assert b.replay("generation", request_id, {"module": "devmind", "topic": "git", "count": 1}) is None
    own_b = seed(b, request_id)
    assert own_b["id"] != card["id"]
    assert b.progress()["total"] == 1 and b.progress()["attempts"] == 0
    assert s.client.get("/learning/progress?user_id=" + A, headers=h).json()["attempts"] == 0
    assert "Resposta privada" not in s.client.get("/learning/progress", headers=h).text
    assert s.store.progress()["total"] == 0


def test_frontend_user_id_is_not_accepted_as_identity(identity):
    response = identity.client.post("/ask", headers=bearer(identity), json={"question": "Oi", "user_id": B})
    assert response.status_code == 422
    response = identity.client.post("/learning/cards", headers=bearer(identity), json={"request_id": str(uuid4()), "module": "devmind", "user_id": B})
    assert response.status_code == 422


def test_cookie_mutations_require_origin_and_csrf_header(identity):
    s = identity
    s.client.cookies.set(auth.ACCESS_COOKIE, s.token())
    assert s.client.post("/ask", json={"question": "Oi"}).status_code == 403
    assert s.client.post("/ask", headers={"Origin": "https://evil.example", "X-DevMind-CSRF": "1"}, json={"question": "Oi"}).status_code == 403
    assert s.client.post("/auth/login", headers={"Origin": "http://localhost:3035"}, json={"email": "x@example.com", "password": "secret"}).status_code == 403


def test_login_confirm_refresh_password_logout_http_only(identity, monkeypatch):
    calls = []
    session = {"access_token": identity.token(), "refresh_token": "refresh-secret", "expires_in": 600,
               "user": {"id": A, "email_confirmed_at": "2026-11-16T00:00:00Z"}}
    def provider(method, path, **kwargs):
        calls.append((method, path, kwargs))
        return session
    monkeypatch.setattr(auth, "auth_call", provider)
    monkeypatch.setenv("APP_ENV", "production")
    # Secure cookies require an HTTPS test origin.
    c = TestClient(api.app, base_url="https://testserver", headers={"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"})
    r = c.post("/auth/login", json={"email": "a@example.com", "password": "existing"})
    assert r.status_code == 200 and "access_token" not in r.text and "refresh-secret" not in r.text
    assert all("HttpOnly" in cookie and "Secure" in cookie and "SameSite=lax" in cookie for cookie in r.headers.get_list("set-cookie"))
    assert c.get("/auth/me").json()["id"] == A
    # /api/auth is the browser-facing cookie path. The same-origin proxy strips /api.
    r = c.post("/auth/refresh", cookies={auth.REFRESH_COOKIE: "refresh-secret"})
    assert r.status_code == 200 and calls[-1][1] == "token?grant_type=refresh_token"
    assert c.post("/auth/password", json={"password": "new-long-password"}).status_code == 200
    assert calls[-1][1] == "logout?scope=global"
    r = c.post("/auth/logout")
    assert r.status_code == 204 and all("Max-Age=0" in cookie for cookie in r.headers.get_list("set-cookie"))


def test_signup_verification_and_recovery_contract(identity, monkeypatch):
    calls = []
    def provider(method, path, **kwargs):
        calls.append((method, path, kwargs))
        if path == "signup":
            return {}
        return {"access_token": identity.token(), "refresh_token": "refresh", "user": {"email_confirmed_at": "confirmed"}}
    monkeypatch.setattr(auth, "auth_call", provider)
    c = identity.client
    h = {"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"}
    body = {"email": "new@example.com", "password": "sufficient-long-password", "adult": True, "accepted_terms": True, "country": "BR"}
    assert c.post("/auth/signup", headers=h, json=body).status_code == 200
    assert calls[-1][1] == "signup"
    assert c.post("/auth/signup", headers=h, json={**body, "adult": False}).status_code == 422
    assert c.post("/auth/signup", headers=h, json={**body, "country": "GB"}).status_code == 422
    assert c.post("/auth/verify", headers=h, json={"email": body["email"], "token": "123456", "type": "signup"}).status_code == 200
    assert c.post("/auth/recover", headers=h, json={"email": body["email"]}).status_code == 200
    assert c.post("/auth/verify", headers=h, json={"email": body["email"], "token": "123456", "type": "recovery"}).status_code == 200


def test_unconfirmed_email_cannot_create_cookie_session(identity, monkeypatch):
    monkeypatch.setattr(auth, "auth_call", lambda *a, **k: {"access_token": identity.token(), "refresh_token": "secret", "user": {}})
    r = identity.client.post("/auth/login", headers={"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"}, json={"email": "a@example.com", "password": "password"})
    assert r.status_code == 403 and not r.headers.get_list("set-cookie")


def test_persistent_atomic_daily_quotas_and_global_budget(identity, monkeypatch):
    a, b = identity.store.for_user(A), identity.store.for_user(B)
    monkeypatch.setenv("AI_DAILY_CHAT_LIMIT", "1")
    a.charge_chat()
    with pytest.raises(ServiceError, match="limite diário"):
        LearningStore(a.path, user_id=A).charge_chat()
    b.charge_chat()
    monkeypatch.setenv("AI_GLOBAL_DAILY_LIMIT", "2")
    with pytest.raises(ServiceError):
        identity.store.for_user(str(uuid4())).charge_chat()


def test_concurrent_quota_reservations_cannot_overspend(identity, monkeypatch):
    monkeypatch.setenv("AI_DAILY_CHAT_LIMIT", "1")
    a = identity.store.for_user(A)
    def call(_):
        try:
            a.charge_chat()
            return True
        except ServiceError:
            return False
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert sum(pool.map(call, range(8))) == 1


def test_rate_limit_and_concurrency_are_persistent(identity, monkeypatch):
    a = identity.store.for_user(A)
    rate_limit(a, "ip:test", 1)
    with pytest.raises(Exception) as exc:
        rate_limit(LearningStore(a.path, user_id=B), "ip:test", 1)
    assert exc.value.status_code == 429
    with ai_slot(a):
        with pytest.raises(ServiceError) as exc:
            with ai_slot(LearningStore(a.path, user_id=A)):
                pass
        assert exc.value.status == 429
    with ai_slot(a):
        pass


def test_ip_rate_limiter_ignores_untrusted_forwarding_headers(identity, monkeypatch):
    monkeypatch.setenv("IP_REQUESTS_PER_MINUTE", "1")
    assert identity.client.get("/auth/me", headers={**bearer(identity), "X-Forwarded-For": "1.1.1.1"}).status_code == 200
    r = identity.client.get("/auth/me", headers={**bearer(identity), "X-Forwarded-For": "2.2.2.2"})
    assert r.status_code == 429 and int(r.headers["Retry-After"]) > 0


def test_sqlite_v1_migration_preserves_legacy_owner(tmp_path):
    import sqlite3
    from pathlib import Path
    path = tmp_path / "legacy.sqlite3"
    with sqlite3.connect(path) as db:
        db.executescript(Path("migrations/001_learning.sql").read_text() + "PRAGMA user_version=1;")
        db.execute("INSERT INTO learners VALUES ('local-demo','America/Sao_Paulo','2026-11-12')")
    local = LearningStore(path)
    card = seed(local)
    assert LearningStore(path).card(card["id"])["id"] == card["id"]
    assert LearningStore(path, user_id=A).progress()["total"] == 0


def test_zero_quota_disables_ai_before_first_call(identity, monkeypatch):
    monkeypatch.setenv("AI_DAILY_CHAT_LIMIT", "0")
    with pytest.raises(ServiceError):
        identity.store.for_user(A).charge_chat()
    monkeypatch.setenv("AI_DAILY_CHAT_LIMIT", "10")
    monkeypatch.setenv("AI_GLOBAL_DAILY_LIMIT", "0")
    with pytest.raises(ServiceError):
        identity.store.for_user(A).charge_chat()


def test_rs256_supabase_signatures(identity, monkeypatch):
    from cryptography.hazmat.primitives.asymmetric import rsa
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    monkeypatch.setattr(auth, "jwks_client", lambda url: SimpleNamespace(
        get_signing_key_from_jwt=lambda token: SimpleNamespace(key=key.public_key())))
    claims = jwt.decode(identity.token(), options={"verify_signature": False})
    token = jwt.encode(claims, key, algorithm="RS256", headers={"kid": "rsa-key"})
    assert identity.client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 200


def test_legacy_hmac_and_missing_required_claims_are_rejected(identity):
    claims = jwt.decode(identity.token(), options={"verify_signature": False})
    token = jwt.encode(claims, "legacy-secret-is-not-a-public-jwk", algorithm="HS256", headers={"kid": "hmac"})
    assert identity.client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    claims.pop("exp")
    token = jwt.encode(claims, identity.key, algorithm="ES256", headers={"kid": "test-key"})
    assert identity.client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_jwks_network_failure_is_sanitized(identity, monkeypatch):
    def unavailable(token):
        raise jwt.PyJWKClientConnectionError("private provider detail")
    monkeypatch.setattr(auth, "jwks_client", lambda url: SimpleNamespace(get_signing_key_from_jwt=unavailable))
    r = identity.client.get("/auth/me", headers=bearer(identity))
    assert r.status_code == 503 and "private provider detail" not in r.text


def test_signup_requires_confirmation_and_explicit_production_opening(identity, monkeypatch):
    body = {"email": "a@example.com", "password": "test-password-1234", "adult": True, "accepted_terms": True, "country": "BR"}
    headers = {"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"}
    monkeypatch.setattr(auth, "auth_call", lambda *a, **kw: {"access_token": "unexpected auto-confirm session"})
    assert identity.client.post("/auth/signup", headers=headers, json=body).status_code == 503
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("SIGNUP_ENABLED", raising=False)
    r = identity.client.post("/auth/signup", headers=headers, json=body)
    assert r.status_code == 503 and "unexpected" not in r.text


def test_logout_can_revoke_a_session_with_only_refresh_cookie(identity, monkeypatch):
    calls = []
    def provider(method, path, **kwargs):
        calls.append(path)
        return {"access_token": identity.token()}
    monkeypatch.setattr(auth, "auth_call", provider)
    identity.client.cookies.set(auth.REFRESH_COOKIE, "refresh-only")
    r = identity.client.post("/auth/logout", headers={"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"})
    assert r.status_code == 204
    assert calls == ["token?grant_type=refresh_token", "logout?scope=local"]


def test_root_path_preserves_rate_limiting(identity, monkeypatch):
    monkeypatch.setenv("IP_REQUESTS_PER_MINUTE", "1")
    with TestClient(api.app, root_path="/api", base_url="http://testserver/api/") as client:
        assert client.get("auth/me", headers=bearer(identity)).status_code == 200
        assert client.get("auth/me", headers=bearer(identity)).status_code == 429


def test_oversized_stream_is_rejected_before_model_or_json_processing(identity):
    def body():
        yield b'{"question":"private-answer'
        yield b'x' * (33 * 1024)
        yield b'"}'
    r = identity.client.post("/ask", headers={**bearer(identity), "Content-Type": "application/json"}, content=body())
    assert r.status_code == 413 and "private-answer" not in r.text


def test_password_changed_but_logout_failure_reports_partial_result_and_clears_cookies(identity, monkeypatch):
    def provider(method, path, **kwargs):
        if path.startswith("logout"):
            raise ServiceError("auth_unavailable", "private upstream detail", 503)
        return {}
    monkeypatch.setattr(auth, "auth_call", provider)
    response = identity.client.post("/auth/password", headers=bearer(identity), json={"password": "updated-password-1234"})
    assert response.status_code == 503
    assert "senha foi atualizada" in response.json()["detail"]
    assert "private upstream detail" not in response.text
    assert all("Max-Age=0" in cookie for cookie in response.headers.get_list("set-cookie"))
