"use client";

import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";

const components: Components = {
  h1: (props) => <h1 className="text-base font-semibold mt-2 mb-1 text-foreground" {...props} />,
  h2: (props) => <h2 className="text-sm font-semibold mt-2 mb-1 text-foreground" {...props} />,
  h3: (props) => <h3 className="text-sm font-semibold mt-2 mb-1 text-muted" {...props} />,
  p: (props) => <p className="mb-2 last:mb-0" {...props} />,
  ul: (props) => <ul className="list-disc pl-5 mb-2 space-y-1" {...props} />,
  ol: (props) => <ol className="list-decimal pl-5 mb-2 space-y-1" {...props} />,
  li: (props) => <li {...props} />,
  strong: (props) => <strong className="text-foreground font-semibold" {...props} />,
  pre: (props) => <pre className="my-2 overflow-x-auto" {...props} />,
  table: (props) => <table className="border border-border text-xs my-2 w-full" {...props} />,
  th: (props) => <th className="border border-border px-2 py-1 text-left text-muted" {...props} />,
  td: (props) => <td className="border border-border px-2 py-1" {...props} />,
  code: ({ className, children, ...rest }) => {
    const isFenced = Boolean(className);
    if (isFenced) {
      return (
        <code
          className={`block whitespace-pre-wrap rounded-sm bg-surface-raised border border-border px-3 py-2 my-2 text-xs ${className ?? ""}`}
          {...rest}
        >
          {children}
        </code>
      );
    }
    return (
      <code className="rounded-sm bg-surface-raised border border-border px-1 py-0.5 text-xs text-accent" {...rest}>
        {children}
      </code>
    );
  },
};

const documentComponents: Components = {
  ...components,
  a: ({ href, children }) => {
    if (!href || !/^https?:\/\//i.test(href)) return <>{children}</>;
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className="text-accent underline">
        {children}
      </a>
    );
  },
  pre: ({ children }) => (
    <pre className="my-3 overflow-x-auto whitespace-pre rounded-sm border border-border bg-surface-raised px-3 py-2 [&>code]:p-0 [&>code]:text-inherit" tabIndex={0}>
      {children}
    </pre>
  ),
  code: ({ className, children }) => (
    <code className={`rounded-sm bg-surface-raised px-1 py-0.5 text-xs text-accent ${className ?? ""}`}>
      {children}
    </code>
  ),
  table: ({ children }) => (
    <div className="my-3 overflow-x-auto" tabIndex={0}>
      <table className="w-full border border-border text-xs">{children}</table>
    </div>
  ),
};

export function MarkdownContent({
  content,
  variant = "answer",
}: {
  content: string;
  variant?: "answer" | "document";
}) {
  const isDocument = variant === "document";
  return (
    <div className="text-sm text-foreground leading-relaxed wrap-anywhere">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={isDocument ? documentComponents : components}
        disallowedElements={isDocument ? ["img"] : ["img", "a"]}
        unwrapDisallowed
        skipHtml
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
