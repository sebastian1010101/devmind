"use client";

import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";
import type { RetrievalStatus } from "@/hooks/useKnowledge";

/**
 * Nó central que representa a pergunta ativa. Pulsa enquanto busca,
 * fica estável com os resultados, e se atenua discretamente em erro.
 */
export function QueryCore({ status, paused = false }: { status: RetrievalStatus; paused?: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const haloRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    const mesh = meshRef.current;
    const halo = haloRef.current;
    if (!mesh || !halo) return;
    const t = clock.getElapsedTime();
    const pulse = status === "searching" && !paused ? 1 + Math.sin(t * 5) * 0.15 : 1;
    mesh.scale.setScalar(THREE.MathUtils.lerp(mesh.scale.x, 0.22 * pulse, 0.2));
    const haloPulse = paused ? 1 : 1 + Math.sin(t * 1.5) * 0.08;
    halo.scale.setScalar(THREE.MathUtils.lerp(halo.scale.x, 0.4 * pulse * haloPulse, 0.15));
  });

  if (status === "idle") return null;

  const color = status === "error" ? "#ff6b6b" : "#e6e6ea";
  const opacity = status === "error" ? 0.3 : 0.9;

  return (
    <>
      {/* Halo aditivo atrás do core: reforça o glow central junto ao bloom
       * sem depender de o pós-processamento estar disponível. */}
      <mesh ref={haloRef}>
        <sphereGeometry args={[1, 16, 16]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={status === "error" ? 0.08 : 0.18}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </mesh>
      <mesh ref={meshRef}>
        <sphereGeometry args={[1, 16, 16]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.6} transparent opacity={opacity} />
      </mesh>
    </>
  );
}
