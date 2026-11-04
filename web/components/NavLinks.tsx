"use client";

// Navigation : pastilles dans l'en-tête sur grand écran, barre d'onglets en bas sinon.
// Rubriques sans contenu grisées avec leur phase : le menu ne promet pas ce que le site n'a pas encore.
import Link from "next/link";
import { usePathname } from "next/navigation";

export type NavItem = { href: string; label: string; soon: string | null; icon: IconName };
export type IconName = keyof typeof ICONS;

const ICONS = {
  home: "M3 10.5 10 4l7 6.5M5 9v7h4v-4h2v4h4V9",
  pin: "M10 18s-5.5-5-5.5-9.2A5.5 5.5 0 0 1 10 3a5.5 5.5 0 0 1 5.5 5.8C15.5 13 10 18 10 18ZM10 10.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z",
  map: "M3 5.5 7.5 4l5 2L17 4.5v10L12.5 16l-5-2L3 15.5v-10ZM7.5 4v10M12.5 6v10",
  globe: "M10 17.5a7.5 7.5 0 1 0 0-15 7.5 7.5 0 0 0 0 15ZM2.5 10h15M10 2.5c2.2 2 3.2 4.6 3.2 7.5s-1 5.5-3.2 7.5c-2.2-2-3.2-4.6-3.2-7.5s1-5.5 3.2-7.5Z",
  grid: "M3.5 3.5h5.5v5.5H3.5zM11 3.5h5.5v5.5H11zM3.5 11h5.5v5.5H3.5zM11 11h5.5v5.5H11z",
  doc: "M5 2.5h7l3.5 3.5v11.5H5V2.5ZM7.5 9.5h5M7.5 12.5h5",
  ruler: "M3 13.5 13.5 3 17 6.5 6.5 17 3 13.5ZM6.5 10l1.8 1.8M9 7.5l1.8 1.8M11.5 5l1.8 1.8",
  more: "M4.5 10h.01M10 10h.01M15.5 10h.01",
};

function Icon({ name }: { name: IconName }) {
  return (
    <svg viewBox="0 0 20 20" className="h-5 w-5 shrink-0" fill="none" stroke="currentColor" strokeWidth={name === "more" ? 2.6 : 1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d={ICONS[name]} />
    </svg>
  );
}

const isActive = (path: string, href: string) => (href === "/" ? path === "/" : path === href || path.startsWith(`${href}/`));

function Soon({ code }: { code: string }) {
  return <span className="rounded-full border border-[var(--rule)] px-1.5 text-[10px] leading-4">{code}</span>;
}

export function TopNav({ items }: { items: NavItem[] }) {
  const path = usePathname();
  return (
    <ul className="no-scrollbar flex items-center gap-0.5 overflow-x-auto p-0.5 xl:gap-1">
      {items.map((n) => {
        const active = isActive(path, n.href);
        return (
          <li key={n.href} className="shrink-0">
            <Link
              href={n.href}
              aria-current={active ? "page" : undefined}
              title={n.soon ? `À venir (${n.soon})` : undefined}
              className={`inline-flex h-9 items-center gap-1.5 whitespace-nowrap rounded-full px-2.5 text-sm font-medium transition-colors xl:h-10 xl:px-3.5 xl:text-[15px] ${
                active
                  ? "bg-[var(--primary)] text-[var(--primary-ink)]"
                  : n.soon
                    ? "text-[var(--muted)] hover:bg-[var(--hover)]"
                    : "hover:bg-[var(--hover)]"
              }`}
            >
              {n.label}
              {n.soon && <Soon code={n.soon} />}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

const tabClass = (active: boolean) =>
  `flex w-full flex-col items-center gap-0.5 py-2 text-[11px] ${active ? "font-medium text-[var(--primary)]" : "text-[var(--muted)]"}`;

/** `tabs` : onglets directs ; `more` : le reste, replié derrière « Plus ». */
export function TabBar({ tabs, more }: { tabs: NavItem[]; more: NavItem[] }) {
  const path = usePathname();
  const moreActive = more.some((n) => isActive(path, n.href));
  return (
    <ul className="flex items-stretch">
      {tabs.map((n) => {
        const active = isActive(path, n.href);
        return (
          <li key={n.href} className="flex-1">
            <Link href={n.href} aria-current={active ? "page" : undefined} className={tabClass(active)}>
              <Icon name={n.icon} />
              {n.label}
            </Link>
          </li>
        );
      })}
      <li className="flex-1">
        {/* `key` : le menu se referme à chaque changement de page. */}
        <details key={path} className="relative">
          <summary className={`${tabClass(moreActive)} cursor-pointer`}>
            <Icon name="more" />
            Plus
          </summary>
          <ul className="card absolute right-2 bottom-full mb-2 w-52 py-1 text-sm">
            {more.map((n) => (
              <li key={n.href}>
                <Link href={n.href} aria-current={isActive(path, n.href) ? "page" : undefined} className="flex items-center gap-3 px-3 py-2 hover:bg-[var(--hover)]">
                  <Icon name={n.icon} />
                  <span className="mr-auto">{n.label}</span>
                  {n.soon && <Soon code={n.soon} />}
                </Link>
              </li>
            ))}
          </ul>
        </details>
      </li>
    </ul>
  );
}
