"""Supabase Auth REST, JWT verification and server-only cookie sessions."""

import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated, Literal
from uuid import UUID

import httpx
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, StringConstraints

from providers import ServiceError, require_key

logger = logging.getLogger(__name__)
ACCESS_COOKIE = "devmind_access"
REFRESH_COOKIE = "devmind_refresh"
router = APIRouter(prefix="/auth", tags=["Authentication"])
Email = Annotated[str, StringConstraints(strip_whitespace=True, max_length=254, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")]
Password = Annotated[str, StringConstraints(min_length=12, max_length=128)]


@dataclass(frozen=True)
class User:
    id: str
    email: str


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: Email
    # Existing Supabase accounts may have shorter passwords.
    password: Annotated[str, StringConstraints(min_length=1, max_length=128)]


class Signup(Credentials):
    password: Password
    adult: Literal[True]
    accepted_terms: Literal[True]
    country: Literal["BR"]


class EmailRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: Email


class Verification(EmailRequest):
    token: Annotated[str, StringConstraints(pattern=r"^\d{6,10}$")]
    type: Literal["signup", "recovery"] = "signup"


class NewPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    password: Password


def supabase_url():
    url = require_key("SUPABASE_URL").rstrip("/")
    if not url.startswith("https://"):
        raise ServiceError("auth_config", "Configure uma URL HTTPS do Supabase no servidor.", 503)
    return url


@lru_cache(maxsize=4)
def jwks_client(url):
    return jwt.PyJWKClient(f"{url}/auth/v1/.well-known/jwks.json", cache_jwk_set=True, lifespan=300, timeout=5)


def verify_token(token: str) -> User:
    if len(token) > 16_384:
        raise HTTPException(401, "Sessão inválida. Entre novamente.")
    issuer = f"{supabase_url()}/auth/v1"
    try:
        header = jwt.get_unverified_header(token)
        if header.get("alg") not in {"ES256", "RS256"} or not isinstance(header.get("kid"), str):
            raise jwt.InvalidTokenError()
        key = jwks_client(supabase_url()).get_signing_key_from_jwt(token)
        claims = jwt.decode(token, key.key, algorithms=[header["alg"]], audience="authenticated", issuer=issuer,
                            options={"require": ["exp", "iat", "iss", "aud", "sub", "role"]})
        user_id = str(UUID(claims["sub"]))
        if claims["role"] != "authenticated" or claims.get("is_anonymous") is True:
            raise jwt.InvalidTokenError()
        return User(user_id, claims.get("email", ""))
    except jwt.PyJWKClientConnectionError:
        raise ServiceError("auth_unavailable", "Não foi possível verificar a sessão. Tente novamente.", 503) from None
    except (jwt.PyJWTError, ValueError, TypeError, KeyError):
        raise HTTPException(401, "Sessão inválida ou expirada. Entre novamente.") from None


def access_token(request: Request):
    authorization = request.headers.get("authorization", "")
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise HTTPException(401, "Sessão inválida. Entre novamente.")
        return token
    return request.cookies.get(ACCESS_COOKIE)


def current_user(request: Request) -> User:
    token = access_token(request)
    if not token:
        raise HTTPException(401, "Entre na sua conta para continuar.")
    return verify_token(token)


def auth_call(method, path, *, payload=None, token=None):
    headers = {"apikey": require_key("SUPABASE_PUBLISHABLE_KEY")}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = httpx.request(method, f"{supabase_url()}/auth/v1/{path}", headers=headers,
                                 json=payload, timeout=10, follow_redirects=False)
    except httpx.RequestError:
        raise ServiceError("auth_unavailable", "O serviço de acesso está indisponível. Tente novamente.", 503) from None
    if response.status_code >= 400:
        logger.warning("auth_failure status=%s", response.status_code)
        if response.status_code == 429:
            raise HTTPException(429, "Muitas tentativas. Aguarde antes de tentar novamente.", headers={"Retry-After": "60"})
        if response.status_code >= 500:
            raise ServiceError("auth_unavailable", "O serviço de acesso está indisponível. Tente novamente.", 503)
        raise HTTPException(400, "Não foi possível concluir. Confira os dados e a confirmação de email.")
    try:
        data = response.json() if response.content else {}
        if not isinstance(data, dict):
            raise ValueError()
        return data
    except ValueError:
        raise ServiceError("auth_unavailable", "O serviço de acesso retornou uma resposta inválida.", 502) from None


def secure_cookies():
    return os.getenv("APP_ENV", "development") == "production"


def set_session(response: Response, session):
    token = session.get("access_token", "")
    user = verify_token(token)
    if not session.get("user", {}).get("email_confirmed_at"):
        raise HTTPException(403, "Confirme seu email antes de entrar.")
    refresh = session.get("refresh_token")
    if not isinstance(refresh, str) or not refresh:
        raise ServiceError("auth_unavailable", "O serviço de acesso retornou uma sessão inválida.", 502)
    response.set_cookie(ACCESS_COOKIE, token, max_age=int(session.get("expires_in", 3600)),
                        httponly=True, secure=secure_cookies(), samesite="lax", path="/")
    response.set_cookie(REFRESH_COOKIE, refresh, max_age=30 * 86400,
                        httponly=True, secure=secure_cookies(), samesite="lax", path="/api/auth")
    response.headers["Cache-Control"] = "no-store"
    return {"id": user.id, "email": user.email}


def clear_session(response):
    response.delete_cookie(ACCESS_COOKIE, path="/", secure=secure_cookies(), httponly=True, samesite="lax")
    response.delete_cookie(REFRESH_COOKIE, path="/api/auth", secure=secure_cookies(), httponly=True, samesite="lax")
    response.headers["Cache-Control"] = "no-store"


@router.post("/signup")
def signup(body: Signup):
    if os.getenv("SIGNUP_ENABLED", "false" if secure_cookies() else "true").lower() != "true":
        raise HTTPException(503, "Novas contas estão temporariamente indisponíveis.")
    # Supabase manages credentials, hashing, confirmation and account enumeration protection.
    result = auth_call("POST", "signup", payload={"email": body.email, "password": body.password,
              "data": {"adult": True, "country": body.country, "terms_version": "2026-11-16"}})
    if result.get("access_token"):
        raise ServiceError("auth_config", "Ative a confirmação de email no Supabase antes de registrar contas.", 503)
    return {"message": "Confira seu email e use o código de confirmação para ativar a conta."}


@router.post("/login")
def login(body: Credentials, response: Response):
    return set_session(response, auth_call("POST", "token?grant_type=password", payload=body.model_dump()))


@router.post("/verify")
def verify(body: Verification, response: Response):
    return set_session(response, auth_call("POST", "verify", payload=body.model_dump()))


@router.post("/recover")
def recover(body: EmailRequest):
    try:
        auth_call("POST", "recover", payload=body.model_dump())
    except HTTPException as exc:
        if exc.status_code != 400:
            raise
    return {"message": "Se houver uma conta com esse email, você receberá um código para recuperar o acesso."}


@router.post("/resend")
def resend(body: EmailRequest):
    try:
        auth_call("POST", "resend", payload={**body.model_dump(), "type": "signup"})
    except HTTPException as exc:
        if exc.status_code != 400:
            raise
    return {"message": "Se necessário, um novo código de confirmação será enviado ao seu email."}


@router.post("/refresh")
def refresh(request: Request, response: Response):
    token = request.cookies.get(REFRESH_COOKIE)
    if not token:
        raise HTTPException(401, "Sua sessão expirou. Entre novamente.")
    return set_session(response, auth_call("POST", "token?grant_type=refresh_token", payload={"refresh_token": token}))


@router.post("/password")
def password(body: NewPassword, request: Request, response: Response, user: User = Depends(current_user)):
    auth_call("PUT", "user", payload=body.model_dump(), token=access_token(request))
    # Revoke provider refresh tokens after changing credentials.
    try:
        auth_call("POST", "logout?scope=global", token=access_token(request))
    except (HTTPException, ServiceError):
        logger.warning("auth_global_logout_after_password_failed")
        failure = JSONResponse(status_code=503, content={
            "detail": "Sua senha foi atualizada. O encerramento das outras sessões está pendente. Entre com a nova senha e tente encerrar as sessões novamente.",
        })
        clear_session(failure)
        return failure
    clear_session(response)
    return {"message": "Senha atualizada. Entre novamente para continuar."}


@router.post("/logout")
def logout(request: Request):
    response = Response(status_code=204)
    token = access_token(request)
    try:
        refresh_token = request.cookies.get(REFRESH_COOKIE)
        if not token and refresh_token:
            session = auth_call("POST", "token?grant_type=refresh_token", payload={"refresh_token": refresh_token})
            token = session.get("access_token")
        if token:
            auth_call("POST", "logout?scope=local", token=token)
    except (HTTPException, ServiceError):
        # Cookies are cleared even when the upstream session already expired.
        pass
    clear_session(response)
    return response


@router.get("/me")
def me(response: Response, user: User = Depends(current_user)):
    response.headers["Cache-Control"] = "no-store"
    return {"id": user.id, "email": user.email}
