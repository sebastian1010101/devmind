import { AuthForm } from "@/components/auth/AuthForm";
export default async function Page({ searchParams }: {
  searchParams: Promise<{
    retomar?: string;
    senha?: string;
    sessao?: string;
  }>;
}) {
  const query = await searchParams;
  const notice = query.senha ? "Senha atualizada. Entre com sua nova senha." : query.sessao ? "Sua sessão expirou. Entre novamente para retomar seu progresso." : "";
  return <AuthForm mode="login" resume={query.retomar === "1"} initialNotice={notice} />;
}
