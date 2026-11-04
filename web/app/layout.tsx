import type { Metadata } from "next";
import Link from "next/link";

import { TabBar, TopNav, type IconName, type NavItem } from "@/components/NavLinks";
import SearchBox from "@/components/SearchBox";
import { getManifest, listIndicators } from "@/lib/data";
import { fmtDateTime, SCALE_LABELS } from "@/lib/format";
import { anomalyColor } from "@/lib/heat";
import { SCALES, type Scale } from "@/lib/schema";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Évolution climatique", template: "%s · Évolution climatique" },
  description: "Évolution du climat en Gironde, en France et dans le monde, à partir de données ouvertes.",
};

const SCALE_ICONS: Record<Scale, IconName> = { gironde: "pin", france: "map", monde: "globe" };

// Une entrée sans contenu publié reste accessible mais s'affiche « à venir », avec sa phase :
// le menu ne promet pas ce que le site n'a pas encore.
function nav(): { tabs: NavItem[]; more: NavItem[] } {
  const scales = SCALES.map((s): NavItem => ({
    href: `/${s}`,
    label: SCALE_LABELS[s].name,
    soon: listIndicators(s).length === 0 ? SCALE_LABELS[s].phaseCode : null,
    icon: SCALE_ICONS[s],
  }));
  return {
    tabs: [{ href: "/", label: "Accueil", soon: null, icon: "home" }, ...scales],
    more: [
      { href: "/couverture", label: "Couverture", soon: null, icon: "grid" },
      { href: "/synthese", label: "Synthèse", soon: "P8", icon: "doc" },
      { href: "/methode", label: "Méthode", soon: null, icon: "ruler" },
    ],
  };
}

// Le logo reprend le motif du site : bandes d'écart de température, du froid au chaud.
function Brand() {
  return (
    <Link href="/" aria-label="Évolution climatique, accueil" className="flex shrink-0 items-center gap-2.5 xl:gap-3">
      <span className="flex h-9 w-9 shrink-0 overflow-hidden rounded-[11px] lg:h-[42px] lg:w-[42px]" aria-hidden>
        {[-2, -1, -0.25, 0.5, 1.5, 2.6].map((v) => (
          <i key={v} className="block flex-1" style={{ background: anomalyColor(v) }} />
        ))}
      </span>
      <span className="leading-tight">
        <span className="block max-w-[6rem] font-bold tracking-tight sm:max-w-none sm:text-[19px] lg:max-w-[6rem] lg:text-base xl:max-w-none xl:text-[19px]">Évolution climatique</span>
        <span className="hidden text-[13px] text-[var(--muted)] sm:block lg:hidden xl:block">Gironde, France, monde</span>
      </span>
    </Link>
  );
}

function Freshness() {
  const manifest = getManifest();
  return (
    <p className="text-xs text-[var(--muted)]">
      Données calculées le {fmtDateTime(manifest.generated_at)}, ETL <span className="font-mono">{manifest.etl_version}</span>. Sources ouvertes, voir{" "}
      <Link href="/methode" className="underline underline-offset-2">
        méthode
      </Link>
      .
    </p>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const { tabs, more } = nav();
  const items = getManifest().indicators.map((e) => ({ title: e.title, scale: SCALE_LABELS[e.scale].name, href: `/${e.scale}/${e.id}` }));
  return (
    <html lang="fr">
      <body className="flex min-h-screen flex-col">
        <header className="border-b border-[var(--rule)] bg-[var(--rail)] lg:sticky lg:top-0 lg:z-40">
          <div className="mx-auto flex h-16 max-w-[72rem] items-center gap-4 px-4 sm:px-6 lg:h-[76px]">
            <Brand />
            <nav aria-label="Navigation principale" className="hidden min-w-0 flex-1 lg:block">
              <TopNav items={[...tabs, ...more]} />
            </nav>
            <div className="ml-auto min-w-0 flex-1 sm:max-w-64 lg:w-40 lg:flex-none">
              <SearchBox items={items} />
            </div>
          </div>
        </header>

        <main className="mx-auto w-full max-w-[72rem] flex-1 px-4 pt-5 pb-10 sm:px-6 lg:pt-8">{children}</main>

        <footer className="border-t border-[var(--rule)] bg-[var(--rail)] pb-20 lg:pb-0">
          <div className="mx-auto max-w-[72rem] px-4 py-5 sm:px-6">
            <Freshness />
          </div>
        </footer>

        <nav aria-label="Navigation principale" className="fixed inset-x-0 bottom-0 z-40 border-t border-[var(--rule)] bg-[var(--rail)] pb-[env(safe-area-inset-bottom)] lg:hidden">
          <TabBar tabs={tabs} more={more} />
        </nav>
      </body>
    </html>
  );
}
