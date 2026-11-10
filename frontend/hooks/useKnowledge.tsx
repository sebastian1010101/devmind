"use client";

import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { GuidePath, Mode, Source } from "@/lib/types";

export type RetrievalStatus = "idle" | "searching" | "results" | "error";

type RetrievalState = {
  status: RetrievalStatus;
  sources: Source[];
};

type KnowledgeContextValue = RetrievalState & {
  mode: Mode;
  guidePath: GuidePath;
  startSearch: () => void;
  setResults: (sources: Source[]) => void;
  setError: () => void;
  reset: () => void;
  setMode: (mode: Mode) => void;
  setGuidePath: (path: GuidePath) => void;
};

const KnowledgeContext = createContext<KnowledgeContextValue | null>(null);

const INITIAL_STATE: RetrievalState = { status: "idle", sources: [] };

/**
 * Ponte entre o fluxo do Terminal (modo ativo, `/ask`, navegação de
 * GUIDE) e a cena 3D (Scene / AskScene / GuideScene): um estado
 * compartilhado via Context, sem necessidade de uma biblioteca de estado externa.
 */
export function KnowledgeProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<RetrievalState>(INITIAL_STATE);
  const [mode, setMode] = useState<Mode>("ask");
  const [guidePath, setGuidePath] = useState<GuidePath>({});

  const value = useMemo<KnowledgeContextValue>(
    () => ({
      ...state,
      mode,
      guidePath,
      startSearch: () => setState({ status: "searching", sources: [] }),
      setResults: (sources: Source[]) => setState({ status: "results", sources }),
      setError: () => setState((prev) => ({ status: "error", sources: prev.sources })),
      reset: () => setState(INITIAL_STATE),
      setMode,
      setGuidePath,
    }),
    [state, mode, guidePath]
  );

  return <KnowledgeContext.Provider value={value}>{children}</KnowledgeContext.Provider>;
}

export function useKnowledge() {
  const ctx = useContext(KnowledgeContext);
  if (!ctx) {
    throw new Error("useKnowledge deve ser usado dentro de <KnowledgeProvider>.");
  }
  return ctx;
}
