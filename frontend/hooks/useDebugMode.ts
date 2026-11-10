"use client";

import { useSyncExternalStore } from "react";

function subscribe() {
  // A URL não muda sem uma navegação completa da página, então não
  // há um evento externo no qual se inscrever: no-op com cleanup vazio.
  return () => {};
}

function getSnapshot(): boolean {
  return new URLSearchParams(window.location.search).get("debug") === "true";
}

function getServerSnapshot(): boolean {
  return false;
}

/**
 * Ativa o modo debug com `?debug=true` na URL. Usa
 * `useSyncExternalStore` (em vez de `useState` + `useEffect`) para ler um
 * valor que só existe no cliente sem produzir um mismatch de
 * hidratação entre o HTML renderizado no servidor e o primeiro render
 * do cliente.
 */
export function useDebugMode(): boolean {
  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}
