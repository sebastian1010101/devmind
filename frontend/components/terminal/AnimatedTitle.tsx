"use client";

import { useTypewriter } from "@/hooks/useTypewriter";

/**
 * Título do header com efeito typewriter (mesmo hook usado por
 * `AnimatedAnswer` para as respostas). O texto é escrito uma única vez
 * ao montar; o cursor continua piscando indefinidamente depois.
 */
export function AnimatedTitle({ text }: { text: string }) {
  const { display } = useTypewriter(text, 0.5);

  return (
    <h1 className="text-sm tracking-[0.2em] text-foreground">
      {display}
      <span className="animate-caret-blink text-foreground" aria-hidden="true">
        _
      </span>
    </h1>
  );
}
