"""Cada teste usa progresso isolado; nunca toca o SQLite do estudante."""

import pytest


@pytest.fixture(autouse=True)
def isolated_learning_db(tmp_path, monkeypatch):
    monkeypatch.setenv("LEARNING_DB_PATH", str(tmp_path / "learning.sqlite3"))
