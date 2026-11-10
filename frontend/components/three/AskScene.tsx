"use client";

import type { RetrievalStatus } from "@/hooks/useKnowledge";
import { QueryCore } from "./QueryCore";

/**
 * Conteúdo 3D específico de ASK: o nó da pergunta ativa (`QueryCore`),
 * que pulsa enquanto busca e fica estável com os resultados. Grid/Stars/
 * Particles/CameraRig são compartilhados por `Scene.tsx`.
 */
export function AskScene({ status, paused = false }: { status: RetrievalStatus; paused?: boolean }) {
  return <QueryCore status={status} paused={paused} />;
}
