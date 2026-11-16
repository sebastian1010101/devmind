"use client";

import type { Mode } from "@/lib/types";

const MODES: { id: Mode; label: string }[] = [
  { id: "ask", label: "Chat" },
  { id: "guide", label: "Guia" },
  { id: "study", label: "Estudo" },
];

type ModeSelectorProps = {
  activeMode: Mode;
  onSelect: (mode: Mode) => void;
};

export function ModeSelector({ activeMode, onSelect }: ModeSelectorProps) {
  return (
    <div role="group" aria-label="Modo ativo" className="flex flex-wrap gap-2">
      {MODES.map(({ id, label }) => {
        const isActive = id === activeMode;
        return (
          <button
            key={id}
            type="button"
            aria-pressed={isActive}
            onClick={() => onSelect(id)}
            className={`px-4 py-1.5 text-xs font-medium border rounded-full transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent ${
              isActive
                ? "border-accent text-accent border-glow"
                : "border-border text-muted hover:text-foreground hover:border-border-strong"
            }`}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
