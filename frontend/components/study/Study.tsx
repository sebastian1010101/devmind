"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError, getGuideDocument, learningApi } from "@/lib/api";
import type { DailySession, GenerateCardsRequest, GuideModule, LearningProgress, LearningSource, Recall, ReviewResult, StudyCard } from "@/lib/types";
import { MarkdownContent } from "@/components/MarkdownContent";

const button = "rounded-lg border border-border-strong px-4 py-2 text-sm hover:border-accent focus-visible:outline-accent disabled:opacity-50 disabled:cursor-wait";
const field = "mt-1 w-full rounded-lg border border-border-strong bg-surface px-3 py-2 text-foreground focus-visible:outline-accent";
const grades = { correct: "Conceito compreendido", partial: "Você está no caminho", incorrect: "Vamos revisar o conceito", ungradable: "A IA não conseguiu avaliar com segurança" };
const difficulties = { easy: "Básico", medium: "Intermediário", hard: "Avançado" };
const recalls: { value: Recall; label: string; hint: string }[] = [
  { value: "again", label: "Não lembrei", hint: "Recomeçar · 1 dia" },
  { value: "hard", label: "Com dificuldade", hint: "Manter etapa · 1 dia" },
  { value: "good", label: "Lembrei", hint: "Avançar uma etapa" },
  { value: "easy", label: "Foi fácil", hint: "Avançar duas etapas" },
];

function date(value: string) {
  return new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short", timeZone: "America/Sao_Paulo" }).format(new Date(value));
}
function message(error: unknown) {
  return error instanceof ApiError ? error.message : "Não foi possível concluir. Tente novamente.";
}
function saved(key: string): string | null {
  try { return localStorage.getItem(key); } catch { return null; }
}
function remember(key: string, value: string | null) {
  try { if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value); } catch { /* Server still persists submitted answers. */ }
}

function Evidence({ sources }: { sources: LearningSource[] }) {
  const [document, setDocument] = useState<{ source: string; markdown: string } | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function open(source: string) {
    setLoading(true); setError("");
    try { setDocument({ source, markdown: await getGuideDocument(source, new AbortController().signal) }); }
    catch (error) { setError(message(error)); }
    finally { setLoading(false); }
  }
  return <div className="mt-4 space-y-2 min-w-0">
    <p className="text-xs uppercase tracking-widest text-muted">Evidência documental</p>
    {sources.map((source) => <details key={source.evidence_id} className="rounded-lg border border-border p-3">
      <summary className="cursor-pointer break-words text-accent">{source.section} · {source.evidence_id}</summary>
      <p className="mt-2 break-all text-xs text-muted">{source.source} · fragmento {source.chunk_id}</p>
      {source.source_changed && <p className="mt-2 text-danger">O documento mudou. Este cartão usa a versão salva na geração.</p>}
      {source.chunk_text && <p className="mt-3 whitespace-pre-wrap leading-relaxed">{source.chunk_text}</p>}
      <p className="mt-2 break-all font-mono text-xs text-muted">SHA-256: {source.text_sha256}</p>
      <button className={`${button} mt-2`} disabled={loading} onClick={() => open(source.source)}>Abrir documento atual</button>
    </details>)}
    {error && <p role="alert" className="text-danger">{error}</p>}
    {document && <section className="rounded-xl border border-border p-4">
      <button className={`${button} mb-3`} onClick={() => setDocument(null)}>Fechar documento</button>
      <p className="mb-3 break-all text-xs text-muted">{document.source} · versão atual do Guia</p>
      <MarkdownContent content={document.markdown} />
    </section>}
  </div>;
}

