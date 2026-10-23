"use client";

// Liens du menu : page courante soulignée, rubriques sans contenu grisées avec leur phase.
import Link from "next/link";
import { usePathname } from "next/navigation";

export type NavItem = { href: string; label: string; soon: string | null };

export default function NavLinks({ items }: { items: NavItem[] }) {
  const path = usePathname();
  return (
    <>
      {items.map((n) => {
        const active = path === n.href || path.startsWith(`${n.href}/`);
        return (
          <Link
            key={n.href}
            href={n.href}
            aria-current={active ? "page" : undefined}
            title={n.soon ? `À venir (${n.soon})` : undefined}
            className={`text-sm ${
              active
                ? "border-b-2 border-[var(--warm)] pb-0.5 font-medium text-[var(--ink)]"
                : n.soon
                  ? "text-[var(--muted)] opacity-60 hover:opacity-100"
                  : "text-[var(--muted)] hover:text-[var(--ink)]"
            }`}
          >
            {n.label}
            {n.soon && (
              <span className="ml-1 rounded-full border border-[var(--rule)] px-1.5 align-[1px] text-[10px]">{n.soon}</span>
            )}
          </Link>
        );
      })}
    </>
  );
}
