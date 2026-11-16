"""Opt-in tests against a dedicated PostgreSQL test database."""

import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest

from learning_store import LearningStore
from manage_db import import_sqlite, migrate
from providers import ServiceError
from security import ai_slot
from test_security import EVAL, seed

pytestmark = pytest.mark.skipif(not os.getenv("TEST_DATABASE_URL"), reason="Set TEST_DATABASE_URL for a dedicated PostgreSQL database")


@pytest.fixture
def postgres():
    url = os.environ["TEST_DATABASE_URL"]
    migrate(url)
    return url


def test_postgres_learning_idempotency_isolation_and_persistence(postgres):
    a, b = LearningStore(postgres, user_id=str(uuid4())), LearningStore(postgres, user_id=str(uuid4()))
    request_id = str(uuid4())
    card = seed(a, request_id)
    assert a.card(card["id"])["id"] == card["id"]
    with pytest.raises(ServiceError) as exc:
        b.card(card["id"])
    assert exc.value.status == 404
    review_id = str(uuid4())
    claim = a.claim("review", review_id, {"card_id": card["id"], "answer": "Preservar edições"}, card["id"])
    result = a.save_review(review_id, claim["token"], EVAL, "fixture", {})
    a.rate(result["review_id"], "easy")
    reopened = LearningStore(postgres, user_id=a.user_id)
    assert reopened.card(card["id"])["schedule"]["reviews"] == 1
    assert reopened.progress()["attempts"] == 1
    assert b.progress()["total"] == 0
    assert reopened.daily()["id"] == a.daily()["id"]
    assert b.daily()["id"] != a.daily()["id"]
    with ai_slot(a):
        with pytest.raises(ServiceError):
            with ai_slot(reopened):
                pass


def test_postgres_atomic_quota(postgres, monkeypatch):
    store = LearningStore(postgres, user_id=str(uuid4()))
    monkeypatch.setenv("AI_DAILY_CHAT_LIMIT", "1")
    def charge(_):
        try:
            store.charge_chat()
            return True
        except ServiceError:
            return False
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert sum(pool.map(charge, range(8))) == 1


def test_postgres_rls_applies_to_non_owner_role(postgres):
    import psycopg
    a, b = LearningStore(postgres, user_id=str(uuid4())), LearningStore(postgres, user_id=str(uuid4()))
    card = seed(a)
    # Temporary role is transaction-scoped through rollback. Requires test DB owner.
    with psycopg.connect(postgres) as db:
        role = "qa_" + uuid4().hex
        db.execute(f'CREATE ROLE "{role}" NOLOGIN')
        db.execute(f'GRANT USAGE ON SCHEMA devmind TO "{role}"')
        db.execute(f'GRANT SELECT ON ALL TABLES IN SCHEMA devmind TO "{role}"')
        db.execute(f'SET LOCAL ROLE "{role}"')
        db.execute("SELECT set_config('app.user_id', %s, true)", (b.user_id,))
        assert db.execute("SELECT id FROM devmind.cards WHERE id=%s", (card["id"],)).fetchall() == []
        assert db.execute("SELECT card_id FROM devmind.card_evidence WHERE card_id=%s", (card["id"],)).fetchall() == []
        db.execute("SELECT set_config('app.user_id', %s, true)", (a.user_id,))
        assert len(db.execute("SELECT id FROM devmind.cards WHERE id=%s", (card["id"],)).fetchall()) == 1
        db.rollback()


def test_sqlite_import_preserves_source_and_reassigns_only_explicit_owner(postgres, tmp_path):
    import hashlib
    import psycopg
    from psycopg import sql
    from urllib.parse import urlsplit, urlunsplit
    source = tmp_path / "legacy.sqlite3"
    original = LearningStore(source)
    card = seed(original)
    review_id = str(uuid4())
    claim = original.claim("review", review_id, {"card_id": card["id"], "answer": "Resposta histórica"}, card["id"])
    review = original.save_review(review_id, claim["token"], EVAL, "fixture", {})
    original.rate(review["review_id"], "easy")
    session_id = original.daily()["id"]
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    database = "import_" + uuid4().hex
    parts = urlsplit(postgres)
    target = urlunsplit(parts._replace(path="/" + database))
    with psycopg.connect(postgres, autocommit=True) as admin:
        admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
        try:
            migrate(target)
            owner = str(uuid4())
            import_sqlite(target, source, owner)
            assert LearningStore(target, user_id=owner).card(card["id"])["schedule"]["interval_days"] == 3
            assert LearningStore(target, user_id=owner).progress()["attempts"] == 1
            assert LearningStore(target, user_id=owner).daily()["id"] == session_id
            assert LearningStore(target, user_id=str(uuid4())).progress()["total"] == 0
            assert hashlib.sha256(source.read_bytes()).hexdigest() == before
            with pytest.raises(RuntimeError, match="vazio"):
                import_sqlite(target, source, owner)
            assert LearningStore(target, user_id=owner).progress()["total"] == 1
        finally:
            admin.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(database)))