export function Study({ active, modules }: { active: boolean; modules: GuideModule[] }) {
  const [tab, setTab] = useState<"dashboard" | "practice" | "progress">("dashboard");
  const [progress, setProgress] = useState<LearningProgress | null>(null);
  const [due, setDue] = useState<StudyCard[]>([]);
  const [daily, setDaily] = useState<DailySession | null>(null);
  const [moduleId, setModuleId] = useState("devmind");
  const [topic, setTopic] = useState("");
  const [source, setSource] = useState("");
  const [focus, setFocus] = useState("");
  const [count, setCount] = useState(3);
  const [queue, setQueue] = useState<StudyCard[]>([]);
  const [position, setPosition] = useState(0);
  const [card, setCard] = useState<StudyCard | null>(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const reviewRequest = useRef<{ id: string; answer: string } | null>(null);
  const loaded = useRef(false);
  const selectedModule = modules.find((m) => m.id === moduleId);
  const documents = selectedModule?.sections.flatMap((s) => s.documents).filter((d) => !topic || d.topic === topic) ?? [];

  const refresh = useCallback(async () => {
    const [p, d] = await Promise.all([learningApi.progress(), learningApi.due()]);
    setProgress(p); setDue(d.cards);
  }, []);

  useEffect(() => {
    if (!active || loaded.current) return;
    loaded.current = true;
    refresh().then(() => {
      const pending = saved("devmind:generation");
      if (pending) {
        try {
          const request: GenerateCardsRequest = JSON.parse(pending);
          setModuleId(request.module); setTopic(request.topic ?? ""); setSource(request.source ?? "");
          setFocus(request.focus); setCount(request.count);
          setNotice("Há uma geração anterior. Enviar novamente com as mesmas opções recupera o resultado.");
        } catch { remember("devmind:generation", null); }
      }
    }).catch((error) => { loaded.current = false; setError(message(error)); });
  }, [active, refresh]);

  async function openCard(item: StudyCard) {
    setBusy("Abrindo cartão…"); setError(""); setResult(null); setAnswer("");
    try {
      const current = await learningApi.card(item.id);
      setCard(current); reviewRequest.current = null;
      const attempt = current.latest_attempt;
      if (attempt && (attempt.state !== "completed" || !attempt.result?.self_recall)) {
        setAnswer(attempt.answer); setResult(attempt.result);
        reviewRequest.current = { id: attempt.request_id, answer: attempt.answer };
      } else {
        setAnswer(saved(`devmind:draft:${item.id}`) ?? "");
      }
      setTab("practice");
    } catch (error) { setError(message(error)); }
    finally { setBusy(""); }
  }

  async function start(cards: StudyCard[]) {
    setNotice("");
    if (!cards.length) { setNotice("Tudo em dia. Gere novos cartões ou volte na próxima revisão."); return; }
    setQueue(cards); setPosition(0); await openCard(cards[0]);
  }

  async function generate(event: React.FormEvent) {
    event.preventDefault(); setBusy("Recuperando evidências e gerando cartões…"); setError(""); setNotice("");
    const body = { module: moduleId, ...(topic ? { topic } : {}), ...(source ? { source } : {}),
      focus: focus.trim() || `Conceitos fundamentais de ${selectedModule?.title ?? moduleId} ${topic}`, count };
    let request: GenerateCardsRequest = { ...body, request_id: crypto.randomUUID() };
    try {
      const old = saved("devmind:generation");
      if (old) {
        const parsed: GenerateCardsRequest = JSON.parse(old);
        const { request_id: id, ...previous } = parsed;
        if (JSON.stringify(previous) === JSON.stringify(body)) request = { ...body, request_id: id };
      }
    } catch { /* A new request is safe if a saved draft is malformed. */ }
    remember("devmind:generation", JSON.stringify(request));
    try {
      const deck = await learningApi.generate(request);
      remember("devmind:generation", null);
      await refresh(); await start(deck.cards);
    } catch (error) { setError(message(error)); }
    finally { setBusy(""); }
  }

  async function evaluate(event: React.FormEvent) {
    event.preventDefault(); if (!card || !answer.trim()) return;
    setBusy("Avaliando os conceitos da sua resposta…"); setError("");
    if (!reviewRequest.current || reviewRequest.current.answer !== answer.trim()) {
      reviewRequest.current = { id: crypto.randomUUID(), answer: answer.trim() };
    }
    try {
      setResult(await learningApi.review(card.id, reviewRequest.current.id, reviewRequest.current.answer));
      await refresh();
      if (daily) setDaily(await learningApi.daily());
    } catch (error) { setError(`${message(error)} Seu texto está salvo; você pode reenviar.`); }
    finally { setBusy(""); }
  }

  async function rate(recall: Recall) {
    if (!result || !card) return;
    setBusy("Salvando sua recordação…"); setError("");
    try {
      setResult(await learningApi.recall(result.review_id, recall));
      remember(`devmind:draft:${card.id}`, null);
      await refresh(); if (daily) setDaily(await learningApi.daily());
    } catch (error) { setError(message(error)); }
    finally { setBusy(""); }
  }

  async function next() {
    if (position + 1 < queue.length) { setPosition(position + 1); await openCard(queue[position + 1]); }
    else { setTab("dashboard"); setCard(null); setNotice("Sessão concluída. Seu progresso foi salvo."); }
  }

  async function startDaily() {
    setBusy("Preparando sua revisão diária…"); setError("");
    try { const session = await learningApi.daily(); setDaily(session); await start(session.cards.filter((c) => !c.completed)); }
    catch (error) { setError(message(error)); }
    finally { setBusy(""); }
  }

  return <section aria-label="Active Recall" className="space-y-5 pb-3">
    <div className="flex flex-wrap items-start justify-between gap-3">
      <div><p className="font-mono text-xs tracking-widest text-accent">ACTIVE RECALL</p>
        <h2 className="mt-2 text-2xl font-semibold">Aprenda. Recorde. Evolua.</h2>
        <p className="mt-2 text-xs text-muted">Demo local · um estudante · datas de São Paulo</p></div>
      <nav aria-label="Navegação de estudo" className="flex flex-wrap gap-2">
        <button className={button} aria-current={tab === "dashboard" ? "page" : undefined} onClick={() => setTab("dashboard")}>Painel</button>
        <button className={button} aria-current={tab === "progress" ? "page" : undefined} onClick={() => setTab("progress")}>Progresso</button>
        {card && <button className={button} onClick={() => setTab("practice")}>Continuar prática</button>}
      </nav>
    </div>
    {busy && <p role="status" className="text-accent">{busy}</p>}
    {error && <div role="alert" className="rounded-lg border border-danger/40 p-3 text-danger">{error}
      {!progress && <button className={`${button} ml-2`} onClick={() => { setError(""); refresh().catch((e) => setError(message(e))); }}>Reconectar</button>}
    </div>}
    {notice && <p role="status" className="rounded-lg border border-border p-3 text-muted">{notice}</p>}

    {tab !== "practice" && <div className="grid grid-cols-3 gap-2">
      {[{ label: "Para revisar", value: progress?.due }, { label: "Já praticados", value: progress?.reviewed }, { label: "Cartões", value: progress?.total }].map((item) =>
        <div key={item.label} className="rounded-xl border border-border bg-surface/80 p-3 sm:p-4">
          <p className="text-2xl font-semibold text-accent">{item.value ?? "—"}</p><p className="mt-1 text-xs text-muted">{item.label}</p>
        </div>)}
    </div>}

    {tab === "dashboard" && <>
      <div className="rounded-xl border border-accent/40 bg-surface/80 p-4">
        <h3 className="font-semibold">Um pouco todos os dias</h3>
        <p className="mt-2 text-muted">Até 5 cartões vencidos. Os mais atrasados e difíceis vêm primeiro.</p>
        {daily && <div className="mt-3"><label htmlFor="daily-progress">Hoje: {daily.completed} de {daily.total}</label>
          <progress id="daily-progress" className="mt-2 w-full accent-accent" value={daily.completed} max={daily.total || 1} /></div>}
        <button className={`${button} mt-3 border-accent text-accent`} disabled={!!busy} onClick={startDaily}>Começar revisão diária</button>
      </div>
      <form onSubmit={generate} className="rounded-xl border border-border bg-surface/80 p-4 space-y-3">
        <h3 className="font-semibold">Criar cartões com suas fontes</h3>
        <p className="text-xs text-muted">A IA usa documentos recuperados no escopo selecionado. Até 3 cartões por geração.</p>
        <div className="grid gap-3 sm:grid-cols-2">
          <label>Módulo<select aria-label="Módulo" className={field} value={moduleId} disabled={!!busy} onChange={(e) => { setModuleId(e.target.value); setTopic(""); setSource(""); }}>
            {modules.map((m) => <option key={m.id} value={m.id}>{m.title}</option>)}
          </select></label>
          <label>Tema<select aria-label="Tema" className={field} value={topic} disabled={!!busy} onChange={(e) => { setTopic(e.target.value); setSource(""); }}>
            <option value="">Todos os temas</option>
            {selectedModule?.sections.map((s) => <option key={s.id} value={s.documents[0]?.topic ?? s.id}>{s.title}</option>)}
          </select></label>
        </div>
        <label className="block">Documento<select aria-label="Documento" className={field} value={source} disabled={!!busy} onChange={(e) => setSource(e.target.value)}>
          <option value="">Documentos do escopo</option>{documents.map((d) => <option key={d.id} value={d.source}>{d.title}</option>)}
        </select></label>
        <label className="block">O que quer praticar? <span className="text-muted">(opcional)</span>
          <input aria-label="O que quer praticar?" className={field} maxLength={1200} value={focus} disabled={!!busy} onChange={(e) => setFocus(e.target.value)} placeholder="Ex.: retirar arquivos do staging sem perder edições" />
        </label>
        <div className="flex flex-wrap items-end gap-3">
          <label>Quantidade<select aria-label="Quantidade" className={field} value={count} disabled={!!busy} onChange={(e) => setCount(Number(e.target.value))}>{[1, 2, 3].map((n) => <option key={n}>{n}</option>)}</select></label>
          <button className={`${button} border-accent text-accent`} disabled={!!busy || !selectedModule} type="submit">Gerar e estudar</button>
        </div>
        <p className="text-xs text-muted">Gerações hoje: {progress?.usage.generation?.used ?? 0}/10 · avaliações: {progress?.usage.review?.used ?? 0}/50. Reenvios concluídos não consomem cota.</p>
      </form>
      <section><div className="flex items-center justify-between gap-3"><h3 className="font-semibold">Sua fila de revisão</h3>
        <button className={button} disabled={!!busy || !due.length} onClick={() => start(due)}>Praticar pendentes</button></div>
        <ul className="mt-3 space-y-2">{due.map((item) => <li key={item.id}><button className={`${button} w-full text-left`} disabled={!!busy} onClick={() => start([item])}>
          <span className="block break-words">{item.question}</span><span className="mt-1 block text-xs text-muted">{item.module} · {item.topic ?? "Geral"} · {difficulties[item.difficulty]} · {item.schedule.reviews} revisões</span>
        </button></li>)}</ul>
        {!due.length && <p className="mt-3 text-muted">Nenhum cartão pendente. Gere cartões para começar.</p>}
      </section>
    </>}

    {tab === "practice" && card && <article className="rounded-xl border border-border bg-surface/90 p-4 sm:p-6">
      <div className="flex flex-wrap justify-between gap-2 text-xs text-muted"><span>Cartão {position + 1} de {queue.length} · {card.module} / {card.topic ?? "Geral"}</span><span>{difficulties[card.difficulty]}</span></div>
      <h3 className="mt-5 break-words text-xl leading-relaxed font-medium">{card.question}</h3>
      <form className="mt-5" onSubmit={evaluate}>
        <label htmlFor="study-answer">Explique com suas palavras</label>
        <textarea id="study-answer" className={`${field} min-h-32 resize-y`} maxLength={1200} value={answer} disabled={!!busy || !!result}
          onChange={(e) => { setAnswer(e.target.value); remember(`devmind:draft:${card.id}`, e.target.value); }} placeholder="Tente recordar antes de consultar as fontes…" />
        <div className="mt-2 flex flex-wrap items-center justify-between gap-2"><span className="text-xs text-muted">{answer.length}/1200 · rascunho salvo neste navegador</span>
          {!result && <button className={`${button} border-accent text-accent`} disabled={!!busy || !answer.trim()} type="submit">Avaliar resposta</button>}</div>
      </form>
      {result && <div className="mt-6 space-y-4" aria-live="polite">
        <div className="rounded-xl border border-accent/40 p-4"><h4 className="text-lg font-semibold text-accent">{grades[result.grade]}</h4><p className="mt-2 leading-relaxed">{result.feedback}</p></div>
        {[{ label: "Você incluiu", items: result.present_concepts }, { label: "Para completar", items: result.missing_concepts }, { label: "Pontos para corrigir", items: result.errors }].filter((g) => g.items.length).map((group) =>
          <div key={group.label}><h4 className="font-semibold">{group.label}</h4><ul className="mt-2 list-disc pl-5 space-y-1">{group.items.map((text, i) => <li className="break-words" key={i}>{text}</li>)}</ul></div>)}
        <details className="rounded-lg border border-border p-3"><summary className="cursor-pointer text-accent">Resposta de referência e explicação</summary>
          <p className="mt-3 whitespace-pre-wrap break-words">{result.reference_answer}</p><p className="mt-3 whitespace-pre-wrap break-words text-muted">{result.explanation}</p></details>
        <p className="text-xs text-muted">{result.notice}</p>
        <fieldset disabled={!!busy || !!result.self_recall}><legend className="mb-3 font-semibold">Como foi recordar?</legend>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">{recalls.map((item) => <button key={item.value} type="button" className={`${button} ${result.self_recall === item.value ? "border-accent text-accent" : ""}`} onClick={() => rate(item.value)}>
            {item.label}<span className="mt-1 block text-xs text-muted">{item.hint}</span></button>)}</div>
        </fieldset>
        <p className="text-accent">{result.grade === "ungradable" && !result.self_recall ? "Calendário preservado até sua autoavaliação." : `Próxima revisão: ${date(result.schedule.due_at)} · ${result.schedule.interval_days} dia(s)`}</p>
        {result.grade === "ungradable" && !result.self_recall && <button className={button} disabled={!!busy} onClick={() => { reviewRequest.current = null; setResult(null); }}>Tentar avaliar novamente</button>}
        <button className={`${button} border-accent text-accent`} disabled={!!busy || !result.self_recall} onClick={next}>{position + 1 < queue.length ? "Próximo cartão" : "Concluir sessão"}</button>
      </div>}
      <Evidence key={card.id} sources={result?.sources ?? card.sources} />
    </article>}

    {tab === "progress" && progress && <div className="space-y-5">
      <section className="rounded-xl border border-border bg-surface/80 p-4"><h3 className="font-semibold">Seu aprendizado</h3>
        <p className="mt-2 text-muted">{progress.reviewed} cartões praticados · {progress.new} novos · {progress.attempts} tentativas avaliadas.</p>
        <p className="mt-2 text-muted">{progress.correct} de {progress.graded} avaliações classificáveis foram consideradas corretas pela IA. Este indicador não comprova domínio.</p>
      </section>
      <section><h3 className="font-semibold">Progresso por tema</h3><ul className="mt-3 space-y-3">{progress.topics.map((item) => <li key={`${item.module}:${item.topic}`} className="rounded-lg border border-border p-3">
        <div className="flex flex-wrap justify-between gap-2"><span>{item.module} / {item.topic ?? "Geral"}</span><span className="text-muted">{item.reviewed}/{item.total} praticados · {item.due} pendentes</span></div>
        <progress aria-label={`Cartões praticados em ${item.topic ?? item.module}`} className="mt-2 w-full accent-accent" value={item.reviewed} max={item.total || 1} />
      </li>)}</ul>{!progress.topics.length && <p className="mt-3 text-muted">Seu progresso aparecerá após a primeira geração.</p>}</section>
      <section><h3 className="font-semibold">Próximas revisões</h3><ul className="mt-3 space-y-2">{progress.upcoming.map((item) => <li key={item.id} className="rounded-lg border border-border p-3">
        <p className="break-words">{item.question}</p><p className="mt-1 text-xs text-accent">{date(item.due_at)}</p>
      </li>)}</ul>{!progress.upcoming.length && <p className="mt-3 text-muted">Nenhuma revisão futura agendada.</p>}</section>
    </div>}
  </section>;
}
