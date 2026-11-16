"use client";

import { useEffect, useRef, useState, type MouseEvent } from "react";
import { ApiError, askQuestion, getStats } from "@/lib/api";
import { ABOUT_TEXT, HELP_TEXT, parseCommand } from "@/lib/commands";
import { useDebugMode } from "@/hooks/useDebugMode";
import { useGuide } from "@/hooks/useGuide";
import { useKnowledge } from "@/hooks/useKnowledge";
import type { AskScope, GuidePath, Mode, Source, StatsResponse } from "@/lib/types";
import { CommandInput } from "./CommandInput";
import { ModeSelector } from "./ModeSelector";
import { TerminalEntry, type TerminalEntryData } from "./TerminalEntry";
import { Guide } from "@/components/guide/Guide";
import { Study } from "@/components/study/Study";

let entryCounter = 0;
function nextId() {
  entryCounter += 1;
  return `entry-${entryCounter}`;
}

const EXAMPLES = [
  { topic: "Git", question: "Como retiro README.md do staging mantendo minhas edições?" },
  { topic: "Python", question: "Como conto ocorrências em Python com um dicionário e get?" },
  { topic: "HTTP", question: "Quando uma API deve retornar 401 ou 403?" },
];

function formatStatsLine(stats: StatsResponse | null, statsError: boolean): string {
  if (statsError) return "Catálogo local indisponível";
  if (!stats) return "Carregando catálogo…";
  return `Catálogo local · ${stats.documents_indexed} documentos`;
}

/** Não re-focar o input se o clique foi sobre um elemento interativo próprio
 * (botões de mode/guide/sources, links, etc.) — evita roubar o foco. */
function isInteractiveTarget(target: EventTarget | null): boolean {
  return target instanceof Element && Boolean(target.closest("button, a, input, textarea, summary"));
}

/**
 * Terminal é o orquestrador da CLI: mantém o histórico de entradas
 * (comandos + saídas), o modo ativo e traduz cada linha de entrada
 * (parseada por lib/commands.ts) em uma ação.
 *
 * ASK (texto livre ou `/ask`) chama o backend real via lib/api.ts,
 * opcionalmente restrito a um `AskScope` (module/topic) quando se chega
 * desde GUIDE com "Ask about this topic/document". GUIDE (`/guide`) navega
 * a estrutura Module -> Section -> Document servida por `GET /guide`
 * (ver hooks/useGuide), substituindo o log de entries enquanto está ativo.
 */
