// Contenu de l'accueil. Ce fichier choisit QUOI montrer (choix éditorial, assumé et regroupé ici) ;
// tous les chiffres viennent des JSON publiés par l'ETL : rien n'est calculé ni écrit à la main.
import { getIndicator, listIndicators } from "./data";
import { SCALE_LABELS } from "./format";
import { SCALES, type Confidence, type Indicator, type Scale, type Trend } from "./schema";

const load = ([scale, id]: readonly [Scale, string]) => getIndicator(scale, id);

/** Une série de température par échelle, toutes en écart à la même référence. */
const TEMPERATURE: readonly (readonly [Scale, string])[] = [
  ["gironde", "tm-annuelle-gironde"],
  ["france", "tm-france"],
  ["monde", "temperature-hadcrut5-monde"],
];

// Pente publiée par l'ETL sur la même fenêtre pour les trois séries (etl/indicators/comparaison.py).
// Seule tendance que l'accueil met en regard d'une échelle à l'autre : les tendances mises en avant ne couvrent pas la même période.
const COMPARISON_LABEL = "comparaison entre échelles";

function comparisonTrend(ind: Indicator): Trend {
  const t = ind.alt_trends.find((a) => a.label.includes(COMPARISON_LABEL));
  if (!t) throw new Error(`Accueil : ${ind.id} ne publie pas de tendance de comparaison entre échelles`);
  return t;
}

export type ScaleSeries = {
  key: Scale;
  name: string;
  href: string;
  color: string;
  years: number[];
  value: (number | null)[];
  raw: boolean[];
  trend: { start: number; end: number; fittedStart: number; fittedEnd: number; slope: number; significant: boolean };
};

export function temperatureByScale(): { reference: string; unit: string; first: number; last: number; period: string; series: ScaleSeries[] } {
  const inds = TEMPERATURE.map(load).filter((i): i is Indicator => i !== undefined);
  const ref = inds[0]?.reference_period;
  if (!ref) throw new Error("Accueil : aucune série de température à référence publiée");
  // Comparer des écarts n'a de sens qu'à référence et unité identiques : sinon le build échoue, l'accueil ne ment pas.
  for (const i of inds) {
    const r = i.reference_period;
    if (!r || r.start !== ref.start || r.end !== ref.end || i.unit !== inds[0]!.unit) {
      throw new Error(`Accueil : ${i.id} n'a pas la même référence ou la même unité que ${inds[0]!.id}`);
    }
  }
  // Même règle pour la fenêtre : des pentes sur des périodes différentes ne s'affichent pas côte à côte.
  const window0 = comparisonTrend(inds[0]!).period;
  for (const i of inds) {
    const p = comparisonTrend(i).period;
    if (p.start !== window0.start || p.end !== window0.end) throw new Error(`Accueil : ${i.id} n'a pas la même fenêtre de comparaison que ${inds[0]!.id}`);
  }
  const series = inds.map((i): ScaleSeries => {
    const t = comparisonTrend(i);
    return {
    key: i.scale,
    name: SCALE_LABELS[i.scale].name,
    href: `/${i.scale}/${i.id}`,
    color: `var(--s-${i.scale})`,
    years: i.series.time.map((t) => Number(t.slice(0, 4))),
    value: i.series.value,
    raw: i.series.time.map((_, k) => i.series.quality?.[k] === "raw"),
    trend: { start: t.period.start, end: t.period.end, fittedStart: t.fitted_start, fittedEnd: t.fitted_end, slope: t.slope_per_decade, significant: t.significant },
    };
  });
  return {
    reference: `${ref.start}-${ref.end}`,
    unit: inds[0]!.unit,
    first: Math.min(...series.flatMap((s) => s.years)),
    last: Math.max(...series.flatMap((s) => s.years)),
    period: `${window0.start}-${window0.end}`,
    series,
  };
}

// `slope` pour les écarts : une année isolée est trop bruitée pour servir de chiffre de tête.
// `last` pour un niveau qui se lit directement (ppm).
// `compare` : les deux températures, côte à côte, sur la fenêtre de comparaison entre échelles.
const FEATURED: readonly { at: readonly [Scale, string]; label: string; show: "slope" | "last"; compare?: boolean }[] = [
  { at: ["gironde", "tm-annuelle-gironde"], label: "Température en Gironde", show: "slope", compare: true },
  { at: ["monde", "temperature-hadcrut5-monde"], label: "Température mondiale", show: "slope", compare: true },
  { at: ["monde", "co2-monde"], label: "CO₂ atmosphérique", show: "last" },
  { at: ["monde", "niveau-mer-monde"], label: "Niveau de la mer", show: "slope" },
];

export function featuredIndicators() {
  return FEATURED.flatMap((f) => {
    const ind = load(f.at);
    return ind ? [{ ind, trend: f.compare ? comparisonTrend(ind) : ind.trend, label: f.label, show: f.show, href: `/${ind.scale}/${ind.id}` }] : [];
  });
}

// Volontairement mêlés : un constat établi et des constats qui ne le sont pas, tels que publiés.
const FINDINGS: readonly (readonly [Scale, string])[] = [
  ["monde", "banquise-arctique-septembre-monde"],
  ["gironde", "rr-cumul-gironde"],
  ["monde", "ouragans-monde"],
];

export function publishedFindings() {
  return FINDINGS.map(load)
    .filter((i): i is Indicator => i !== undefined)
    .map((ind) => ({ ind, href: `/${ind.scale}/${ind.id}` }));
}

export const CONFIDENCE_ORDER: Confidence[] = ["elevee", "moyenne", "faible", "non_etabli"];

export function confidenceByScale() {
  return SCALES.map((scale) => {
    const items = listIndicators(scale);
    return {
      scale,
      name: SCALE_LABELS[scale].name,
      total: items.length,
      counts: CONFIDENCE_ORDER.map((level) => ({ level, n: items.filter((e) => e.confidence === level).length })),
    };
  }).filter((r) => r.total > 0);
}
