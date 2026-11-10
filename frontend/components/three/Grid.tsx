"use client";

import { Grid as DreiGrid } from "@react-three/drei";

/**
 * Grid infinito bem tênue: apenas sugere profundidade/espaço, não deve
 * competir visualmente com o terminal em primeiro plano.
 */
export function Grid() {
  return (
    <DreiGrid
      position={[0, -1.4, 0]}
      args={[40, 40]}
      cellSize={1}
      cellThickness={0.35}
      cellColor="#22242b"
      sectionSize={5}
      sectionThickness={0.6}
      sectionColor="#3a4cbf"
      fadeDistance={24}
      fadeStrength={1.8}
      infiniteGrid
    />
  );
}
