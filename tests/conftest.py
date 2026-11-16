"""Cada teste usa progresso isolado; nunca toca o SQLite do estudante."""

import pytest


@pytest.fixture(autouse=True)
def isolated_learning_db(tmp_path, monkeypatch):
    monkeypatch.setenv("LEARNING_DB_PATH", str(tmp_path / "learning.sqlite3"))


@pytest.fixture(autouse=True)
def legacy_contracts(request, monkeypatch):
    """Existing pipeline tests retain their OpenAI fixtures and explicit test identity."""
    from config import settings
    monkeypatch.setattr(settings, "llm_provider", "openai")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("AUTH_REQUESTS_PER_MINUTE", "1000")
    monkeypatch.setenv("IP_REQUESTS_PER_MINUTE", "1000")
    monkeypatch.setenv("USER_REQUESTS_PER_MINUTE", "1000")
    if request.module.__name__ not in {"test_api", "test_learning", "test_live_integration"}:
        yield
        return
    import api
    from auth import User, current_user
    from fastapi.testclient import TestClient
    original = TestClient.__init__
    def authorized_init(self, *args, **kwargs):
        original(self, *args, **kwargs)
        self.headers.update({"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"})
    monkeypatch.setattr(TestClient, "__init__", authorized_init)
    client = getattr(request.module, "client", None)
    if client:
        client.headers.update({"Origin": "http://localhost:3035", "X-DevMind-CSRF": "1"})
    api.app.dependency_overrides[current_user] = lambda: User("local-demo", "fixture@example.com")
    yield
    api.app.dependency_overrides.pop(current_user, None)
