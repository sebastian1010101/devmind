"use client";

import { useGuide } from "@/hooks/useGuide";
import type { GuidePath } from "@/lib/types";
import { Connections } from "./Connections";
import { MAX_VISIBLE_SECTIONS, modulePosition, sectionPosition } from "./guideLayout";
import { KnowledgeNode } from "./KnowledgeNodes";

type GuideSceneProps = {
  path: GuidePath;
  paused?: boolean;
};

/**
 * Representação 3D da estrutura de GUIDE: nós por módulo (sempre
 * visíveis) e, ao entrar em um módulo, suas seções. Nunca representa os
 * ~500 documentos individuais (LOD lógico: doc-level só no HTML).
 * Complementar à navegação real, que vive no terminal/UI HTML.
 */
export function GuideScene({ path, paused = false }: GuideSceneProps) {
  const { modules } = useGuide();
  if (!modules || modules.length === 0) return null;

  const activeModule = path.moduleId ? modules.find((m) => m.id === path.moduleId) : undefined;
  const visibleSections = activeModule ? activeModule.sections.slice(0, MAX_VISIBLE_SECTIONS) : [];

  const moduleNodes = modules.map((module, index) => ({
    module,
    position: modulePosition(index, modules.length),
  }));

  const activeModulePosition = moduleNodes.find((n) => n.module.id === activeModule?.id)?.position;

  const links = [
    ...moduleNodes.map((n) => ({ from: [0, 0, 0] as [number, number, number], to: n.position, opacity: 0.2 })),
    ...(activeModulePosition
      ? visibleSections.map((section, index) => ({
          from: activeModulePosition,
          to: sectionPosition(activeModulePosition, index, visibleSections.length),
          opacity: 0.4,
        }))
      : []),
  ];

  return (
    <>
      <Connections links={links} />
      <KnowledgeNode position={[0, 0, 0]} radius={0.1} color="#e6e6ea" opacity={0.6} paused={paused} />
      {moduleNodes.map(({ module, position }) => (
        <KnowledgeNode
          key={module.id}
          position={position}
          radius={0.22}
          color={module.id === activeModule?.id ? "#7c9cff" : "#4a4f6b"}
          opacity={activeModule ? (module.id === activeModule.id ? 1 : 0.25) : 0.85}
          active={module.id === activeModule?.id}
          paused={paused}
        />
      ))}
      {activeModulePosition &&
        visibleSections.map((section, index) => (
          <KnowledgeNode
            key={section.id}
            position={sectionPosition(activeModulePosition, index, visibleSections.length)}
            radius={path.sectionId === section.id ? 0.16 : 0.12}
            color={path.sectionId === section.id ? "#a7b6ff" : "#7c9cff"}
            opacity={0.9}
            active={path.sectionId === section.id}
            paused={paused}
          />
        ))}
    </>
  );
}
