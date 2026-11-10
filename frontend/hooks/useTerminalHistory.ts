"use client";

import { useCallback, useRef, useState } from "react";

/**
 * Histórico de comandos tipo shell: ↑/↓ navegam por entradas anteriores,
 * qualquer edição reinicia a navegação para o final do histórico.
 */
export function useTerminalHistory() {
  const [history, setHistory] = useState<string[]>([]);
  const cursorRef = useRef<number | null>(null); // null = fora do histórico (input livre)
  const draftRef = useRef<string>("");

  const push = useCallback((entry: string) => {
    if (!entry.trim()) return;
    setHistory((prev) => [...prev, entry]);
    cursorRef.current = null;
    draftRef.current = "";
  }, []);

  const previous = useCallback(
    (currentValue: string): string | null => {
      if (history.length === 0) return null;
      if (cursorRef.current === null) {
        draftRef.current = currentValue;
        cursorRef.current = history.length - 1;
      } else if (cursorRef.current > 0) {
        cursorRef.current -= 1;
      }
      return history[cursorRef.current];
    },
    [history]
  );

  const next = useCallback(
    (): string | null => {
      if (cursorRef.current === null) return null;
      if (cursorRef.current >= history.length - 1) {
        cursorRef.current = null;
        return draftRef.current;
      }
      cursorRef.current += 1;
      return history[cursorRef.current];
    },
    [history]
  );

  const reset = useCallback(() => {
    cursorRef.current = null;
    draftRef.current = "";
  }, []);

  return { history, push, previous, next, reset };
}
