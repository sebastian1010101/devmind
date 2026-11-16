"use client";
import { createContext, useContext, useEffect, useState } from "react";
import Link from "next/link";
import { authApi, clearStudyDrafts, navigateWithFreshSession, sessionEvents } from "@/lib/api";
const UserContext = createContext("");
export const useUserId = () => useContext(UserContext);
export function Session({ children, user }: {
  children: React.ReactNode;
  user: {
    id: string;
    email: string;
  };
}) {
  const [error, setError] = useState("");
  useEffect(() => {
    const channel = sessionEvents();
    if (!channel)
      return;
    const changed = () => { clearStudyDrafts(); window.location.reload(); };
    channel.addEventListener("message", changed);
    return () => channel.removeEventListener("message", changed);
  }, []);
  async function logout() {
    setError("");
    try {
      await authApi("logout");
      clearStudyDrafts();
      navigateWithFreshSession("/");
    }
    catch {
      setError("Não foi possível encerrar a sessão. Tente novamente.");
    }
  }
  return <UserContext value={user.id}>
    <div className="dashboard-shell">
      <header className="dashboard-nav">
        <Link href="/" className="brand">
          <span className="brand-mark" aria-hidden="true">&gt;_</span>DevMind</Link>
        <span className="truncate text-xs text-muted">{user.email}</span>
        <button onClick={logout} className="rounded-lg border border-border-strong px-3 py-2 text-sm">Sair</button>
      </header>{error && <p role="alert" className="px-6 text-danger">{error}</p>}{children}</div>
  </UserContext>;
}
