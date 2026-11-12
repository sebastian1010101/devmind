import type {
  AskRequest,
  AskResponse,
  AskScope,
  GuideModule,
  HealthResponse,
  StatsResponse,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    const timeout = AbortSignal.timeout(90_000);
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
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

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const message = typeof data?.detail === "string" ? data.detail : "Não foi possível concluir a consulta.";
    throw new ApiError(message, response.status);
  }

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
