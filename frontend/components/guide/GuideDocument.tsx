"use client";

import { useEffect, useState } from "react";
import { MarkdownContent } from "@/components/MarkdownContent";
import { ApiError, getGuideDocument } from "@/lib/api";
import type { GuideDocument as GuideDocumentType, GuideModule, GuideSection } from "@/lib/types";

type GuideDocumentProps = {
  module: GuideModule;
  section: GuideSection;
  doc: GuideDocumentType;
  onAskAboutDocument: () => void;
};

type DocumentState =
  | { status: "loading" }
  | { status: "ready"; markdown: string }
  | { status: "error"; message: string };

export function GuideDocument({ module, section, doc, onAskAboutDocument }: GuideDocumentProps) {
  const [state, setState] = useState<DocumentState>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    getGuideDocument(doc.source, controller.signal)
      .then((markdown) => {
        if (!controller.signal.aborted) setState({ status: "ready", markdown });
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        const message = error instanceof ApiError ? error.message : "Não foi possível carregar o documento.";
        setState({ status: "error", message });
      });
    return () => controller.abort();
  }, [doc.source, attempt]);

  function retry() {
    setState({ status: "loading" });
    setAttempt((previous) => previous + 1);
  }

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
      <article aria-label={doc.title} className="mt-5 min-w-0 border-t border-border pt-4">
        {state.status === "loading" && <p role="status" className="text-muted">Carregando documento…</p>}
        {state.status === "error" && (
          <>
            <p role="alert" className="text-danger">{state.message}</p>
            <button
              type="button"
              onClick={retry}
              className="mt-2 rounded-sm text-accent underline focus-visible:outline-accent"
            >
              Tentar novamente
            </button>
          </>
        )}
        {state.status === "ready" && <MarkdownContent content={state.markdown} variant="document" />}
      </article>
    </div>
  );
}
