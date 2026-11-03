"use client";

// Recherche d'un indicateur par mots du titre, sans accents ni casse. La liste vient du manifeste, au build.
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useId, useMemo, useState } from "react";

export type SearchItem = { title: string; scale: string; href: string };

const norm = (s: string) => s.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();

export default function SearchBox({ items }: { items: SearchItem[] }) {
  const router = useRouter();
  const listId = useId();
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);

  const index = useMemo(() => items.map((it) => ({ it, key: norm(`${it.title} ${it.scale}`) })), [items]);
  const results = useMemo(() => {
    const words = norm(q).split(/\s+/).filter(Boolean);
    if (words.length === 0) return [];
    return index.filter((e) => words.every((w) => e.key.includes(w))).slice(0, 8).map((e) => e.it);
  }, [index, q]);

  const close = () => {
    setOpen(false);
    setQ("");
  };

  return (
    <div className="relative" onBlur={(e) => !e.currentTarget.contains(e.relatedTarget) && setOpen(false)}>
      <input
        type="search"
        role="combobox"
        aria-expanded={open && q !== ""}
        aria-controls={listId}
        aria-label="Rechercher un indicateur"
        placeholder="Rechercher…"
        value={q}
        onChange={(e) => {
          setQ(e.target.value);
          setActive(0);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={(e) => {
          if (e.key === "Escape") close();
          if (e.key === "ArrowDown") {
            e.preventDefault();
            setActive((a) => Math.min(results.length - 1, a + 1));
          }
          if (e.key === "ArrowUp") {
            e.preventDefault();
            setActive((a) => Math.max(0, a - 1));
          }
          const hit = results[active];
          if (e.key === "Enter" && hit) {
            router.push(hit.href);
            close();
          }
        }}
        className="w-full rounded-full border border-[var(--rule)] bg-[var(--card)] px-3.5 py-1.5 text-sm placeholder:text-[var(--muted)]"
      />
      {open && q !== "" && (
        <ul id={listId} className="card absolute left-0 z-50 mt-1 max-h-96 w-[min(26rem,calc(100vw-2rem))] overflow-auto py-1 text-sm">
          {results.length === 0 && <li className="px-3 py-2 text-[var(--muted)]">Aucun indicateur ne contient ces mots.</li>}
          {results.map((r, i) => (
            <li key={r.href}>
              <Link
                href={r.href}
                onClick={close}
                onMouseEnter={() => setActive(i)}
                className={`block px-3 py-1.5 ${i === active ? "bg-[var(--hover)]" : ""}`}
              >
                {r.title} <span className="text-xs text-[var(--muted)]">{r.scale}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
