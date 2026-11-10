"use client";

import { Line } from "@react-three/drei";

type ConnectionsProps = {
  links: { from: [number, number, number]; to: [number, number, number]; opacity?: number }[];
  color?: string;
};

/** Linhas finas entre nós (module -> section, center -> module):
 * comunica hierarquia sem precisar de um layout de grafo real. */
export function Connections({ links, color = "#3a4cbf" }: ConnectionsProps) {
  return (
    <>
      {links.map((link, index) => (
        <Line
          key={index}
          points={[link.from, link.to]}
          color={color}
          transparent
          opacity={link.opacity ?? 0.35}
          lineWidth={1}
        />
      ))}
    </>
  );
}
