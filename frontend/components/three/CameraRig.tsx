"use client";

import { useFrame, useThree } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";

const BASE_POSITION = { x: 0, y: 2.4, z: 9 };

type CameraRigProps = {
  paused?: boolean;
  /** Ponto que a câmera deve reenquadrar suavemente (GUIDE: cluster
   * ativo). `null`/`undefined` volta ao enquadramento padrão (origem). */
  focus?: [number, number, number] | null;
};

/**
 * Deriva de câmera bem leve, tipo "idle": nunca deixa de olhar perto do
 * centro da cena e se desativa por completo com `prefers-reduced-motion`.
 * Quando se passa `focus`, o alvo se desloca lentamente (lerp) até
 * esse ponto em vez de saltar — sem zooms nem movimentos agressivos.
 */
export function CameraRig({ paused = false, focus = null }: CameraRigProps) {
  const { camera } = useThree();
  const lookAtTarget = useRef(new THREE.Vector3(0, 0, 0));

  useFrame(({ clock }) => {
    if (paused) return;
    const t = clock.getElapsedTime();
    const desired = focus ? new THREE.Vector3(...focus) : new THREE.Vector3(0, 0, 0);
    lookAtTarget.current.lerp(desired, 0.02);

    camera.position.x = BASE_POSITION.x + lookAtTarget.current.x * 0.3 + Math.sin(t * 0.08) * 0.6;
    camera.position.y = BASE_POSITION.y + lookAtTarget.current.y * 0.3 + Math.cos(t * 0.06) * 0.25;
    camera.lookAt(lookAtTarget.current);
  });

  return null;
}
