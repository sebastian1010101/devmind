import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { Session } from "@/components/auth/Session";
import { KnowledgeProvider } from "@/hooks/useKnowledge";
import { Scene } from "@/components/three/Scene";
export default async function DashboardLayout({ children }: {
  children: React.ReactNode;
}) {
  const token = (await cookies()).get("devmind_access")?.value;
  if (!token)
    redirect("/entrar?retomar=1");
  const apiUrl = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
  const response = await fetch(`${apiUrl}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }, cache: "no-store", signal: AbortSignal.timeout(10000),
  });
  if (response.status === 401)
    redirect("/entrar?retomar=1");
  if (!response.ok)
    throw new Error("Não foi possível verificar a sessão. Tente novamente.");
  const user: {
    id: string;
    email: string;
  } = await response.json();
  return <Session user={user}>
    <KnowledgeProvider>
      <Scene />{children}</KnowledgeProvider>
  </Session>;
}
