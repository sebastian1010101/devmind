"use client";

import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";

export type KnowledgeNodeProps = {
  position: [number, number, number];
  radius?: number;
  color?: string;
  opacity?: number;
  active?: boolean;
  paused?: boolean;
};

/**
 * Nó etiquetado reutilizável para GuideScene: uma esfera simples que se
 * atenua/realça conforme `opacity`/`active`. Pensado para representar
 * módulos/seções (dezenas de nós), nunca os ~500 documentos.
 */
export function KnowledgeNode({
  position,
  radius = 0.16,
  color = "#7c9cff",
  opacity = 1,
  active = false,
  paused = false,
}: KnowledgeNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    const mesh = meshRef.current;
    if (!mesh) return;
    const pulse = active && !paused ? 1 + Math.sin(clock.getElapsedTime() * 2.5) * 0.08 : 1;
    mesh.scale.setScalar(THREE.MathUtils.lerp(mesh.scale.x || 1, pulse, 0.15));
  });

  return (
    <mesh ref={meshRef} position={position}>
      <sphereGeometry args={[radius, 16, 16]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={active ? 0.7 : 0.3}
        transparent
        opacity={opacity}
      />
    </mesh>
  );
}
