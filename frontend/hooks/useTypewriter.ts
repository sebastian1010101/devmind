"use client";

import { useEffect, useState } from "react";

const CHARS_PER_TICK = 3;
const TICK_MS = 16;

function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/**
 * Revela `text` progressivamente (efeito "typewriter"). O backend não
 * suporta streaming real (`rag.py::answer_question` não usa `stream=True`,
 * `/ask` devolve o JSON completo de uma só vez) — isto simula a
 * sensação de escrita sobre uma resposta que já chegou completa,
 * puramente no cliente.
 *
 * Tira um snapshot de `text` ao montar e anima uma única vez: se `text`
 * mudar depois, é ignorado (o mesmo componente não se reutiliza para
 * animar uma segunda resposta; ver AnimatedAnswer.tsx, que monta uma
 * instância nova por resposta). Respeita `prefers-reduced-motion`
 * mostrando o texto completo de imediato.
 *
 * `speed` escala a velocidade padrão (1 = velocidade normal, 0.5 = o
 * dobro mais lento, etc.) — útil para animações mais pausadas como o
 * título do header (ver AnimatedTitle.tsx).
 */
export function useTypewriter(text: string, speed = 1): { display: string; done: boolean } {
  const [target] = useState(text);
  const [length, setLength] = useState(() => (prefersReducedMotion() ? target.length : 0));

  useEffect(() => {
    if (prefersReducedMotion() || target.length === 0) return;

    const tickMs = TICK_MS / speed;
    let current = 0;
    let lastTick = performance.now();
    let raf = 0;

    const step = (now: number) => {
      if (now - lastTick >= tickMs) {
        lastTick = now;
        current = Math.min(target.length, current + CHARS_PER_TICK);
        setLength(current);
      }
      if (current < target.length) {
        raf = requestAnimationFrame(step);
      }
    };

    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [target, speed]);

  return { display: target.slice(0, length), done: length >= target.length };
}
