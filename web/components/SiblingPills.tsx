// Navigation latérale : même lieu / autre variable, même variable / autre lieu.
import Link from "next/link";

import type { Sibling } from "@/lib/family";

function Group({ label, items }: { label: string; items: Sibling[] }) {
  if (items.length < 2) return null;
  return (
    <div className="flex flex-wrap items-center gap-1.5">
      <span className="mr-1 text-xs text-[var(--muted)]">{label}</span>
      {items.map((s) => {
        const base = "rounded-full border px-3 py-0.5 text-sm";
        if (s.active) {
          return (
            <span key={s.key} aria-current="page" className={`${base} border-[var(--ink)] bg-[var(--ink)] text-[var(--paper)]`}>
              {s.label}
            </span>
          );
        }
        if (!s.href) {
          return (
            <span key={s.key} title="Pas de série pour ce lieu" className={`${base} border-dashed border-[var(--rule)] text-[var(--muted)] opacity-60`}>
              {s.label}
            </span>
          );
        }
        return (
          <Link key={s.key} href={s.href} className={`${base} border-[var(--rule)] bg-[var(--card)] hover:border-[var(--muted)]`}>
            {s.label}
          </Link>
        );
      })}
    </div>
  );
}

export default function SiblingPills({ variables, places }: { variables: Sibling[]; places: Sibling[] }) {
  return (
    <nav aria-label="Autres séries" className="flex flex-wrap gap-x-6 gap-y-2">
      <Group label="Variable" items={variables} />
      <Group label="Lieu" items={places} />
    </nav>
  );
}
