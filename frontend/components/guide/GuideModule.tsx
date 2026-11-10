"use client";

import type { GuideModule as GuideModuleType } from "@/lib/types";

type GuideModuleProps = {
  module: GuideModuleType;
  onSelectSection: (sectionId: string) => void;
};

/** Lista de seções (temas) dentro de um módulo. */
export function GuideModule({ module, onSelectSection }: GuideModuleProps) {
  return (
    <div>
      <p className="text-xs tracking-widest text-accent mb-3">{module.title.toUpperCase()}</p>
      <ul className="flex flex-col gap-1">
        {module.sections.map((section, index) => (
          <li key={section.id}>
            <button
              type="button"
              onClick={() => onSelectSection(section.id)}
              className="w-full flex items-center gap-3 text-left text-sm text-foreground rounded-sm py-1 hover:text-accent transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent"
            >
              <span className="text-muted">{String(index + 1).padStart(2, "0")}</span>
              <span>{section.title}</span>
              <span className="text-muted text-xs ml-auto">{section.documents.length} docs</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
