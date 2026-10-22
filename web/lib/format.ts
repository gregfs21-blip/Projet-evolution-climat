import type { Confidence, Scale } from "./schema";

export const SCALE_LABELS: Record<Scale, { name: string; blurb: string; phase: string }> = {
  gironde: {
    name: "Gironde",
    blurb: "Stations longues de Météo-France, réanalyse ERA5, littoral et impacts locaux.",
    phase: "phases 1 à 4",
  },
  france: {
    name: "France",
    blurb: "Indicateur thermique national et tendances station par station.",
    phase: "phase 5",
  },
  monde: {
    name: "Monde",
    blurb: "Gaz à effet de serre, températures globales, océans, cryosphère, bilan énergétique.",
    phase: "phase 6",
  },
};

export const CONFIDENCE_LABELS: Record<Confidence, string> = {
  elevee: "Confiance élevée",
  moyenne: "Confiance moyenne",
  faible: "Confiance faible",
  non_etabli: "Signal non établi",
};

const signed = new Intl.NumberFormat("fr-FR", { signDisplay: "always", maximumFractionDigits: 2, minimumFractionDigits: 2 });
const plain = new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 2, minimumFractionDigits: 2 });

export const fmtSigned = (v: number) => signed.format(v);
export const fmt = (v: number) => plain.format(v);

export function fmtPValue(p: number): string {
  if (p < 0.001) return "p < 0,001";
  return `p = ${new Intl.NumberFormat("fr-FR", { maximumSignificantDigits: 2 }).format(p)}`;
}

export function fmtDateTime(iso: string): string {
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "long", timeStyle: "short", timeZone: "Europe/Paris" }).format(
    new Date(iso),
  );
}
