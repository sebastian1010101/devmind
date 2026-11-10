"use client";

import { useTypewriter } from "@/hooks/useTypewriter";
import { Answer } from "./Answer";

/**
 * Envolve `Answer` com o efeito typewriter. Montada uma única vez por
 * resposta (ver TerminalEntry.tsx: a entrada `answer` não volta a ser
 * substituída após ser criada), então a animação roda uma vez e não se
 * reinicia em renders posteriores do log.
 *
 * Enquanto escreve, mostra texto plano (`whitespace-pre-wrap`): passar
 * Markdown incompleto ao react-markdown produziria renders intermediários
 * quebrados (um fence ``` sem fechar engoliria tudo o que vem depois). Ao
 * terminar, monta `Answer`, que renderiza o Markdown já completo.
 */
export function AnimatedAnswer({ content }: { content: string }) {
  const { display, done } = useTypewriter(content);

  if (!done) {
    return (
      <p className="whitespace-pre-wrap break-words text-sm text-foreground leading-relaxed">
        {display}
        <span className="animate-caret-blink text-accent" aria-hidden="true">
          ▍
        </span>
      </p>
    );
  }

  return <Answer content={content} />;
}
