import type { AskScope, Source } from "@/lib/types";
import { Answer } from "./Answer";
import { LoadingDots } from "./LoadingDots";
import { Sources } from "./Sources";

export type TerminalEntryData =
  | { id: string; kind: "command"; content: string }
  | { id: string; kind: "system" | "output" | "error"; content: string }
  | { id: string; kind: "loading"; content: string }
  | {
      id: string;
      kind: "answer";
      content: string;
      sources: Source[];
      latencyMs?: number;
      scope?: AskScope | null;
    };

const TEXT_STYLES: Record<"command" | "system" | "output" | "error", string> = {
  command: "text-foreground",
  output: "text-muted",
  system: "text-accent",
  error: "text-danger",
};

type TerminalEntryProps = {
  entry: TerminalEntryData;
  debug?: boolean;
};

export function TerminalEntry({ entry, debug = false }: TerminalEntryProps) {
  if (entry.kind === "command") {
    return (
      <p className="max-w-[90%] self-end rounded-xl border border-border bg-accent/12 px-4 py-2.5 whitespace-pre-wrap wrap-anywhere leading-relaxed text-foreground">
        {entry.content}
      </p>
    );
  }

  if (entry.kind === "answer") {
    return (
      <article className="rounded-xl border border-border bg-surface/90 p-4">
        <div className="flex items-center gap-2 mb-1.5">
          <p className="text-xs font-semibold tracking-wide text-accent">DevMind</p>
          {entry.scope && (
            <p className="text-xs text-muted">
              · scope: {entry.scope.moduleTitle}
              {entry.scope.topicTitle ? ` / ${entry.scope.topicTitle}` : ""}
            </p>
          )}
          {debug && (
            <p className="text-xs text-muted">
              · {entry.latencyMs ?? "—"} ms
            </p>
          )}
        </div>
        <Answer content={entry.content} />
        <Sources sources={entry.sources} debug={debug} />
      </article>
    );
  }

  if (entry.kind === "loading") {
    return (
      <p className="flex items-center text-muted" role="status">
        {entry.content}
        <LoadingDots />
      </p>
    );
  }

  return (
    <p role={entry.kind === "error" ? "alert" : undefined} className={`whitespace-pre-wrap wrap-anywhere leading-relaxed ${TEXT_STYLES[entry.kind]}`}>
      {entry.content}
    </p>
  );
}
