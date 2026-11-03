import type { Metadata } from "next";
import { IBM_Plex_Sans } from "next/font/google";
import Link from "next/link";

import { RailNav, TabBar, type IconName, type NavItem } from "@/components/NavLinks";
import SearchBox from "@/components/SearchBox";
import { getManifest, listIndicators } from "@/lib/data";
import { fmtDateTime, SCALE_LABELS } from "@/lib/format";
import { anomalyColor } from "@/lib/heat";
import { SCALES, type Scale } from "@/lib/schema";
import "./globals.css";

const sans = IBM_Plex_Sans({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-plex-sans" });

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
      { href: "/synthese", label: "Synthèse", soon: null, icon: "doc" },
      { href: "/methode", label: "Méthode", soon: null, icon: "ruler" },
    ],
  };
}

// Le logo reprend le motif du site : bandes d'écart de température, du froid au chaud.
function Brand() {
  return (
    <Link href="/" className="flex items-center gap-2.5 font-semibold leading-tight tracking-tight">
      <span className="flex h-8 w-8 shrink-0 overflow-hidden rounded-lg" aria-hidden>
        {[-2, -1, -0.25, 0.5, 1.5, 2.6].map((v) => (
          <i key={v} className="block flex-1" style={{ background: anomalyColor(v) }} />
        ))}
      </span>
      <span>
        Évolution
        <br />
        climatique
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
    <html lang="fr" className={sans.variable}>
      <body className="min-h-screen md:grid md:grid-cols-[15rem_minmax(0,1fr)]">
        <aside className="sticky top-0 hidden h-screen flex-col gap-5 overflow-y-auto border-r border-[var(--rule)] bg-[var(--rail)] p-4 md:flex">
          <Brand />
          <SearchBox items={items} />
          <nav aria-label="Navigation principale">
            <RailNav items={[...tabs, ...more]} />
          </nav>
          <div className="mt-auto">
            <Freshness />
          </div>
        </aside>

        <div className="min-w-0">
          <header className="flex items-center gap-4 border-b border-[var(--rule)] bg-[var(--rail)] px-4 py-3 md:hidden">
            <Brand />
            <div className="min-w-0 flex-1">
              <SearchBox items={items} />
            </div>
          </header>
          <main className="mx-auto max-w-[72rem] px-4 pt-5 pb-8 md:px-8 md:pt-8">{children}</main>
          <footer className="mx-auto max-w-[72rem] border-t border-[var(--rule)] px-4 pt-4 pb-24 md:hidden">
            <Freshness />
          </footer>
        </div>

        <nav aria-label="Navigation principale" className="fixed inset-x-0 bottom-0 z-40 border-t border-[var(--rule)] bg-[var(--rail)] pb-[env(safe-area-inset-bottom)] md:hidden">
          <TabBar tabs={tabs} more={more} />
        </nav>
      </body>
    </html>
  );
}
