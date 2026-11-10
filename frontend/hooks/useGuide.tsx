"use client";

import { useEffect, useRef, useState } from "react";
import { ApiError, getGuide } from "@/lib/api";
import type { GuideModule } from "@/lib/types";

type GuideState =
  | { status: "loading"; modules: null; error: null }
  | { status: "ready"; modules: GuideModule[]; error: null }
  | { status: "error"; modules: null; error: string };

/**
 * Carrega a estrutura de GUIDE (`GET /guide`) uma única vez e a mantém em
 * cache em memória durante a vida do módulo: não requer Pinecone/OpenAI e não
 * muda entre renders, então não é necessário revalidar por polling.
 */
let cache: GuideModule[] | null = null;

export function useGuide(): GuideState {
  const [state, setState] = useState<GuideState>(
    cache ? { status: "ready", modules: cache, error: null } : { status: "loading", modules: null, error: null }
  );
  const requested = useRef(cache !== null);

  useEffect(() => {
    if (requested.current) return;
    requested.current = true;
    getGuide()
      .then((modules) => {
        cache = modules;
        setState({ status: "ready", modules, error: null });
      })
      .catch((error) => {
        const message = error instanceof ApiError ? error.message : "Não foi possível carregar a guia.";
        setState({ status: "error", modules: null, error: message });
      });
  }, []);

  return state;
}
