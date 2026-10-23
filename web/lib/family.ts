// Familles d'indicateurs : une même variable mesurée en plusieurs lieux (stations + composite),
// regroupées par thème (variables comparables : TN, TM, TX…). C'est ce qui permet les vues comparatives
// (matrice, superposition, carte, navigation latérale) sans écrire de code par indicateur.
//
// Contrat v1.2 : `variable` et `place` sont publiés par l'ETL (vocabulaire etl/config/variables.yaml).
// Le site ne connaît aucune variable à l'avance. Un indicateur sans ces champs reste listé normalement.
import { getIndicator, listIndicators } from "./data";
import type { Indicator, ManifestEntry, Place, Scale, Trend, Variable } from "./schema";

export type Member = { entry: ManifestEntry; variable: Variable; place: Place };
export type Theme = { id: string; label: string; variables: Variable[]; unit: string };

export function members(scale: Scale): Member[] {
  return listIndicators(scale).flatMap((e) => (e.variable && e.place ? [{ entry: e, variable: e.variable, place: e.place }] : []));
}

/** Indicateurs hors famille : listés tels quels sur la page de l'échelle. */
export function nonMembers(scale: Scale): ManifestEntry[] {
  return listIndicators(scale).filter((e) => !e.variable || !e.place);
}

const load = (m: Member) => getIndicator(m.entry.scale, m.entry.id)!;
const href = (m: Member) => `/${m.entry.scale}/${m.entry.id}`;
const isComposite = (m: Member) => m.place.kind === "composite";
const byOrder = (a: Variable, b: Variable) => a.order - b.order || a.id.localeCompare(b.id);

export function placeLabel(place: Place): string {
  return place.kind === "composite" ? `${place.name} (composite)` : place.name;
}

/** Thèmes de l'échelle, dans l'ordre de leur première apparition au manifeste. */
export function themes(scale: Scale): Theme[] {
  const out = new Map<string, Theme>();
  for (const m of members(scale)) {
    const t: Theme = out.get(m.variable.theme) ?? { id: m.variable.theme, label: m.variable.theme_label, variables: [], unit: m.entry.unit };
    if (!t.variables.some((v) => v.id === m.variable.id)) t.variables.push(m.variable);
    if (t.unit !== m.entry.unit) {
      // Un thème rassemble des variables comparables : des unités différentes signalent une erreur de vocabulaire.
      throw new Error(`thème « ${t.id} » : unités différentes (${t.unit}, ${m.entry.unit})`);
    }
    out.set(t.id, t);
  }
  return [...out.values()].map((t) => ({ ...t, variables: t.variables.sort(byOrder) }));
}

const inTheme = (scale: Scale, theme: string) => members(scale).filter((m) => m.variable.theme === theme);

/** Tendance sur la période commune à toutes les stations, publiée par l'ETL (critère C5). */
export function commonTrend(ind: Indicator): Trend | undefined {
  return ind.alt_trends.find((t) => t.label.includes("période commune"));
}

/** Composites d'un thème, dans l'ordre des variables. */
export function composites(scale: Scale, theme: string): { variable: Variable; ind: Indicator; href: string }[] {
  return inTheme(scale, theme)
    .filter(isComposite)
    .sort((a, b) => byOrder(a.variable, b.variable))
    .map((m) => ({ variable: m.variable, ind: load(m), href: href(m) }));
}

/** `slope` null : la série existe mais ne couvre pas toute la période commune (années manquantes). */
export type Cell = { slope: number | null; low: number | null; high: number | null; href: string };
export type MatrixRow = { place: string; name: string; isComposite: boolean; cells: Record<string, Cell> };
export type Matrix = {
  variables: Variable[];
  unit: string;
  rows: MatrixRow[];
  period: { start: number; end: number } | null;
  /** Écart entre la pente la plus forte et la plus faible des stations (composite exclu), par variable. */
  spread: Record<string, { min: number; max: number; n: number }>;
};

