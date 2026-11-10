"use client";

import type { GuideModule } from "@/lib/types";

type GuideHomeProps = {
  modules: GuideModule[];
  onSelectModule: (moduleId: string) => void;
};

/** Vista raiz de GUIDE: lista de módulos em ordem pedagógica. */
export function GuideHome({ modules, onSelectModule }: GuideHomeProps) {
  return (
    <div>
      <p className="text-xs tracking-widest text-accent mb-3">KNOWLEDGE GUIDE</p>
      <ul className="flex flex-col gap-1">
        {modules.map((module) => (
          <li key={module.id}>
            <button
              type="button"
              onClick={() => onSelectModule(module.id)}
              className="w-full flex items-center gap-3 text-left text-sm text-foreground rounded-sm py-1 hover:text-accent transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent"
            >
              <span className="text-muted">{String(module.order).padStart(2, "0")}</span>
              <span>{module.title}</span>
              <span className="text-muted text-xs ml-auto">{module.sections.length} sections</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
