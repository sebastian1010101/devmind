"use client";
import Link from "next/link";
import { useEffect, useState, type FormEvent } from "react";
import { authApi, clearStudyDrafts, navigateWithFreshSession } from "@/lib/api";
type Mode = "login" | "signup" | "verify" | "recover" | "password";
const titles = { login: "Bom ter você de volta.", signup: "Seu próximo passo começa aqui.", verify: "Confirme seu email.", recover: "Recupere seu acesso.", password: "Escolha uma nova senha." };
const actions = { login: "Entrar na minha conta", signup: "Criar conta gratuita", verify: "Confirmar código", recover: "Enviar código de recuperação", password: "Salvar nova senha" };
export function AuthForm({ mode, resume = false, initialNotice = "" }: {
  mode: Mode;
  resume?: boolean;
  initialNotice?: string;
}) {
  const [busy, setBusy] = useState(resume);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState(initialNotice);
  const [recovery, setRecovery] = useState(false);
  useEffect(() => {
    if (mode !== "login" || !resume)
      return;
    authApi("me").then(() => navigateWithFreshSession("/dashboard"))
      .catch(() => setNotice("Entre na sua conta para continuar."))
      .finally(() => setBusy(false));
  }, [mode, resume]);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setBusy(true);
    setError("");
    setNotice("");
    const email = String(data.get("email") ?? "");
    const password = String(data.get("password") ?? "");
    try {
      if (mode === "signup") {
        await authApi("signup", { email, password, adult: data.get("adult") === "on", accepted_terms: data.get("terms") === "on", country: "BR" });
        navigateWithFreshSession("/verificar");
      }
      else if (mode === "verify") {
        await authApi("verify", { email, token: data.get("token"), type: recovery ? "recovery" : "signup" });
        clearStudyDrafts();
        navigateWithFreshSession(recovery ? "/nova-senha" : "/dashboard");
      }
      else if (mode === "recover") {
        await authApi("recover", { email });
        setNotice("Se houver uma conta com esse email, você receberá um código. Abra Confirmar email e selecione recuperação de senha.");
      }
      else if (mode === "password") {
        await authApi("password", { password });
        clearStudyDrafts();
        navigateWithFreshSession("/entrar?senha=atualizada");
      }
      else {
        await authApi("login", { email, password });
        clearStudyDrafts();
        navigateWithFreshSession("/dashboard");
      }
    }
    catch (error) {
      setError(error instanceof Error ? error.message : "Não foi possível continuar. Tente novamente.");
    }
    finally {
      setBusy(false);
    }
  }
  async function resend(event: React.MouseEvent<HTMLButtonElement>) {
    const form = event.currentTarget.form;
    const emailInput = form?.elements.namedItem("email") as HTMLInputElement | null;
    if (!form || !emailInput?.reportValidity())
      return;
    setBusy(true);
    setError("");
    try {
      const result = await authApi("resend", { email: new FormData(form).get("email") });
      setNotice(result.message ?? "Confira seu email.");
    }
    catch (error) {
      setError(error instanceof Error ? error.message : "Tente novamente.");
    }
    finally {
      setBusy(false);
    }
  }
  return <main className="auth-page">
    <Link href="/" className="brand">
      <span className="brand-mark" aria-hidden="true">&gt;_</span>DevMind</Link>
    <section className="auth-card">
      <p className="eyebrow">APRENDER. RECORDAR. EVOLUIR.</p>
      <h1>{titles[mode]}</h1>
      <p className="auth-description">{mode === "verify" ? "Use o código recebido no seu email. Confira também a caixa de spam." : "Seu conhecimento e suas revisões, no seu ritmo."}</p>
      <form onSubmit={submit} className="auth-form">
        {mode !== "password" && <label>Email<input required name="email" type="email" maxLength={254} autoComplete="email" placeholder="voce@exemplo.com" />
        </label>}
        {["login", "signup", "password"].includes(mode) && <label>Senha<input required name="password" type="password" minLength={mode === "login" ? 1 : 12} maxLength={128} autoComplete={mode === "login" ? "current-password" : "new-password"} placeholder={mode === "login" ? "Sua senha" : "Pelo menos 12 caracteres"} />
        </label>}
        {mode === "verify" && <>
          <label>Código de confirmação<input name="token" required inputMode="numeric" autoComplete="one-time-code" pattern="[0-9]{6,10}" minLength={6} maxLength={10} />
          </label>
          <label className="checkbox-label">
            <input type="checkbox" checked={recovery} onChange={e => setRecovery(e.target.checked)} />Estou recuperando minha senha</label>
        </>}
        {mode === "signup" && <>
          <p className="auth-small">Acesso para adultos residentes no Brasil. Use apenas conteúdo técnico público nas interações com IA.</p>
          <label className="checkbox-label">
            <input type="checkbox" name="adult" required />Tenho 18 anos ou mais e resido no Brasil.</label>
          <label className="checkbox-label">
            <input type="checkbox" name="terms" required />
            <span>Li e aceito os <Link href="/termos" target="_blank">termos de uso</Link> e a <Link href="/privacidade" target="_blank">política de privacidade</Link>.</span>
          </label>
        </>}
        {error && <p role="alert" className="auth-error">{error}</p>}
        {notice && <p role="status" className="auth-notice">{notice}</p>}
        <button className="button" disabled={busy}>{busy ? "Aguarde…" : actions[mode]}</button>
        {mode === "verify" && <button className="auth-resend" type="button" onClick={resend} disabled={busy}>Reenviar código de confirmação</button>}
      </form>
      <nav className="auth-links" aria-label="Acesso à conta">
        {mode === "login" ? <>
          <Link href="/recuperar">Esqueci minha senha</Link>
          <Link href="/cadastro">Criar uma conta</Link>
        </> : <Link href="/entrar">Voltar para entrar</Link>}
        <Link href="/verificar">Confirmar email</Link>
      </nav>
    </section>
    <Link className="auth-back" href="/">← Voltar para o início</Link>
  </main>;
}
