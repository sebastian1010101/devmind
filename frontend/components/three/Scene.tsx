"use client";

import { Stars } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Bloom, EffectComposer, Vignette } from "@react-three/postprocessing";
import { Component, Suspense, useEffect, useMemo, useState, type ReactNode } from "react";
import { useGuide } from "@/hooks/useGuide";
import { useKnowledge } from "@/hooks/useKnowledge";
import { AskScene } from "./AskScene";
import { CameraRig } from "./CameraRig";
import { GuideScene } from "./GuideScene";
import { Grid } from "./Grid";
import { modulePosition } from "./guideLayout";
import { Particles } from "./Particles";

/**
 * Fundo 3D decorativo em tela cheia. Puramente visual/complementar:
 * `pointer-events-none` + `aria-hidden` para nunca competir com a UI real
 * nem com a acessibilidade. Pausa (frameloop "never") se a aba não está
 * visível, e desativa animações se o usuário pede `prefers-reduced-motion`.
 */
function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function isTabVisible() {
  return typeof document === "undefined" || document.visibilityState === "visible";
}

function isCompactViewport() {
  return typeof window !== "undefined" && window.matchMedia("(max-width: 640px)").matches;
}

class SceneFallback extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  render() {
    return this.state.failed ? null : this.props.children;
  }
}

export function Scene() {
  return <SceneFallback><KnowledgeScene /></SceneFallback>;
}

function KnowledgeScene() {
  const [reducedMotion, setReducedMotion] = useState(prefersReducedMotion);
  const [tabVisible, setTabVisible] = useState(isTabVisible);
  const [compact, setCompact] = useState(isCompactViewport);
  const { status, mode, guidePath } = useKnowledge();
  const { modules } = useGuide();

  const cameraFocus = useMemo<[number, number, number] | null>(() => {
    if (mode !== "guide" || !guidePath.moduleId || !modules) return null;
    const index = modules.findIndex((m) => m.id === guidePath.moduleId);
    if (index === -1) return null;
    return modulePosition(index, modules.length);
  }, [mode, guidePath.moduleId, modules]);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const onChange = (event: MediaQueryListEvent) => setReducedMotion(event.matches);
    mediaQuery.addEventListener("change", onChange);
    return () => mediaQuery.removeEventListener("change", onChange);
  }, []);

  useEffect(() => {
    const onVisibilityChange = () => setTabVisible(isTabVisible());
    document.addEventListener("visibilitychange", onVisibilityChange);
    return () => document.removeEventListener("visibilitychange", onVisibilityChange);
  }, []);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(max-width: 640px)");
    const onChange = (event: MediaQueryListEvent) => setCompact(event.matches);
    mediaQuery.addEventListener("change", onChange);
    return () => mediaQuery.removeEventListener("change", onChange);
  }, []);

  return (
    <div className="fixed inset-0 -z-10 pointer-events-none" aria-hidden="true">
      <Canvas
        dpr={compact ? [1, 1] : [1, 1.5]}
        gl={{ antialias: true, alpha: true }}
        camera={{ position: [0, 2.4, 9], fov: 45 }}
        frameloop={tabVisible ? "always" : "never"}
      >
        <color attach="background" args={["#050506"]} />
        <fog attach="fog" args={["#050506", 9, 24]} />
        <ambientLight intensity={0.25} />
        <hemisphereLight args={["#4a5cff", "#050506", 0.4]} />
        <pointLight position={[0, 1.6, 1]} color="#7c9cff" intensity={12} distance={9} decay={2} />
        <Suspense fallback={null}>
          <Stars
            radius={60}
            depth={30}
            count={compact ? 800 : 2200}
            factor={2.2}
            saturation={0}
            fade
            speed={reducedMotion ? 0 : 0.3}
          />
          <Grid />
          <Particles paused={reducedMotion} count={compact ? 90 : undefined} />
          {mode === "guide" ? (
            <GuideScene path={guidePath} paused={reducedMotion} />
          ) : (
            <AskScene status={status} paused={reducedMotion} />
          )}
        </Suspense>
        <CameraRig paused={reducedMotion} focus={cameraFocus} />
        {!compact && (
          <EffectComposer multisampling={0}>
            <Bloom
              mipmapBlur
              luminanceThreshold={0.18}
              luminanceSmoothing={0.3}
              intensity={0.9}
              radius={0.6}
            />
            <Vignette eskil={false} offset={0.25} darkness={0.65} />
          </EffectComposer>
        )}
      </Canvas>
    </div>
  );
}
