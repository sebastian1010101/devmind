import type { Source } from "@/lib/types";

export function Sources({ sources, debug = false }: { sources: Source[]; debug?: boolean }) {
  if (!sources.length) return null;

  return (
    <details className="mt-3 border-t border-border pt-3">
      <summary className="cursor-pointer rounded-sm text-xs font-medium text-accent focus-visible:outline-accent">
        Fontes citadas ({sources.length})
      </summary>
      <ul className="mt-2 grid gap-2">
        {sources.map((item) => (
          <li
            key={JSON.stringify([item.source, item.section])}
            className="rounded-lg border border-border bg-surface-raised p-3 text-xs wrap-anywhere"
          >
            <p className="font-medium text-foreground">{item.section}</p>
            <p className="mt-1 font-mono text-muted">knowledge/{item.source}</p>
            <p className="mt-2 whitespace-pre-line leading-relaxed text-foreground/80">{item.excerpt}</p>
            {debug && <p className="mt-2 text-muted">Fragmento {item.chunk_id} · similaridade {item.score.toFixed(4)}</p>}
          </li>
        ))}
      </ul>
    </details>
  );
}
