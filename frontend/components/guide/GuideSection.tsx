"use client";

import type { GuideModule, GuideSection as GuideSectionType } from "@/lib/types";

type GuideSectionProps = {
  module: GuideModule;
  section: GuideSectionType;
  onSelectDocument: (documentId: string) => void;
  onAskAboutTopic: () => void;
};

/** "Recommended order": documentos de uma seção na ordem real do curso. */
export function GuideSection({ module, section, onSelectDocument, onAskAboutTopic }: GuideSectionProps) {
  return (
    <div>
      <div className="flex items-center justify-between gap-3 mb-3">
        <p className="text-xs tracking-widest text-accent">{section.title.toUpperCase()}</p>
        <button
          type="button"
          onClick={onAskAboutTopic}
          className="text-[11px] tracking-widest px-2.5 py-1 border border-border rounded-full text-muted hover:text-accent hover:border-border-strong transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent"
        >
          ASK ABOUT THIS TOPIC
        </button>
      </div>
      <p className="text-xs text-muted mb-2">Recommended order</p>
      <ul className="flex flex-col gap-1">
        {section.documents.map((document, index) => (
          <li key={document.id}>
            <button
              type="button"
              onClick={() => onSelectDocument(document.id)}
              className="w-full flex items-center gap-3 text-left text-sm text-foreground rounded-sm py-1 hover:text-accent transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent"
            >
              <span className="text-muted">{String(index + 1).padStart(2, "0")}</span>
              <span className="truncate">{document.title}</span>
            </button>
          </li>
        ))}
      </ul>
      <p className="text-xs text-muted mt-3">{module.title}</p>
    </div>
  );
}
