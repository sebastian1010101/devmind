"""SQLite local: migração, reservas com lease e confirmações atômicas."""

import hashlib
import json
import os
import re
import sqlite3
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path, PurePosixPath
from uuid import uuid4
from zoneinfo import ZoneInfo

from config import settings
from providers import ServiceError
from review_schedule import GRADE_RECALL, advance, stamp, utc_now

LEARNER = "local-demo"
TIMEZONE = ZoneInfo("America/Sao_Paulo")
LIMITS = {"generation": 10, "review": 50, "chat": 50}


def encode(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def question_key(question: str) -> str:
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", question).casefold()))


def conflict(message="Esta solicitação já está em andamento. Tente novamente."):
    return ServiceError("request_conflict", message, 409)


class LearningStore:
    def __init__(self, path: str | Path | None = None, clock=utc_now, *, user_id=LEARNER):
        location = str(path or os.getenv("DATABASE_URL") or os.getenv("LEARNING_DB_PATH", "data/learning.sqlite3"))
        self.postgres = location.startswith(("postgresql://", "postgres://"))
        self.path = location if self.postgres else Path(location)
        self.clock = clock
        self.user_id = user_id
        if not self.postgres:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._migrate_sqlite()
        with self.connection(write=True) as db:
            if self.postgres and db.execute("SELECT max(version) FROM schema_version").fetchone()[0] != 2:
                raise ServiceError("database_version", "A base requer uma migração compatível com esta versão do DevMind.", 503)
            db.execute("INSERT INTO learners VALUES (?, ?, ?) ON CONFLICT(id) DO NOTHING",
                       (self.user_id, str(TIMEZONE), stamp(self.clock())))

    def for_user(self, user_id):
        if user_id == self.user_id:
            return self
        return LearningStore(self.path, clock=self.clock, user_id=user_id)

    def _migrate_sqlite(self):
        migrations = Path(__file__).parent / "migrations"
        with sqlite3.connect(self.path, timeout=10, isolation_level=None) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("BEGIN IMMEDIATE")
            try:
                version = db.execute("PRAGMA user_version").fetchone()[0]
                if version > 2:
                    raise ServiceError("database_version", "A base requer uma versão mais recente do DevMind.", 503)
                for number, name in [(1, "001_learning.sql"), (2, "002_multiuser.sql")]:
                    if version < number:
                        # Execute individual statements to keep the migration and version atomic.
                        for statement in (migrations / name).read_text().split(";"):
                            if statement.strip():
                                db.execute(statement)
                        db.execute(f"PRAGMA user_version={number}")
                db.commit()
            except Exception:
                db.rollback()
                raise

    @contextmanager
    def connection(self, write=False):
        if self.postgres:
            from database import postgres_connection
            with postgres_connection(self.path, self.user_id, write) as db:
                yield db
            return
        db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            if write:
                db.execute("BEGIN IMMEDIATE")
            yield db
            if write:
                db.commit()
        except sqlite3.OperationalError:
            if db.in_transaction:
                db.rollback()
            raise ServiceError("database_busy", "A base está ocupada ou indisponível. Tente novamente.", 503) from None
        except Exception:
            if db.in_transaction:
                db.rollback()
            raise
        finally:
            db.close()

    def local_date(self, now=None):
        return (now or self.clock()).astimezone(TIMEZONE).date().isoformat()

    def limit(self, kind):
        return max(0, int(os.getenv(f"AI_DAILY_{kind.upper()}_LIMIT", str(LIMITS[kind]))))

    def _quota(self, db, kind, now):
        day = self.local_date(now)
        row = db.execute("SELECT calls FROM daily_usage WHERE user_id=? AND local_date=? AND kind=?",
                         (self.user_id, day, kind)).fetchone()
        if (row[0] if row else 0) >= self.limit(kind):
            raise ServiceError("daily_limit", "Seu limite diário foi atingido. Volte amanhã.", 429)
        total = db.execute("SELECT calls FROM global_usage WHERE local_date=?", (day,)).fetchone()
        if (total[0] if total else 0) >= int(os.getenv("AI_GLOBAL_DAILY_LIMIT", "200")):
            raise ServiceError("global_limit", "A capacidade diária de IA foi atingida. Volte amanhã.", 429)
        db.execute("INSERT INTO global_usage VALUES (?, 1) ON CONFLICT(local_date) DO UPDATE SET calls=global_usage.calls+1", (day,))
        db.execute("INSERT INTO daily_usage VALUES (?, ?, ?, 1) "
                   "ON CONFLICT(user_id, local_date, kind) DO UPDATE SET calls=daily_usage.calls+1", (self.user_id, day, kind))

    def charge_chat(self):
        with self.connection(write=True) as db:
            self._quota(db, "chat", self.clock())

    def replay(self, kind, request_id, payload):
        """A completed request survives edits/removal of its original local scope."""
        with self.connection() as db:
            row = db.execute("SELECT fingerprint,state,result_json FROM operations WHERE user_id=? AND kind=? AND request_id=?",
                             (self.user_id, kind, request_id)).fetchone()
            if row and row["fingerprint"] != digest(encode(payload)):
                raise conflict("ID reutilizado com outros parâmetros. Use uma nova solicitação.")
            return json.loads(row["result_json"]) if row and row["state"] == "completed" else None

    def claim(self, kind: str, request_id: str, payload: dict, card_id=None):
        """Reserves before network I/O. Failed calls count; completed replays are free."""
        now = self.clock()
        fingerprint = digest(encode(payload))
        with self.connection(write=True) as db:
            row = db.execute("SELECT * FROM operations WHERE user_id=? AND kind=? AND request_id=?",
                             (self.user_id, kind, request_id)).fetchone()
            if row:
                if row["fingerprint"] != fingerprint:
                    raise conflict("ID reutilizado com outros parâmetros. Use uma nova solicitação.")
                if row["state"] == "completed":
                    return {"cached": json.loads(row["result_json"])}
                if row["state"] == "pending" and row["lease_until"] > stamp(now):
                    raise conflict()
            before = None
            if card_id:
                self._owned_card(db, card_id)
                pending = db.execute(
                    "SELECT 1 FROM operations WHERE user_id=? AND kind='review' AND card_id=? "
                    "AND request_id!=? AND state='pending' AND lease_until>?",
                    (self.user_id, card_id, request_id, stamp(now)),
                ).fetchone()
                if pending:
                    raise conflict("Este cartão já tem uma avaliação em andamento.")
                # A failed older request cannot overwrite a newer review.
                if row and db.execute(
                    "SELECT 1 FROM review_events WHERE user_id=? AND card_id=? AND created_at>?",
                    (self.user_id, card_id, row["created_at"]),
                ).fetchone():
                    raise conflict("Já existe uma revisão posterior. Envie uma nova resposta.")
                before = self._schedule(db, card_id)
                if row and row["base_schedule_json"] and json.loads(row["base_schedule_json"])["version"] != before["version"]:
                    raise conflict("O calendário avançou desde essa tentativa. Envie uma nova solicitação.")
            self._quota(db, kind, now)
            token = uuid4().hex
            db.execute(
                "INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?, NULL, NULL, ?, ?) "
                "ON CONFLICT(user_id,kind,request_id) DO UPDATE SET state='pending', lease_until=excluded.lease_until, "
                "lease_token=excluded.lease_token, base_schedule_json=excluded.base_schedule_json, "
                "error_code=NULL, updated_at=excluded.updated_at",
                (self.user_id, kind, request_id, fingerprint, encode(payload), card_id,
                 stamp(now + timedelta(seconds=max(120, settings.timeout * 3 + 30))), token, encode(before) if before else None, stamp(now), stamp(now)),
            )
            return {"token": token, "before": before}

    def _reservation(self, db, kind, request_id, token):
        row = db.execute("SELECT * FROM operations WHERE user_id=? AND kind=? AND request_id=?",
                         (self.user_id, kind, request_id)).fetchone()
        if not row or row["lease_token"] != token or row["state"] != "pending" or row["lease_until"] < stamp(self.clock()):
            raise conflict("A reserva expirou. Reenvie a mesma solicitação.")
        return row

    def fail(self, kind, request_id, token, code):
        with self.connection(write=True) as db:
            db.execute("UPDATE operations SET state='failed',error_code=?,updated_at=? "
                       "WHERE user_id=? AND kind=? AND request_id=? AND lease_token=? AND state='pending'",
                       (code, stamp(self.clock()), self.user_id, kind, request_id, token))

    def record_trace(self, kind, request_id, trace, error_code=None):
        from dataclasses import fields
        # Hits can contain SDK objects; persist only public metadata and measured usage.
        data = {item.name: getattr(trace, item.name) for item in fields(trace) if item.name != "hits"}
        with self.connection(write=True) as db:
            db.execute("INSERT INTO provider_runs VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (uuid4().hex, self.user_id, kind, request_id, trace.generation_model,
                        encode(data), error_code, stamp(self.clock())))

    def _complete(self, db, kind, request_id, result):
        db.execute("UPDATE operations SET state='completed', result_json=?,updated_at=? "
                   "WHERE user_id=? AND kind=? AND request_id=?",
                   (encode(result), stamp(self.clock()), self.user_id, kind, request_id))

    def save_cards(self, request_id, token, cards, evidence, scope, model, prompt_version):
        now = stamp(self.clock())
        with self.connection(write=True) as db:
            self._reservation(db, "generation", request_id, token)
            ids = []
            for card in cards:
                cited = [evidence[citation] for citation in dict.fromkeys(card.citations)]
                evidence_version = digest(encode(sorted((e["source"], e["text_sha256"]) for e in cited)))
                key = question_key(card.question) + "|" + evidence_version
                duplicate = db.execute("SELECT id FROM cards WHERE user_id=? AND module=? AND question_key=?",
                                       (self.user_id, scope["module"], key)).fetchone()
                if duplicate:
                    ids.append(duplicate[0])
                    continue
                card_id = str(uuid4())
                ids.append(card_id)
                topics = {PurePosixPath(e["source"]).parts[1].lower() for e in cited if len(PurePosixPath(e["source"]).parts) > 2}
                topic = scope.get("topic") or (next(iter(topics)) if len(topics) == 1 else None)
                db.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    card_id, self.user_id, scope["module"], topic, card.question, key,
                    card.reference_answer, card.explanation, encode(card.concepts), card.difficulty,
                    model, prompt_version, now,
                ))
                for citation in dict.fromkeys(card.citations):
                    item = evidence[citation]
                    db.execute("INSERT INTO card_evidence VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        card_id, citation, item["source"], item["section"], item["chunk_id"], item["chunk_text"],
                        item["text_sha256"], item["index_name"], item["namespace"], item["score"],
                    ))
                db.execute("INSERT INTO review_schedule(card_id,user_id,due_at) VALUES (?, ?, ?)",
                           (card_id, self.user_id, now))
            result = {"cards": [self._public_card(db, card_id) for card_id in dict.fromkeys(ids)], "request_id": request_id}
            self._complete(db, "generation", request_id, result)
            return result

    def _owned_card(self, db, card_id):
        card = db.execute("SELECT * FROM cards WHERE id=? AND user_id=?", (card_id, self.user_id)).fetchone()
        if not card:
            raise ServiceError("card_not_found", "Cartão não encontrado.", 404)
        return dict(card)

    def _schedule(self, db, card_id):
        row = db.execute("SELECT * FROM review_schedule WHERE card_id=? AND user_id=?", (card_id, self.user_id)).fetchone()
        return {k: row[k] for k in ("stage", "reviews", "lapses", "last_recall", "last_review_at", "due_at", "interval_days", "version")}

    def _evidence(self, db, card_id):
        from chunking import chunk_markdown
        from guide import read_guide_document
        evidence = [dict(row) for row in db.execute("SELECT e.* FROM card_evidence e JOIN cards c ON c.id=e.card_id WHERE e.card_id=? AND c.user_id=? ORDER BY evidence_id", (card_id, self.user_id))]
        for item in evidence:
            current = read_guide_document(item["source"])
            item["source_changed"] = current is None or not any(
                digest(chunk["chunk_text"]) == item["text_sha256"] for chunk in chunk_markdown(current)
            )
        return evidence

    def _public_card(self, db, card_id):
        card = self._owned_card(db, card_id)
        schedule = self._schedule(db, card_id)
        return {
            "id": card_id, "question": card["question"], "module": card["module"], "topic": card["topic"],
            "difficulty": card["difficulty"], "created_at": card["created_at"],
            "schedule": schedule,
            "learning_state": "new" if schedule["reviews"] == 0 else ("due" if schedule["due_at"] <= stamp(self.clock()) else "scheduled"),
            "sources": [{k: e[k] for k in ("evidence_id", "source", "section", "chunk_id", "text_sha256", "source_changed")}
                        for e in self._evidence(db, card_id)],
        }

    def card(self, card_id, private=False):
        with self.connection() as db:
            if private:
                return {**self._owned_card(db, card_id), "evidence": self._evidence(db, card_id)}
            card = self._public_card(db, card_id)
            # Restore a pending/failed answer or completed feedback after navigation/reload.
            row = db.execute("SELECT request_id,payload_json,state,result_json,error_code FROM operations "
                             "WHERE user_id=? AND kind='review' AND card_id=? ORDER BY created_at DESC,rowid DESC LIMIT 1",
                             (self.user_id, card_id)).fetchone()
            card["latest_attempt"] = ({
                "request_id": row["request_id"], "answer": json.loads(row["payload_json"])["answer"],
                "state": row["state"], "result": json.loads(row["result_json"]) if row["result_json"] else None,
            } if row else None)
            return card

    def _set_schedule(self, db, card_id, schedule):
        keys = list(schedule)
        db.execute("UPDATE review_schedule SET " + ",".join(f"{key}=?" for key in keys) + " WHERE card_id=? AND user_id=?",
                   (*[schedule[key] for key in keys], card_id, self.user_id))

    def save_review(self, request_id, token, evaluation, model, usage):
        now = self.clock()
        with self.connection(write=True) as db:
            operation = self._reservation(db, "review", request_id, token)
            card_id = operation["card_id"]
            before = json.loads(operation["base_schedule_json"])
            if self._schedule(db, card_id)["version"] != before["version"]:
                raise conflict("O calendário mudou durante a avaliação. Tente uma nova solicitação.")
            card = self._owned_card(db, card_id)
            recall = GRADE_RECALL.get(evaluation.grade)
            after = advance(before, recall, now) if recall else before
            event_id = str(uuid4())
            evidence = self._evidence(db, card_id)
            result = {
                "review_id": event_id, **evaluation.model_dump(), "self_recall": None,
                "reference_answer": card["reference_answer"], "explanation": card["explanation"],
                "sources": [e for e in evidence if e["evidence_id"] in evaluation.citations],
                "schedule": after,
                "notice": "A avaliação de IA pode falhar. Sua autoavaliação define a próxima revisão.",
            }
            db.execute("INSERT INTO review_events VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, ?)", (
                event_id, self.user_id, request_id, card_id, json.loads(operation["payload_json"])["answer"],
                evaluation.grade, encode(evaluation.model_dump()), encode(before), encode(result), model, encode(usage), stamp(now),
            ))
            self._set_schedule(db, card_id, after)
            self._complete(db, "review", request_id, result)
            return result

    def rate(self, event_id, recall):
        with self.connection(write=True) as db:
            row = db.execute("SELECT * FROM review_events WHERE id=? AND user_id=?", (event_id, self.user_id)).fetchone()
            if not row:
                raise ServiceError("review_not_found", "Revisão não encontrada.", 404)
            if row["self_recall"]:
                if row["self_recall"] != recall:
                    raise conflict("A autoavaliação já foi registrada.")
                return json.loads(row["result_json"])
            latest = db.execute("SELECT id FROM review_events WHERE user_id=? AND card_id=? ORDER BY created_at DESC,rowid DESC LIMIT 1",
                                (self.user_id, row["card_id"])).fetchone()[0]
            if latest != event_id:
                raise conflict("Somente a revisão mais recente pode ser autoavaliada.")
            if db.execute("SELECT 1 FROM operations WHERE user_id=? AND card_id=? AND kind='review' "
                          "AND state='pending' AND lease_until>?", (self.user_id, row["card_id"], stamp(self.clock()))).fetchone():
                raise conflict()
            before = json.loads(row["before_json"])
            after = advance(before, recall, datetime.fromisoformat(row["created_at"]))
            after["version"] = self._schedule(db, row["card_id"])["version"] + 1
            result = {**json.loads(row["result_json"]), "self_recall": recall, "schedule": after}
            self._set_schedule(db, row["card_id"], after)
            db.execute("UPDATE review_events SET self_recall=?,result_json=? WHERE id=? AND user_id=?", (recall, encode(result), event_id, self.user_id))
            self._complete(db, "review", row["request_id"], result)
            return result

    def _due_ids(self, db, limit):
        return [row[0] for row in db.execute(
            "SELECT s.card_id FROM review_schedule s JOIN cards c ON c.id=s.card_id "
            "WHERE s.user_id=? AND s.due_at<=? "
            "ORDER BY s.due_at ASC, s.lapses DESC, CASE c.difficulty WHEN 'hard' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END, c.id LIMIT ?",
            (self.user_id, stamp(self.clock()), limit))]

    def due(self, limit=5):
        with self.connection() as db:
            return {"cards": [self._public_card(db, i) for i in self._due_ids(db, limit)]}

    def daily(self):
        with self.connection(write=True) as db:
            day = self.local_date()
            session = db.execute("SELECT * FROM study_sessions WHERE user_id=? AND local_date=?", (self.user_id, day)).fetchone()
            if not session:
                session = {"id": str(uuid4()), "local_date": day, "created_at": stamp(self.clock())}
                db.execute("INSERT INTO study_sessions VALUES (?, ?, ?, ?)", (session["id"], self.user_id, day, session["created_at"]))
                for position, card_id in enumerate(self._due_ids(db, 5)):
                    db.execute("INSERT INTO daily_assignments VALUES (?, ?, ?)", (session["id"], card_id, position))
            items = []
            for item in db.execute("SELECT a.card_id FROM daily_assignments a JOIN study_sessions s ON s.id=a.session_id WHERE a.session_id=? AND s.user_id=? ORDER BY position", (session["id"], self.user_id)):
                card = self._public_card(db, item[0])
                card["completed"] = bool(db.execute(
                    "SELECT 1 FROM review_events WHERE user_id=? AND card_id=? AND created_at>=? "
                    "AND (grade!='ungradable' OR self_recall IS NOT NULL)", (self.user_id, item[0], session["created_at"])).fetchone())
                items.append(card)
            return {"id": session["id"], "local_date": day, "cards": items,
                    "completed": sum(item["completed"] for item in items), "total": len(items)}

    def progress(self):
        with self.connection() as db:
            usage = {row[0]: row[1] for row in db.execute("SELECT kind,calls FROM daily_usage WHERE user_id=? AND local_date=?", (self.user_id, self.local_date()))}
            total = db.execute("SELECT count(*) FROM cards WHERE user_id=?", (self.user_id,)).fetchone()[0]
            due = db.execute("SELECT count(*) FROM review_schedule WHERE user_id=? AND due_at<=?", (self.user_id, stamp(self.clock()))).fetchone()[0]
            reviewed = db.execute("SELECT count(*) FROM review_schedule WHERE user_id=? AND reviews>0", (self.user_id,)).fetchone()[0]
            events = db.execute("SELECT count(*),sum(CASE WHEN grade='correct' THEN 1 ELSE 0 END),sum(CASE WHEN grade!='ungradable' THEN 1 ELSE 0 END) FROM review_events WHERE user_id=?", (self.user_id,)).fetchone()
            topics = [dict(row) for row in db.execute(
                "SELECT c.module,c.topic,count(*) total,sum(CASE WHEN s.reviews>0 THEN 1 ELSE 0 END) reviewed,sum(CASE WHEN s.due_at<=? THEN 1 ELSE 0 END) due "
                "FROM cards c JOIN review_schedule s ON s.card_id=c.id WHERE c.user_id=? GROUP BY c.module,c.topic ORDER BY c.module,c.topic",
                (stamp(self.clock()), self.user_id))]
            upcoming = [dict(row) for row in db.execute(
                "SELECT c.id,c.question,s.due_at FROM cards c JOIN review_schedule s ON s.card_id=c.id "
                "WHERE c.user_id=? AND s.due_at>? ORDER BY s.due_at,c.id LIMIT 10", (self.user_id, stamp(self.clock())))]
            return {"total": total, "due": due, "reviewed": reviewed, "new": total - reviewed,
                    "attempts": events[0], "correct": events[1] or 0, "graded": events[2] or 0,
                    "topics": topics, "upcoming": upcoming, "local_date": self.local_date(),
                    "usage": {kind: {"used": usage.get(kind, 0), "limit": self.limit(kind)} for kind in LIMITS}}
