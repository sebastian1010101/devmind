export type Mode = "ask" | "guide";

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
