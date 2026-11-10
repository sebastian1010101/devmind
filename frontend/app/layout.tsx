import type { Metadata } from "next";
import { Scene } from "@/components/three/Scene";
import { KnowledgeProvider } from "@/hooks/useKnowledge";
import "./globals.css";

export const metadata: Metadata = {
  title: "DevMind — Assistente de estudos",
  description: "Estude programação com respostas fundamentadas e referências para conferir.",
  icons: { icon: "/devmind.svg" },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR" className="h-full antialiased">
      <body className="h-dvh flex flex-col overflow-hidden bg-background text-foreground">
        <KnowledgeProvider>
          <Scene />
          {children}
        </KnowledgeProvider>
      </body>
    </html>
  );
}
