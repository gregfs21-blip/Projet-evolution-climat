"use client";

// Boutons de thème d'une page d'échelle : chacun mène à sa propre page (adresse partageable, bouton retour du navigateur).
// Grand écran : boutons sur plusieurs lignes. Mobile : une ligne qui défile, collée en haut, le bouton actif centré.
import Link from "next/link";
import { useEffect, useRef } from "react";

export type ThemeTab = { id: string; label: string; href: string };

export default function ThemeTabs({ tabs, active }: { tabs: ThemeTab[]; active: string }) {
  const list = useRef<HTMLUListElement>(null);

  useEffect(() => {
    const box = list.current;
    const el = box?.querySelector<HTMLElement>('[aria-current="page"]');
    if (box && el) box.scrollLeft = el.offsetLeft - (box.clientWidth - el.offsetWidth) / 2;
  }, [active]);

  return (
    <nav aria-label="Thèmes" className="sticky top-0 z-30 -mx-4 bg-[var(--paper)] px-4 py-2 sm:static sm:mx-0 sm:bg-transparent sm:p-0">
      <ul ref={list} className="no-scrollbar relative flex gap-1.5 overflow-x-auto sm:flex-wrap sm:overflow-visible">
        {tabs.map((t) => {
          const on = t.id === active;
          return (
            <li key={t.id} className="shrink-0">
              <Link
                href={t.href}
                aria-current={on ? "page" : undefined}
                className={`block rounded-full border px-3.5 py-1.5 text-sm ${
                  on
                    ? "border-[var(--primary)] bg-[var(--primary)] font-medium text-[var(--primary-ink)]"
                    : "border-[var(--rule)] bg-[var(--card)] hover:border-[var(--primary)]"
                }`}
              >
                {t.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
