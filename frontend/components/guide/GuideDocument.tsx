"use client";

import type { GuideDocument as GuideDocumentType, GuideModule, GuideSection } from "@/lib/types";

type GuideDocumentProps = {
  module: GuideModule;
  section: GuideSection;
  doc: GuideDocumentType;
  onAskAboutDocument: () => void;
};

/** Detalhe de um documento dentro de GUIDE. Não carrega o conteúdo completo
 * do arquivo — apenas a metadata já disponível na estrutura de GUIDE. */
export function GuideDocument({ module, section, doc, onAskAboutDocument }: GuideDocumentProps) {
  return (
    <div>
      <p className="text-xs tracking-widest text-accent mb-3">DOCUMENT</p>
      <p className="text-base text-foreground mb-4">{doc.title}</p>
      <dl className="flex flex-col gap-1.5 text-sm mb-5">
        <div className="flex gap-2">
          <dt className="text-muted w-24 shrink-0">Module:</dt>
          <dd className="text-foreground">{module.title}</dd>
        </div>
        <div className="flex gap-2">
          <dt className="text-muted w-24 shrink-0">Section:</dt>
          <dd className="text-foreground">{section.title}</dd>
        </div>
        <div className="flex gap-2">
          <dt className="text-muted w-24 shrink-0">Source:</dt>
          <dd className="text-foreground min-w-0 wrap-anywhere">{doc.source}</dd>
        </div>
      </dl>
      <button
        type="button"
        onClick={onAskAboutDocument}
        className="text-[11px] tracking-widest px-3 py-1.5 border border-accent text-accent rounded-full hover:border-glow transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent"
      >
        ASK ABOUT THIS DOCUMENT
      </button>
    </div>
  );
}
