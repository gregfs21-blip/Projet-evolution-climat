"use client";

// Navigation d'une page d'échelle, sur deux niveaux : les familles, puis les thèmes de la famille ouverte.
// Chaque thème a sa propre page (adresse partageable, bouton retour du navigateur) ; une famille ouvre son premier thème.
// Grand écran : boutons sur plusieurs lignes. Mobile : lignes qui défilent, collées en haut, le bouton actif centré.
import Link from "next/link";
import { useEffect, useRef } from "react";

import type { Family } from "@/lib/family";

function useCentered(key: string) {
  const list = useRef<HTMLUListElement>(null);
  useEffect(() => {
    const box = list.current;
    const el = box?.querySelector<HTMLElement>("[aria-current]");
    if (box && el) box.scrollLeft = el.offsetLeft - (box.clientWidth - el.offsetWidth) / 2;
  }, [key]);
  return list;
}

const ROW = "no-scrollbar relative flex gap-1.5 overflow-x-auto sm:flex-wrap sm:overflow-visible";

export default function ThemeTabs({ scale, families, active }: { scale: string; families: Family[]; active: string }) {
  const href = (section: string) => `/${scale}/themes/${section}`;
  const family = families.find((f) => f.sections.some((s) => s.id === active));
  const showThemes = family !== undefined && family.sections.length > 1;
  const familyRow = useCentered(family?.id ?? "");
  const themeRow = useCentered(active);

  return (
    <nav aria-label="Thèmes" className="sticky top-0 z-30 -mx-4 space-y-2 bg-[var(--paper)] px-4 py-2 sm:static sm:mx-0 sm:bg-transparent sm:p-0">
      <ul ref={familyRow} aria-label="Familles" className={ROW}>
        {families.map((f) => {
          const on = f.id === family?.id;
          return (
            <li key={f.id} className="shrink-0">
              <Link
                href={href(f.sections[0]!.id)}
                aria-current={on ? (showThemes ? "true" : "page") : undefined}
                className={`block rounded-full border px-4 py-1.5 text-sm font-medium ${
                  on
                    ? "border-[var(--primary)] bg-[var(--primary)] text-[var(--primary-ink)]"
                    : "border-[var(--rule)] bg-[var(--card)] hover:border-[var(--primary)]"
                }`}
              >
                {f.label}
              </Link>
            </li>
          );
        })}
      </ul>
      {showThemes && (
        <ul ref={themeRow} aria-label={`Thèmes de la famille ${family.label}`} className={ROW}>
          {family.sections.map((s) => {
            const on = s.id === active;
            return (
              <li key={s.id} className="shrink-0">
                <Link
                  href={href(s.id)}
                  aria-current={on ? "page" : undefined}
                  className={`block rounded-full px-3 py-1 text-sm ${
                    on
                      ? "bg-[color-mix(in_srgb,var(--primary)_14%,var(--card))] font-medium text-[var(--primary)]"
                      : "text-[var(--muted)] hover:text-[var(--ink)]"
                  }`}
                >
                  {s.label}
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </nav>
  );
}
