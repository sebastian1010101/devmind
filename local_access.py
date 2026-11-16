"""Escopo explícito de demo local, sem alegar autenticação multiusuário."""

import ipaddress
import os

from fastapi import HTTPException, Request


def local_demo_access(request: Request):
    host = request.client.host if request.client else ""
    try:
        loopback = ipaddress.ip_address(host).is_loopback
    except ValueError:
        loopback = host == "testclient"  # In-process Starlette transport; never a TCP peer.
    allowed_hosts = {"localhost", "127.0.0.1", "::1", "testserver"}
    origins = {value.strip() for value in os.getenv(
        "FRONTEND_ORIGIN", "http://localhost:3035,http://127.0.0.1:3035",
    ).split(",")}
    if not loopback or request.url.hostname not in allowed_hosts or (
        request.headers.get("origin") and request.headers["origin"] not in origins
    ):
        raise HTTPException(403, "Active Recall e IA disponíveis somente na demo local. Execute sem proxy público.")
