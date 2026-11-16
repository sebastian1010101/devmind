-- Existing local-demo data keeps its owner. Accounts start with an empty library.
ALTER TABLE cards RENAME COLUMN learner_id TO user_id;
ALTER TABLE review_schedule RENAME COLUMN learner_id TO user_id;
ALTER TABLE operations RENAME COLUMN learner_id TO user_id;
ALTER TABLE review_events RENAME COLUMN learner_id TO user_id;
ALTER TABLE study_sessions RENAME COLUMN learner_id TO user_id;
ALTER TABLE daily_usage RENAME COLUMN learner_id TO user_id;
ALTER TABLE provider_runs RENAME COLUMN learner_id TO user_id;
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
