"use client";

import { useGuide } from "@/hooks/useGuide";
import type { AskScope, GuidePath } from "@/lib/types";
import { GuideBreadcrumbs } from "./GuideBreadcrumbs";
import { GuideDocument } from "./GuideDocument";
import { GuideHome } from "./GuideHome";
import { GuideModule } from "./GuideModule";
import { GuideSection } from "./GuideSection";

type GuideProps = {
  path: GuidePath;
  onNavigate: (path: GuidePath) => void;
  onAskAbout: (scope: AskScope) => void;
};

/**
 * Orquestrador de navegação de GUIDE: Home -> Module -> Section -> Document.
 * É "controlado" (recebe `path` e reporta mudanças via `onNavigate`) para
 * que Terminal possa sincronizar o comando `/guide <module> <topic>` e a
 * cena R3F sem estado duplicado.
 */
export function Guide({ path, onNavigate, onAskAbout }: GuideProps) {
  const { status, modules, error } = useGuide();

  if (status === "loading") {
    return <p className="text-sm text-muted">Carregando guia…</p>;
  }
  if (status === "error" || !modules) {
    return <p className="text-sm text-danger">{error ?? "Não foi possível carregar a guia."}</p>;
  }

  const activeModule = path.moduleId ? modules.find((m) => m.id === path.moduleId) : undefined;
  const activeSection = activeModule && path.sectionId ? activeModule.sections.find((s) => s.id === path.sectionId) : undefined;
  const activeDocument =
    activeSection && path.documentId ? activeSection.documents.find((d) => d.id === path.documentId) : undefined;

  const breadcrumbs = (
    <GuideBreadcrumbs
      module={activeModule}
      sectionTitle={activeSection?.title}
      documentTitle={activeDocument?.title}
      onNavigateHome={() => onNavigate({})}
      onNavigateModule={() => onNavigate({ moduleId: activeModule?.id })}
      onNavigateSection={() => onNavigate({ moduleId: activeModule?.id, sectionId: activeSection?.id })}
    />
  );

  if (activeModule && activeSection && activeDocument) {
    return (
      <div className="flex flex-col gap-4">
        {breadcrumbs}
        <GuideDocument
          module={activeModule}
          section={activeSection}
          doc={activeDocument}
          onAskAboutDocument={() =>
            onAskAbout({
              module: activeModule.id,
              moduleTitle: activeModule.title,
              topic: activeSection.id,
              topicTitle: activeSection.title,
              source: activeDocument.source,
              documentTitle: activeDocument.title,
            })
          }
        />
      </div>
    );
  }

  if (activeModule && activeSection) {
    return (
      <div className="flex flex-col gap-4">
        {breadcrumbs}
        <GuideSection
          module={activeModule}
          section={activeSection}
          onSelectDocument={(documentId) => onNavigate({ moduleId: activeModule.id, sectionId: activeSection.id, documentId })}
          onAskAboutTopic={() =>
            onAskAbout({
              module: activeModule.id,
              moduleTitle: activeModule.title,
              topic: activeSection.id,
              topicTitle: activeSection.title,
            })
          }
        />
      </div>
    );
  }

  if (activeModule) {
    return (
      <div className="flex flex-col gap-4">
        {breadcrumbs}
        <GuideModule module={activeModule} onSelectSection={(sectionId) => onNavigate({ moduleId: activeModule.id, sectionId })} />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {breadcrumbs}
      <GuideHome modules={modules} onSelectModule={(moduleId) => onNavigate({ moduleId })} />
    </div>
  );
}
