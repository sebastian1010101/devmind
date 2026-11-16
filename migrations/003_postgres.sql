-- Run with manage_db.py migrate against an empty application database.
CREATE SCHEMA IF NOT EXISTS devmind;
REVOKE ALL ON SCHEMA devmind FROM PUBLIC;
SET search_path TO devmind, pg_catalog;
CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY);
CREATE TABLE IF NOT EXISTS learners (
    id TEXT PRIMARY KEY, timezone TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cards (
    id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES learners(id),
    module TEXT NOT NULL, topic TEXT, question TEXT NOT NULL,
    question_key TEXT NOT NULL, reference_answer TEXT NOT NULL,
    explanation TEXT NOT NULL, concepts_json TEXT NOT NULL, difficulty TEXT NOT NULL,
    model TEXT NOT NULL, prompt_version TEXT NOT NULL, created_at TEXT NOT NULL,
    UNIQUE(user_id, module, question_key)
);
CREATE TABLE IF NOT EXISTS card_evidence (
    card_id TEXT NOT NULL REFERENCES cards(id), evidence_id TEXT NOT NULL,
    source TEXT NOT NULL, section TEXT NOT NULL, chunk_id INTEGER,
    chunk_text TEXT NOT NULL, text_sha256 TEXT NOT NULL,
    index_name TEXT NOT NULL, namespace TEXT NOT NULL, score REAL NOT NULL,
    PRIMARY KEY(card_id, evidence_id)
);
CREATE TABLE IF NOT EXISTS review_schedule (
    card_id TEXT PRIMARY KEY REFERENCES cards(id), user_id TEXT NOT NULL REFERENCES learners(id),
    stage INTEGER NOT NULL DEFAULT 0, reviews INTEGER NOT NULL DEFAULT 0,
    lapses INTEGER NOT NULL DEFAULT 0, last_recall TEXT, last_review_at TEXT,
    due_at TEXT NOT NULL, interval_days INTEGER NOT NULL DEFAULT 0,
    version INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS schedule_due ON review_schedule(user_id, due_at);
CREATE TABLE IF NOT EXISTS operations (
    user_id TEXT NOT NULL REFERENCES learners(id), kind TEXT NOT NULL,
    request_id TEXT NOT NULL, fingerprint TEXT NOT NULL, payload_json TEXT NOT NULL,
    card_id TEXT REFERENCES cards(id), state TEXT NOT NULL,
    lease_until TEXT NOT NULL, lease_token TEXT NOT NULL, base_schedule_json TEXT,
    result_json TEXT, error_code TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, ordinal BIGSERIAL,
    PRIMARY KEY(user_id, kind, request_id)
);
CREATE TABLE IF NOT EXISTS review_events (
    id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES learners(id),
    request_id TEXT NOT NULL, card_id TEXT NOT NULL REFERENCES cards(id),
    student_answer TEXT NOT NULL, grade TEXT NOT NULL, feedback_json TEXT NOT NULL,
    self_recall TEXT, before_json TEXT NOT NULL, result_json TEXT NOT NULL,
    model TEXT, usage_json TEXT NOT NULL, created_at TEXT NOT NULL, ordinal BIGSERIAL,
    UNIQUE(user_id, request_id)
);
CREATE INDEX IF NOT EXISTS events_card ON review_events(user_id, card_id, created_at);
CREATE TABLE IF NOT EXISTS study_sessions (
    id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES learners(id),
    local_date TEXT NOT NULL, created_at TEXT NOT NULL, UNIQUE(user_id, local_date)
);
CREATE TABLE IF NOT EXISTS daily_assignments (
    session_id TEXT NOT NULL REFERENCES study_sessions(id), card_id TEXT NOT NULL REFERENCES cards(id),
    position INTEGER NOT NULL, PRIMARY KEY(session_id, card_id), UNIQUE(session_id, position)
);
CREATE TABLE IF NOT EXISTS daily_usage (
    user_id TEXT NOT NULL REFERENCES learners(id), local_date TEXT NOT NULL,
    kind TEXT NOT NULL, calls INTEGER NOT NULL, PRIMARY KEY(user_id, local_date, kind)
);
CREATE TABLE IF NOT EXISTS provider_runs (
    id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES learners(id),
    kind TEXT NOT NULL, request_id TEXT NOT NULL, model TEXT,
    trace_json TEXT NOT NULL, error_code TEXT, created_at TEXT NOT NULL
);
CREATE TABLE rate_buckets (
    bucket_key TEXT PRIMARY KEY, window_start INTEGER NOT NULL, calls INTEGER NOT NULL
);
CREATE TABLE ai_leases (
    id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES learners(id), expires_at TEXT NOT NULL
);
CREATE INDEX ai_lease_expiry ON ai_leases(expires_at);
CREATE TABLE global_usage (
    local_date TEXT PRIMARY KEY, calls INTEGER NOT NULL
);

INSERT INTO schema_version VALUES (2) ON CONFLICT DO NOTHING;
ALTER TABLE learners ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON learners USING (id=current_setting('app.user_id', true)) WITH CHECK (id=current_setting('app.user_id', true));
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON cards USING (user_id=current_setting('app.user_id', true)) WITH CHECK (user_id=current_setting('app.user_id', true));
ALTER TABLE review_schedule ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON review_schedule USING (user_id=current_setting('app.user_id', true)) WITH CHECK (user_id=current_setting('app.user_id', true));
ALTER TABLE operations ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON operations USING (user_id=current_setting('app.user_id', true)) WITH CHECK (user_id=current_setting('app.user_id', true));
ALTER TABLE review_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON review_events USING (user_id=current_setting('app.user_id', true)) WITH CHECK (user_id=current_setting('app.user_id', true));
ALTER TABLE study_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON study_sessions USING (user_id=current_setting('app.user_id', true)) WITH CHECK (user_id=current_setting('app.user_id', true));
ALTER TABLE daily_usage ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON daily_usage USING (user_id=current_setting('app.user_id', true)) WITH CHECK (user_id=current_setting('app.user_id', true));
ALTER TABLE provider_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON provider_runs USING (user_id=current_setting('app.user_id', true)) WITH CHECK (user_id=current_setting('app.user_id', true));
ALTER TABLE card_evidence ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON card_evidence USING (EXISTS (SELECT 1 FROM cards WHERE cards.id=card_id AND user_id=current_setting('app.user_id', true)));
ALTER TABLE daily_assignments ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_access ON daily_assignments USING (EXISTS (SELECT 1 FROM study_sessions WHERE study_sessions.id=session_id AND user_id=current_setting('app.user_id', true)) AND EXISTS (SELECT 1 FROM cards WHERE cards.id=card_id AND user_id=current_setting('app.user_id', true)));
REVOKE ALL ON ALL TABLES IN SCHEMA devmind FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA devmind FROM PUBLIC;
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname='anon') THEN
        REVOKE ALL ON SCHEMA devmind FROM anon;
        REVOKE ALL ON ALL TABLES IN SCHEMA devmind FROM anon;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname='authenticated') THEN
        REVOKE ALL ON SCHEMA devmind FROM authenticated;
        REVOKE ALL ON ALL TABLES IN SCHEMA devmind FROM authenticated;
    END IF;
END $$;
