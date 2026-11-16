CREATE TABLE IF NOT EXISTS learners (
    id TEXT PRIMARY KEY, timezone TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cards (
    id TEXT PRIMARY KEY, learner_id TEXT NOT NULL REFERENCES learners(id),
    module TEXT NOT NULL, topic TEXT, question TEXT NOT NULL,
    question_key TEXT NOT NULL, reference_answer TEXT NOT NULL,
    explanation TEXT NOT NULL, concepts_json TEXT NOT NULL, difficulty TEXT NOT NULL,
    model TEXT NOT NULL, prompt_version TEXT NOT NULL, created_at TEXT NOT NULL,
    UNIQUE(learner_id, module, question_key)
);
CREATE TABLE IF NOT EXISTS card_evidence (
    card_id TEXT NOT NULL REFERENCES cards(id), evidence_id TEXT NOT NULL,
    source TEXT NOT NULL, section TEXT NOT NULL, chunk_id INTEGER,
    chunk_text TEXT NOT NULL, text_sha256 TEXT NOT NULL,
    index_name TEXT NOT NULL, namespace TEXT NOT NULL, score REAL NOT NULL,
    PRIMARY KEY(card_id, evidence_id)
);
CREATE TABLE IF NOT EXISTS review_schedule (
    card_id TEXT PRIMARY KEY REFERENCES cards(id), learner_id TEXT NOT NULL REFERENCES learners(id),
    stage INTEGER NOT NULL DEFAULT 0, reviews INTEGER NOT NULL DEFAULT 0,
    lapses INTEGER NOT NULL DEFAULT 0, last_recall TEXT, last_review_at TEXT,
    due_at TEXT NOT NULL, interval_days INTEGER NOT NULL DEFAULT 0,
    version INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS schedule_due ON review_schedule(learner_id, due_at);
CREATE TABLE IF NOT EXISTS operations (
    learner_id TEXT NOT NULL REFERENCES learners(id), kind TEXT NOT NULL,
    request_id TEXT NOT NULL, fingerprint TEXT NOT NULL, payload_json TEXT NOT NULL,
    card_id TEXT REFERENCES cards(id), state TEXT NOT NULL,
    lease_until TEXT NOT NULL, lease_token TEXT NOT NULL, base_schedule_json TEXT,
    result_json TEXT, error_code TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
    PRIMARY KEY(learner_id, kind, request_id)
);
CREATE TABLE IF NOT EXISTS review_events (
    id TEXT PRIMARY KEY, learner_id TEXT NOT NULL REFERENCES learners(id),
    request_id TEXT NOT NULL, card_id TEXT NOT NULL REFERENCES cards(id),
    student_answer TEXT NOT NULL, grade TEXT NOT NULL, feedback_json TEXT NOT NULL,
    self_recall TEXT, before_json TEXT NOT NULL, result_json TEXT NOT NULL,
    model TEXT, usage_json TEXT NOT NULL, created_at TEXT NOT NULL,
    UNIQUE(learner_id, request_id)
);
CREATE INDEX IF NOT EXISTS events_card ON review_events(learner_id, card_id, created_at);
CREATE TABLE IF NOT EXISTS study_sessions (
    id TEXT PRIMARY KEY, learner_id TEXT NOT NULL REFERENCES learners(id),
    local_date TEXT NOT NULL, created_at TEXT NOT NULL, UNIQUE(learner_id, local_date)
);
CREATE TABLE IF NOT EXISTS daily_assignments (
    session_id TEXT NOT NULL REFERENCES study_sessions(id), card_id TEXT NOT NULL REFERENCES cards(id),
    position INTEGER NOT NULL, PRIMARY KEY(session_id, card_id), UNIQUE(session_id, position)
);
CREATE TABLE IF NOT EXISTS daily_usage (
    learner_id TEXT NOT NULL REFERENCES learners(id), local_date TEXT NOT NULL,
    kind TEXT NOT NULL, calls INTEGER NOT NULL, PRIMARY KEY(learner_id, local_date, kind)
);
CREATE TABLE IF NOT EXISTS provider_runs (
    id TEXT PRIMARY KEY, learner_id TEXT NOT NULL REFERENCES learners(id),
    kind TEXT NOT NULL, request_id TEXT NOT NULL, model TEXT,
    trace_json TEXT NOT NULL, error_code TEXT, created_at TEXT NOT NULL
);
