import type { Mode } from "./types";

export const KNOWN_COMMANDS = [
  "/help",
  "/ask",
  "/guide",
  "/sources",
  "/clear",
  "/mode",
  "/about",
] as const;

export type CommandName = (typeof KNOWN_COMMANDS)[number];

export type ParsedCommand =
  | { type: "help" }
  | { type: "clear" }
  | { type: "about" }
  | { type: "sources" }
  | { type: "mode"; mode: Mode | null }
  | { type: "ask"; question: string }
  | { type: "guide"; args: string[] }
  | { type: "question"; question: string }
  | { type: "unknown"; raw: string };

const MODES: Mode[] = ["ask", "guide"];

function isMode(value: string): value is Mode {
  return (MODES as string[]).includes(value);
}

/**
 * Parseia uma linha de entrada do terminal. Reconhece os comandos com `/`
 * e trata qualquer outro texto não vazio como uma pergunta direta (equivalente
 * a `/ask <texto>`), conforme pede o design de UX.
 */
export function parseCommand(raw: string): ParsedCommand {
  const input = raw.trim();
  if (!input) return { type: "unknown", raw };

  if (!input.startsWith("/")) {
    return { type: "question", question: input };
  }

  const [command, ...rest] = input.split(/\s+/);
  const arg = rest.join(" ").trim();

  switch (command.toLowerCase()) {
    case "/help":
      return { type: "help" };
    case "/clear":
      return { type: "clear" };
    case "/about":
      return { type: "about" };
    case "/sources":
      return { type: "sources" };
    case "/mode":
      return { type: "mode", mode: isMode(arg.toLowerCase()) ? (arg.toLowerCase() as Mode) : null };
    case "/ask":
      return { type: "ask", question: arg };
    case "/guide":
      return { type: "guide", args: rest };
    default:
      return { type: "unknown", raw: input };
  }
}

export const HELP_TEXT = [
  "COMANDOS",
  "",
  "/ask <pergunta>       faz uma pergunta à base",
  "/guide                abre o guia de estudos",
  "/guide <módulo>       abre um módulo (por exemplo, devmind)",
  "/guide <módulo> <tema>  abre um tema dentro do módulo",
  "/sources              mostra as fontes da última resposta",
  "/mode [ask|guide]     mostra ou alterna o modo",
  "/clear                limpa a conversa",
  "/about                mostra informações do projeto",
  "/help                 mostra esta lista",
  "",
  "Você também pode escrever uma pergunta diretamente.",
].join("\n");

export const ABOUT_TEXT = [
  "DEVMIND",
  "",
  "Um assistente de estudos de programação com busca no Pinecone,",
  "respostas geradas com OpenAI e referências para conferir.",
  "",
  "Chat: perguntas com fontes citadas.",
  "Guia: navegação por módulo, tema e documento.",
  "",
  "Construído com Next.js, TypeScript, Tailwind CSS e React Three Fiber.",
].join("\n");
