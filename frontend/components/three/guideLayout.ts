/**
 * Layout puro (sem dependências de three/fiber) para posicionar os nós
 * de GuideScene: módulos em um arco ao redor da origem, seções em um
 * arco menor ao redor do seu módulo ativo. Compartilhado por
 * `GuideScene` (para desenhar os nós) e `Scene` (para apontar a câmera
 * ao cluster ativo via `CameraRig`).
 */

const MODULE_RADIUS = 3.6;
const SECTION_RADIUS = 1.3;

export function modulePosition(index: number, total: number): [number, number, number] {
  const angle = (index / Math.max(total, 1)) * Math.PI * 2;
  return [Math.cos(angle) * MODULE_RADIUS, 0.4, Math.sin(angle) * MODULE_RADIUS];
}

export function sectionPosition(
  modulePos: [number, number, number],
  index: number,
  total: number
): [number, number, number] {
  const angle = (index / Math.max(total, 1)) * Math.PI * 2;
  return [
    modulePos[0] + Math.cos(angle) * SECTION_RADIUS,
    modulePos[1] - 0.3,
    modulePos[2] + Math.sin(angle) * SECTION_RADIUS,
  ];
}

/** Limite de seções renderizadas por módulo ativo: comunica a
 * hierarquia sem tentar desenhar os ~500 documentos nem saturar a cena. */
export const MAX_VISIBLE_SECTIONS = 10;
