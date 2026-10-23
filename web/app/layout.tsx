import type { Metadata } from "next";
import { IBM_Plex_Mono, IBM_Plex_Sans } from "next/font/google";
import Link from "next/link";

import NavLinks from "@/components/NavLinks";
import { getManifest, listIndicators } from "@/lib/data";
import { fmtDateTime, SCALE_LABELS } from "@/lib/format";
import { SCALES } from "@/lib/schema";
import "./globals.css";

const sans = IBM_Plex_Sans({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-plex-sans" });
const mono = IBM_Plex_Mono({ subsets: ["latin"], weight: ["400", "500"], variable: "--font-plex-mono" });

export const metadata: Metadata = {
  title: { default: "Évolution climatique", template: "%s · Évolution climatique" },
  description: "Évolution du climat en Gironde, en France et dans le monde, à partir de données ouvertes.",
};

// Une entrée sans contenu publié reste accessible mais s'affiche « à venir », avec sa phase :
// le menu ne promet pas ce que le site n'a pas encore.
function nav() {
  const scales = SCALES.map((s) => ({
    href: `/${s}`,
    label: SCALE_LABELS[s].name,
    soon: listIndicators(s).length === 0 ? SCALE_LABELS[s].phaseCode : null,
  }));
  return [
    ...scales,
    { href: "/couverture", label: "Couverture", soon: null },
    { href: "/synthese", label: "Synthèse", soon: "P8" },
    { href: "/methode", label: "Méthode", soon: null },
  ];
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const manifest = getManifest();
  return (
    <html lang="fr" className={`${sans.variable} ${mono.variable}`}>
      <body className="min-h-screen">
        <div className="stripes h-1.5" aria-hidden />
        <header className="border-b border-[var(--rule)]">
          <nav className="mx-auto flex max-w-5xl flex-wrap items-baseline gap-x-6 gap-y-2 px-4 py-4">
            <Link href="/" className="mr-auto font-semibold tracking-tight">
              Évolution climatique
            </Link>
            <NavLinks items={nav()} />
          </nav>
        </header>
        <main className="mx-auto max-w-5xl px-4 py-8">{children}</main>
        <footer className="mx-auto max-w-5xl border-t border-[var(--rule)] px-4 py-6 text-xs text-[var(--muted)]">
          Données calculées le {fmtDateTime(manifest.generated_at)} · ETL{" "}
          <span className="font-mono">{manifest.etl_version}</span> · Sources ouvertes, voir{" "}
          <Link href="/methode" className="underline underline-offset-2">
            méthode
          </Link>
          .
        </footer>
      </body>
    </html>
  );
}
