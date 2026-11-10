"use client";

import type { GuideModule } from "@/lib/types";

type GuideBreadcrumbsProps = {
  module?: GuideModule;
  sectionTitle?: string;
  documentTitle?: string;
  onNavigateHome: () => void;
  onNavigateModule: () => void;
  onNavigateSection: () => void;
};

/** `GUIDE > MODULE > SECTION > DOCUMENT`, com cada parte clicável exceto a
 * última (nível atual). */
export function GuideBreadcrumbs({
  module,
  sectionTitle,
  documentTitle,
  onNavigateHome,
  onNavigateModule,
  onNavigateSection,
}: GuideBreadcrumbsProps) {
  const crumbs: { label: string; onClick?: () => void }[] = [{ label: "GUIDE", onClick: onNavigateHome }];
  if (module) crumbs.push({ label: module.title.toUpperCase(), onClick: sectionTitle ? onNavigateModule : undefined });
  if (sectionTitle) crumbs.push({ label: sectionTitle.toUpperCase(), onClick: documentTitle ? onNavigateSection : undefined });
  if (documentTitle) crumbs.push({ label: documentTitle.toUpperCase() });

  return (
    <nav aria-label="Breadcrumbs" className="flex items-center gap-1.5 text-xs tracking-widest flex-wrap">
      {crumbs.map((crumb, index) => (
        <span key={`${crumb.label}-${index}`} className="flex items-center gap-1.5">
          {index > 0 && <span className="text-muted">&gt;</span>}
          {crumb.onClick ? (
            <button
              type="button"
              onClick={crumb.onClick}
              className="text-muted hover:text-accent transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent rounded-sm"
            >
              {crumb.label}
            </button>
          ) : (
            <span className="text-accent">{crumb.label}</span>
          )}
        </span>
      ))}
    </nav>
  );
}
