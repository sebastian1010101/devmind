import type {
  AskRequest,
  AskResponse,
  AskScope,
  GuideModule,
  HealthResponse,
  StatsResponse,
  StudyCard, DailySession, LearningProgress, GenerateCardsRequest, ReviewResult, Recall,
} from "./types";

const API_BASE_URL = "/api";

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export const learningApi = {
  progress: () => request<LearningProgress>("/learning/progress"),
  due: () => request<{ cards: StudyCard[] }>("/learning/due?limit=20"),
  daily: () => request<DailySession>("/learning/daily"),
  card: (id: string) => request<StudyCard>(`/learning/cards/${encodeURIComponent(id)}`),
  generate: (body: GenerateCardsRequest) => request<{ cards: StudyCard[] }>("/learning/cards", {
    method: "POST", body: JSON.stringify(body),
  }),
  review: (id: string, requestId: string, answer: string) => request<ReviewResult>(`/learning/cards/${encodeURIComponent(id)}/reviews`, {
    method: "POST", body: JSON.stringify({ request_id: requestId, answer }),
  }),
  recall: (id: string, recall: Recall) => request<ReviewResult>(`/learning/reviews/${encodeURIComponent(id)}/recall`, {
    method: "POST", body: JSON.stringify({ recall }),
  }),
};

async function request<T>(path: string, init?: RequestInit, retry = true): Promise<T> {
  let response: Response;
  try {
    const timeout = AbortSignal.timeout(90_000);
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", "X-DevMind-CSRF": "1", ...init?.headers },
      credentials: "same-origin",
      cache: "no-store",
      signal: init?.signal ? AbortSignal.any([init.signal, timeout]) : timeout,
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "TimeoutError") {
      throw new ApiError("A consulta demorou a responder. Tente novamente.");
    }
    throw new ApiError(
      `Não foi possível conectar à API em ${API_BASE_URL}. O \`uvicorn api:app\` está rodando?`
    );
  }

  if (response.status === 401 && retry && path !== "/auth/refresh" && !path.startsWith("/auth/login")) {
    try {
      refreshPromise ??= request("/auth/refresh", { method: "POST" }, false).finally(() => { refreshPromise = null; });
      await refreshPromise;
      return request<T>(path, init, false);
    } catch {
      if (typeof window !== "undefined" && window.location.pathname.startsWith("/dashboard")) {
        navigateWithFreshSession("/entrar?sessao=expirada");
      }
      throw new ApiError("Sua sessão expirou. Entre novamente para recuperar seu progresso.", 401);
    }
  }
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const message = typeof data?.detail === "string" ? data.detail : "Não foi possível concluir a consulta.";
    throw new ApiError(message, response.status);
  }

  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export async function askQuestion(question: string, topK?: number, scope?: AskScope | null) {
  const body: AskRequest = {
    question,
    ...(topK ? { top_k: topK } : {}),
    ...(scope ? { module: scope.module, topic: scope.topic, source: scope.source } : {}),
  };
  const started = performance.now();
  const result = await request<AskResponse>("/ask", {
    method: "POST",
    body: JSON.stringify(body),
  });
  return { ...result, latencyMs: Math.round(performance.now() - started) };
}

export function getStats(): Promise<StatsResponse> {
  return request<StatsResponse>("/stats");
}

export function getGuide(): Promise<GuideModule[]> {
  return request<GuideModule[]>("/guide");
}

export async function getGuideDocument(source: string, signal: AbortSignal): Promise<string> {
  const query = new URLSearchParams({ source });
  const { markdown } = await request<{ markdown: string }>(`/guide/document?${query}`, { signal });
  return markdown;
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

let refreshPromise: Promise<unknown> | null = null;

export function clearStudyDrafts() {
  try {
    for (const storage of [localStorage, sessionStorage]) {
      for (const key of Object.keys(storage)) {
        if (key.startsWith("devmind:")) storage.removeItem(key);
      }
    }
  } catch { /* Submitted answers remain on the server. */ }
}

export function authApi(action: string, body?: object) {
  return request<{ id?: string; email?: string; message?: string }>(`/auth/${action}`, {
    method: action === "me" ? "GET" : "POST",
    ...(body ? { body: JSON.stringify(body) } : {}),
  }, action === "me");
}

let sessionChannel: BroadcastChannel | null = null;

export function sessionEvents() {
  if (typeof window === "undefined" || !("BroadcastChannel" in window)) return null;
  try {
    sessionChannel ??= new BroadcastChannel("devmind-session");
    return sessionChannel;
  } catch {
    return null;
  }
}

// Sharing one channel per document prevents the originating tab from reloading itself.
export function navigateWithFreshSession(path: string) {
  sessionEvents()?.postMessage("changed");
  window.location.replace(new URL(path, window.location.origin).href);
}
