"use client";

import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";

const DEFAULT_PARTICLE_COUNT = 260;
const SPREAD = { x: 18, y: 8, z: 18 };

/** PRNG determinístico (mulberry32): mesmo resultado em cada render/SSR,
 * evita depender de `Math.random` (impuro) dentro de um `useMemo`. */
function createRng(seed: number) {
  let state = seed;
  return () => {
    state |= 0;
    state = (state + 0x6d2b79f5) | 0;
    let t = Math.imul(state ^ (state >>> 15), 1 | state);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function buildParticlePositions(count: number) {
  const rng = createRng(1337);
  const positions = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    positions[i * 3] = (rng() - 0.5) * SPREAD.x;
    positions[i * 3 + 1] = (rng() - 0.5) * SPREAD.y;
    positions[i * 3 + 2] = (rng() - 0.5) * SPREAD.z;
  }
  return positions;
}

function useParticlePositions(count: number) {
  return useMemo(() => buildParticlePositions(count), [count]);
}

/**
 * Campo de partículas bem sutil, representando a knowledge base "em repouso".
 * Um único `THREE.Points` (não centenas de meshes) com geometria/material
 * memoizados: barato de renderizar e de animar. `count` é reduzido em
 * telas pequenas (ver Scene.tsx) para manter o desempenho no mobile.
 */
export function Particles({ paused = false, count = DEFAULT_PARTICLE_COUNT }: { paused?: boolean; count?: number }) {
  const positions = useParticlePositions(count);
  const pointsRef = useRef<THREE.Points>(null);

  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    return geo;
  }, [positions]);

  const material = useMemo(
    () =>
      new THREE.PointsMaterial({
        color: "#7c9cff",
        size: 0.035,
        sizeAttenuation: true,
        transparent: true,
        opacity: 0.55,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      }),
    []
  );

  useFrame((_, delta) => {
    if (paused || !pointsRef.current) return;
    pointsRef.current.rotation.y += delta * 0.015;
    pointsRef.current.rotation.x = Math.sin(Date.now() * 0.00005) * 0.05;
  });

  return <points ref={pointsRef} geometry={geometry} material={material} />;
}