export function familyMatrix(scale: Scale, theme: Theme): Matrix {
  const ms = inTheme(scale, theme.id);
  const byPlace = new Map<string, MatrixRow>();
  let period: Matrix["period"] = null;
  for (const m of ms) {
    const t = commonTrend(load(m));
    const row = byPlace.get(m.place.id) ?? { place: m.place.id, name: placeLabel(m.place), isComposite: isComposite(m), cells: {} };
    if (t) {
      row.cells[m.variable.id] = { slope: t.slope_per_decade, low: t.slope_ci_low, high: t.slope_ci_high, href: href(m) };
      period ??= t.period;
    } else {
      row.cells[m.variable.id] = { slope: null, low: null, high: null, href: href(m) };
    }
    byPlace.set(m.place.id, row);
  }
  const rows = [...byPlace.values()].sort(
    (a, b) =>
      Number(a.isComposite) - Number(b.isComposite) ||
      Object.values(b.cells).filter((c) => c.slope !== null).length - Object.values(a.cells).filter((c) => c.slope !== null).length ||
      a.name.localeCompare(b.name, "fr"),
  );
  const spread: Matrix["spread"] = {};
  for (const v of theme.variables) {
    const vals = rows.filter((r) => !r.isComposite).flatMap((r) => {
      const s = r.cells[v.id]?.slope;
      return s === null || s === undefined ? [] : [s];
    });
    if (vals.length > 1) spread[v.id] = { min: Math.min(...vals), max: Math.max(...vals), n: vals.length };
  }
  return { variables: theme.variables, unit: theme.unit, rows, period, spread };
}

export type Line = { name: string; time: string[]; value: (number | null)[]; quality: ("homogenized" | "raw")[] | null };
export type Overlay = {
  /** Périodes de référence des anomalies, distinctes (ex. « 1961-1990 »). */
  references: string[];
  stations: Line[];
  composite: (Line & { trend: { start: number; end: number; fittedStart: number; fittedEnd: number } | null }) | null;
};

/** Séries de toutes les stations de chaque variable du thème, plus le composite : pour la vue superposée. */
export function overlays(scale: Scale, theme: string): Record<string, Overlay> {
  const out: Record<string, Overlay> = {};
  for (const m of inTheme(scale, theme)) {
    const ind = load(m);
    const o = (out[m.variable.id] ??= { references: [], stations: [], composite: null });
    const ref = ind.reference_period ? `${ind.reference_period.start}-${ind.reference_period.end}` : null;
    if (ref && !o.references.includes(ref)) o.references.push(ref);
    const line = { name: placeLabel(m.place), time: ind.series.time, value: ind.series.value, quality: ind.series.quality };
    if (isComposite(m)) {
      const t = ind.trend;
      o.composite = {
        ...line,
        trend: t ? { start: t.period.start, end: t.period.end, fittedStart: t.fitted_start, fittedEnd: t.fitted_end } : null,
      };
    } else {
      o.stations.push(line);
    }
  }
  return out;
}

export type MapPoint = { id: string; name: string; lat: number; lon: number; value: number | null; href: string };

/** Points de carte par variable du thème : une station par indicateur, valeur = pente sur la période commune. */
export function mapPoints(scale: Scale, theme: string): Record<string, MapPoint[]> {
  const out: Record<string, MapPoint[]> = {};
  for (const m of inTheme(scale, theme)) {
    if (isComposite(m)) continue;
    const ind = load(m);
    const st = ind.stations[0];
    if (!st) continue;
    (out[m.variable.id] ??= []).push({
      id: st.id,
      name: m.place.name,
      lat: st.latitude,
      lon: st.longitude,
      value: commonTrend(ind)?.slope_per_decade ?? null,
      href: href(m),
    });
  }
  return out;
}

export type Sibling = { key: string; label: string; title?: string; href: string | null; active: boolean };

/** Navigation latérale d'une page indicateur : autres variables du thème au même lieu, autres lieux pour la même variable. */
export function siblings(ind: Indicator): { variables: Sibling[]; places: Sibling[]; composite: Indicator | null } | null {
  if (!ind.variable || !ind.place) return null;
  const self = { variable: ind.variable, place: ind.place };
  const ms = inTheme(ind.scale, self.variable.theme);
  const vars = [...new Map(ms.map((m) => [m.variable.id, m.variable])).values()].sort(byOrder);
  const variables = vars.map((v) => {
    const m = ms.find((x) => x.variable.id === v.id && x.place.id === self.place.id);
    return { key: v.id, label: v.code, title: v.label, href: m ? href(m) : null, active: v.id === self.variable.id };
  });
  const same = ms.filter((m) => m.variable.id === self.variable.id);
  const places = same
    .sort((a, b) => Number(isComposite(b)) - Number(isComposite(a)) || a.place.name.localeCompare(b.place.name, "fr"))
    .map((m) => ({ key: m.place.id, label: m.place.name, href: href(m), active: m.place.id === self.place.id }));
  const comp = self.place.kind === "composite" ? undefined : same.find(isComposite);
  return { variables, places, composite: comp ? load(comp) : null };
}
