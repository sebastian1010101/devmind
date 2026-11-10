"use client";

import { forwardRef, useMemo, useState, type FormEvent, type KeyboardEvent } from "react";
import { useTerminalHistory } from "@/hooks/useTerminalHistory";
import { KNOWN_COMMANDS } from "@/lib/commands";

type CommandInputProps = {
  onSubmit: (value: string) => void;
  placeholder?: string;
};

/** Sugestão de autocompletar: apenas quando o valor é um prefixo `/algo`
 * sem espaços que corresponde exatamente a um único comando conhecido. */
function suggestCommand(value: string): string | null {
  if (!value.startsWith("/") || value.includes(" ") || value.length < 2) return null;
  const matches = KNOWN_COMMANDS.filter((cmd) => cmd.startsWith(value) && cmd !== value);
  return matches.length === 1 ? matches[0] : null;
}

export const CommandInput = forwardRef<HTMLInputElement, CommandInputProps>(function CommandInput(
  { onSubmit, placeholder },
  ref
) {
  const [value, setValue] = useState("");
  const { push, previous, next, reset } = useTerminalHistory();
  const suggestion = useMemo(() => suggestCommand(value), [value]);

  const acceptSuggestion = () => {
    if (!suggestion) return false;
    setValue(`${suggestion} `);
    return true;
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Tab") {
      if (acceptSuggestion()) event.preventDefault();
      return;
    }
    if (event.key === "ArrowRight" && suggestion && event.currentTarget.selectionStart === value.length) {
      event.preventDefault();
      acceptSuggestion();
      return;
    }
    if (event.key === "ArrowUp") {
      const prev = previous(value);
      if (prev !== null) {
        event.preventDefault();
        setValue(prev);
      }
      return;
    }
    if (event.key === "ArrowDown") {
      const upcoming = next();
      if (upcoming !== null) {
        event.preventDefault();
        setValue(upcoming);
      }
      return;
    }
    if (event.key === "Escape") {
      setValue("");
      reset();
    }
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) return;
    push(trimmed);
    onSubmit(trimmed);
    setValue("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 sm:gap-3">
      <div className="relative flex-1 min-w-0">
        {suggestion && (
          <div className="absolute inset-0 flex items-center px-2 text-base pointer-events-none whitespace-pre" aria-hidden="true">
            <span className="invisible">{value}</span>
            <span className="text-muted">{suggestion.slice(value.length)}</span>
            <span className="text-muted"> ↹</span>
          </div>
        )}
        <input
          ref={ref}
          type="text"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder ?? "Escreva sua pergunta…"}
          aria-label="Sua pergunta"
          aria-autocomplete="inline"
          maxLength={1205}
          autoComplete="off"
          spellCheck={false}
          className="relative w-full rounded-md bg-transparent px-2 py-2 text-base text-foreground placeholder:text-muted focus-visible:outline-accent"
        />
      </div>
      <button
        type="submit"
        disabled={!value.trim()}
        className="rounded-lg bg-accent px-3 py-2 text-sm font-semibold text-[#0b1330] hover:bg-[#a3b7ff] focus-visible:outline-accent disabled:opacity-60"
      >
        Enviar
      </button>
    </form>
  );
});