export function Terminal() {
  const [entries, setEntries] = useState<TerminalEntryData[]>([]);
  const [inputSession, setInputSession] = useState(0);
  const [mode, setMode] = useState<Mode>("ask");
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [statsError, setStatsError] = useState(false);
  const [lastSources, setLastSources] = useState<Source[]>([]);
  const [guidePath, setGuidePath] = useState<GuidePath>({});
  const [askScope, setAskScope] = useState<AskScope | null>(null);
  const logRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  // Id da última request a /ask. Só a mais recente pode atualizar o estado
  // compartilhado; as antigas apenas completam sua própria entrada do log.
  const latestRequestRef = useRef(0);
  const knowledge = useKnowledge();
  const debug = useDebugMode();
  const guide = useGuide();

  useEffect(() => {
    if (mode === "ask") logRef.current?.scrollTo({ top: logRef.current.scrollHeight });
  }, [entries, mode]);

  useEffect(() => {
    if (mode === "guide") logRef.current?.scrollTo({ top: 0 });
  }, [guidePath, mode]);

  useEffect(() => {
    getStats()
      .then(setStats)
      .catch(() => setStatsError(true));
  }, []);

  // Mantém o Context sincronizado para que a cena R3F (Scene/AskScene/
  // GuideScene) saiba qual modo e qual rota de GUIDE estão ativos sem
  // receber props diretas desde page.tsx.
  useEffect(() => {
    knowledge.setMode(mode);
  }, [mode]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    knowledge.setGuidePath(guidePath);
  }, [guidePath]); // eslint-disable-line react-hooks/exhaustive-deps

  const appendEntry = (kind: "system" | "output" | "error", content: string) => {
    setEntries((prev) => [...prev, { id: nextId(), kind, content }]);
  };

  /** Executa uma pergunta contra `/ask` real, opcionalmente restrita por
   * `askScope` (vinda desde GUIDE). */
  const runQuery = async (question: string, options: { echo?: string; scope?: AskScope | null } = {}) => {
    setMode("ask");
    const scope = options.scope !== undefined ? options.scope : askScope;
    if (options.echo) {
      setEntries((prev) => [...prev, { id: nextId(), kind: "command", content: options.echo! }]);
    }
    const requestId = ++latestRequestRef.current;
    knowledge.startSearch();
    const loadingId = nextId();
    setEntries((prev) => [
      ...prev,
      { id: loadingId, kind: "loading", content: "Consultando a base " },
    ]);

    try {
      const result = await askQuestion(question, undefined, scope);
      if (requestId === latestRequestRef.current) {
        setLastSources(result.sources);
        knowledge.setResults(result.sources);
      }
      setEntries((prev) =>
        prev.map((entry) =>
          entry.id === loadingId
            ? {
                id: loadingId,
                kind: "answer",
                content: result.answer,
                sources: result.sources,
                latencyMs: result.latencyMs,
                scope,
              }
            : entry
        )
      );
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : "Ocorreu um erro inesperado ao consultar a API.";
      if (requestId === latestRequestRef.current) {
        setLastSources([]);
        knowledge.setError();
      }
      setEntries((prev) =>
        prev.map((entry) => (entry.id === loadingId ? { id: loadingId, kind: "error", content: message } : entry))
      );
    }
  };

  const runAsk = (question: string) => runQuery(question);

  /** "Ask about this topic/document" desde GUIDE: fixa o scope ativo,
   * muda para o modo ASK e avisa no log — a pergunta a escreve o usuário. */
  const handleAskAbout = (scope: AskScope) => {
    setAskScope(scope);
    setMode("ask");
    const label = scope.documentTitle ?? scope.topicTitle ?? scope.moduleTitle;
    appendEntry("system", `Consulta restrita a ${label}. Escreva sua pergunta.`);
  };

  const clearAskScope = () => setAskScope(null);

  const clearConversation = () => {
    latestRequestRef.current += 1;
    setEntries([]);
    setLastSources([]);
    setInputSession((session) => session + 1);
    clearAskScope();
    knowledge.reset();
  };

  /** Matching básico (sem NLP) por id exato ou substring do título,
   * case-insensitive, para `/guide <módulo> <tema>`. */
  const resolveGuideArgs = (args: string[]): GuidePath | null => {
    if (!guide.modules) return null;
    if (args.length === 0) return {};

    const [moduleArg, ...rest] = args;
    const moduleQuery = moduleArg.toLowerCase();
    const guideModule = guide.modules.find(
      (m) => m.id === moduleQuery || m.id.includes(moduleQuery) || m.title.toLowerCase().includes(moduleQuery)
    );
    if (!guideModule) return null;
    if (rest.length === 0) return { moduleId: guideModule.id };

    const sectionQuery = rest.join(" ").toLowerCase();
    const section = guideModule.sections.find(
      (s) => s.id === sectionQuery || s.id.includes(sectionQuery) || s.title.toLowerCase().includes(sectionQuery)
    );
    if (!section) return { moduleId: guideModule.id };
    return { moduleId: guideModule.id, sectionId: section.id };
  };

  const runGuide = (args: string[]) => {
    setMode("guide");
    if (args.length === 0) {
      setGuidePath({});
      return;
    }
    const resolved = resolveGuideArgs(args);
    if (resolved === null) {
      appendEntry("error", `"${args.join(" ")}" não encontrado na guia. Digite /guide para ver os módulos.`);
      return;
    }
    setGuidePath(resolved);
  };

  const handleSubmit = (raw: string) => {
    setEntries((prev) => [...prev, { id: nextId(), kind: "command", content: raw }]);
    const parsed = parseCommand(raw);

    switch (parsed.type) {
      case "help":
        appendEntry("output", HELP_TEXT);
        break;
      case "about":
        appendEntry("output", ABOUT_TEXT);
        break;
      case "clear":
        clearConversation();
        break;
      case "sources":
        if (lastSources.length === 0) {
          appendEntry("output", "SOURCES\n(nenhuma ainda — faça uma pergunta primeiro)");
        } else {
          appendEntry(
            "output",
            [
              "SOURCES",
              ...lastSources.map((s, i) => {
                const label = `${String(i + 1).padStart(2, "0")} ${s.source} · ${s.section}`;
                return debug ? `${label} · ${Math.round(s.score * 100)}%` : label;
              }),
            ].join("\n")
          );
        }
        break;
      case "mode":
        if (parsed.mode) {
          if (parsed.mode === "ask") clearAskScope();
          setMode(parsed.mode);
          appendEntry("system", `Modo ativo: ${parsed.mode.toUpperCase()}`);
        } else {
          appendEntry("system", `Modo ativo: ${mode.toUpperCase()}`);
        }
        break;
      case "ask":
        if (!parsed.question) {
          clearAskScope();
          setMode("ask");
          appendEntry("system", "Modo ASK ativo. Escreva uma pergunta.");
        } else {
          runAsk(parsed.question);
        }
        break;
      case "guide":
        runGuide(parsed.args);
        break;
      case "question":
        runAsk(parsed.question);
        break;
      case "unknown":
        appendEntry("error", `Comando não reconhecido: "${parsed.raw}". Digite /help para ver os comandos.`);
        break;
    }
  };

  const focusInput = (event: MouseEvent<HTMLDivElement>) => {
    if (mode !== "ask" || isInteractiveTarget(event.target)) return;
    inputRef.current?.focus();
  };

  return (
    <div
      onClick={focusInput}
      className="glass-panel flex flex-col flex-1 min-h-0 max-w-4xl w-full mx-auto border border-border rounded-2xl overflow-hidden"
    >
      <header className="border-b border-border px-4 py-4 sm:px-6">
        <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-3">
          <div className="flex items-center gap-3">
            <svg aria-hidden="true" viewBox="0 0 48 48" className="size-10 shrink-0">
              <rect width="48" height="48" rx="12" fill="#141c34" />
              <path d="m13 17 8 7-8 7m12 0h10" fill="none" stroke="#a6baff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <div>
              <h1 className="text-xl font-semibold tracking-tight">DevMind</h1>
              <p className="text-xs text-muted">{formatStatsLine(stats, statsError)}</p>
            </div>
          </div>
          <ModeSelector activeMode={mode} onSelect={setMode} />
        </div>
        {(debug || (askScope && mode === "ask")) && (
          <div className="mt-3 flex flex-wrap items-center gap-2">
            {debug && (
              <span className="text-xs px-1.5 py-0.5 border border-accent text-accent rounded-sm tracking-widest">
                DEBUG
              </span>
            )}
            {askScope && mode === "ask" && (
              <button
                type="button"
                onClick={clearAskScope}
                className="text-xs px-1.5 py-0.5 border border-border-strong text-muted hover:text-accent rounded-sm tracking-widest transition-colors"
                title="Remover escopo"
              >
                {askScope.documentTitle ?? askScope.topicTitle ?? askScope.moduleTitle} ✕
              </button>
            )}
          </div>
        )}
      </header>

      <div ref={logRef} className="flex-1 min-h-0 overflow-y-auto px-4 py-4 sm:px-6 flex flex-col gap-3 text-sm">
        <div hidden={mode !== "study"}>
          <Study active={mode === "study"} modules={guide.modules ?? []} />
        </div>
        {mode === "study" ? null : mode === "guide" ? (
          <Guide path={guidePath} onNavigate={setGuidePath} onAskAbout={handleAskAbout} />
        ) : entries.length === 0 ? (
          <div className="my-auto w-full py-5 sm:px-4">
            <p className="font-mono text-xs tracking-widest text-accent uppercase">Assistente de estudos</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-tight sm:text-4xl">O que você quer aprender?</h2>
            <p className="mt-3 max-w-lg text-sm leading-relaxed text-muted">
              Faça uma pergunta de programação e confira as seções da base que sustentam a resposta.
            </p>
            <ul className="mt-6 grid gap-2 sm:grid-cols-3">
              {EXAMPLES.map(({ topic, question }) => (
                <li key={topic}>
                  <button
                    type="button"
                    onClick={() => runQuery(question, { echo: question, scope: null })}
                    className="h-full w-full rounded-xl border border-border bg-surface/90 px-3 py-3 text-left text-sm leading-snug hover:border-accent focus-visible:outline-accent"
                  >
                    <span className="mb-1 block font-mono text-xs text-accent">{topic}</span>
                    {question}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div role="log" aria-label="Conversa" className="flex flex-col gap-3">
            {entries.map((entry) => <TerminalEntry key={entry.id} entry={entry} debug={debug} />)}
          </div>
        )}
      </div>

      <div className="p-3 sm:p-4" hidden={mode === "study"}>
        <div className="glass-panel-raised flex flex-col gap-2 rounded-xl border border-border-strong px-3 py-2">
          <CommandInput key={inputSession} ref={inputRef} onSubmit={handleSubmit} />
          <div className="flex flex-wrap items-center justify-between gap-2 border-t border-border pt-2 text-xs text-muted">
            <span>Enter para enviar · /help para comandos</span>
            <button
              type="button"
              onClick={clearConversation}
              className="rounded px-1 py-1 text-muted hover:text-foreground focus-visible:outline-accent"
            >
              Limpar conversa
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
