import { MarkdownContent } from "@/components/MarkdownContent";

export function Answer({ content }: { content: string }) {
  return <MarkdownContent content={content} />;
}
