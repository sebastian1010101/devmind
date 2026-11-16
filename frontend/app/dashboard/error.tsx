"use client";
import Link from "next/link";
export default function DashboardError({ reset }: {
  reset: () => void;
}) {
  return <main className="auth-page">
    <section className="auth-card">
      <h1>Não foi possível abrir seu painel.</h1>
      <p className="auth-description">Seu progresso fica salvo. Verifique a conexão e tente novamente.</p>
      <button className="button" onClick={reset}>Tentar novamente</button>
      <Link href="/entrar" className="block mt-6 text-accent">Voltar para entrar</Link>
    </section>
  </main>;
}
