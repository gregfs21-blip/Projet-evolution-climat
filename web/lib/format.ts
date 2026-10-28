import type { Confidence, Scale } from "./schema";

export const REPO_URL = "https://github.com/gregfs21-blip/Projet-evolution-climat";

// `validations` : phases dont le rapport de validation couvre cette échelle (data/processed/validation-<phase>.json).
export const SCALE_LABELS: Record<Scale, { name: string; blurb: string; phase: string; phaseCode: string; validations: string[] }> = {
  gironde: {
    name: "Gironde",
    blurb: "Stations longues de Météo-France, réanalyse ERA5, littoral et impacts locaux.",
    phase: "phases 1 à 4",
    phaseCode: "P1-P4",
    validations: ["p1", "p2a", "p2b", "p3", "p4"],
  },
  france: {
    name: "France",
    blurb: "Indicateur thermique national et tendances station par station.",
    phase: "phase 5",
    phaseCode: "P5",
    validations: [],
  },
  monde: {
    name: "Monde",
    blurb: "Gaz à effet de serre, températures globales, océans, cryosphère, bilan énergétique.",
    phase: "phase 6",
    phaseCode: "P6",
    validations: [],
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

const signed1 = new Intl.NumberFormat("fr-FR", { signDisplay: "always", maximumFractionDigits: 1, minimumFractionDigits: 1 });
const plain1 = new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 1, minimumFractionDigits: 1 });

export const fmtSigned = (v: number) => signed.format(v);
export const fmt = (v: number) => plain.format(v);
export const fmtSigned1 = (v: number) => signed1.format(v);
export const fmt1 = (v: number) => plain1.format(v);

export function fmtPValue(p: number): string {
  if (p < 0.001) return "p < 0,001";
  return `p = ${new Intl.NumberFormat("fr-FR", { maximumSignificantDigits: 2 }).format(p)}`;
}

export function fmtDateTime(iso: string): string {
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "long", timeStyle: "short", timeZone: "Europe/Paris" }).format(
    new Date(iso),
  );
}
