export type Mode = "ask" | "guide" | "study";

/** Scope opcional de GUIDE aplicado a uma pergunta de ASK ("Ask about this
 * topic/document"): restringe o retrieval via `filter` de Pinecone no
 * backend (ver `rag.py::build_scope_filter`). */
export type AskScope = {
  module: string;
  moduleTitle: string;
  topic?: string;
  topicTitle?: string;
  source?: string;
  documentTitle?: string;
};

export type AskRequest = {
  question: string;
  top_k?: number;
  module?: string;
  topic?: string;
  source?: string;
};

export type Source = {
  source: string;
  section: string;
  excerpt: string;
  chunk_id: number | null;
  score: number;
};

export type AskResponse = {
  status: "answered" | "insufficient_evidence";
  answer: string;
  sources: Source[];
};

export type StatsResponse = {
  documents_discovered: number;
  documents_indexed: number;
  failed: number;
  empty: number;
  duplicates: number;
  chunks_created: number;
  avg_chunks_per_document: number;
  min_chunk_length: number;
  max_chunk_length: number;
  avg_chunk_length: number;
};

export type HealthResponse = {
  status: string;
};

/**
 * Hierarquia de navegação de GUIDE (espelho de `guide.py`): Module -> Section
 * -> Document. Gerada deterministicamente a partir de `knowledge/` pelo
 * backend — GUIDE não faz queries vetoriais no Pinecone.
 */
export type GuideDocument = {
  id: string;
  title: string;
  source: string;
  order: number;
  topic: string | null;
};

export type GuideSection = {
  id: string;
  title: string;
  order: number;
  documents: GuideDocument[];
};

export type GuideModule = {
  id: string;
  title: string;
  order: number;
  sections: GuideSection[];
};

/** Rota de navegação ativa dentro de GUIDE (para breadcrumbs e R3F). */
export type GuidePath = {
  moduleId?: string;
  sectionId?: string;
  documentId?: string;
};

export type Recall = "again" | "hard" | "good" | "easy";
export type ReviewSchedule = {
  stage: number; reviews: number; lapses: number; last_recall: Recall | null;
  due_at: string; last_review_at: string | null; interval_days: number; version: number;
};
export type LearningSource = {
  evidence_id: string; source: string; section: string; chunk_id: number | null;
  text_sha256: string; chunk_text?: string; source_changed?: boolean;
};
export type ReviewResult = {
  review_id: string; grade: "correct" | "partial" | "incorrect" | "ungradable";
  feedback: string; present_concepts: string[]; missing_concepts: string[]; errors: string[];
  reference_answer: string; explanation: string; sources: LearningSource[];
  schedule: ReviewSchedule; self_recall: Recall | null; notice: string;
};
export type StudyCard = {
  id: string; question: string; module: string; topic: string | null;
  learning_state: "new" | "due" | "scheduled";
  difficulty: "easy" | "medium" | "hard"; schedule: ReviewSchedule;
  sources: LearningSource[]; completed?: boolean;
  latest_attempt?: { request_id: string; answer: string; state: string; result: ReviewResult | null } | null;
};
export type DailySession = {
  id: string; local_date: string; cards: StudyCard[]; completed: number; total: number;
};
export type LearningProgress = {
  total: number; due: number; reviewed: number; new: number; attempts: number; correct: number; graded: number;
  topics: { module: string; topic: string | null; total: number; reviewed: number; due: number }[];
  upcoming: { id: string; question: string; due_at: string }[];
  usage: Record<string, { used: number; limit: number }>; local_date: string;
};
export type GenerateCardsRequest = {
  request_id: string; module: string; topic?: string; source?: string; focus: string; count: number;
};
