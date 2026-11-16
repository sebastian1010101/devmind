import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DevMind — Assistente de estudos",
  description: "Estude programação com respostas fundamentadas e referências para conferir.",
  icons: { icon: "/devmind.svg" },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR" className="h-full antialiased">
      <body className="min-h-dvh bg-background text-foreground">
        {children}
      </body>
    </html>
  );
}
