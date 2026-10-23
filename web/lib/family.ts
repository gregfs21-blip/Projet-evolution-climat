// Familles d'indicateurs : une même variable mesurée en plusieurs lieux (stations + composite).
// C'est ce qui permet les vues comparatives (matrice, superposition, carte, navigation latérale)
// sans écrire de code par indicateur.
//
// Le contrat de données v1.1 ne porte pas explicitement « variable » et « lieu » : on les lit dans
// l'identifiant (`tn-annuelle-cap-ferret`). Un indicateur dont l'identifiant ne suit pas ce motif
// n'est simplement pas rattaché à une famille et reste listé normalement : rien n'est deviné.
// À terme (P2), ces deux champs devront entrer dans le contrat.
import { getIndicator, listIndicators } from "./data";
import { SCALE_LABELS } from "./format";
import type { Indicator, ManifestEntry, Scale, Trend } from "./schema";

export const VARIABLES = {
  tn: { code: "TN", short: "min.", plural: "minimales" },
  tm: { code: "TM", short: "moy.", plural: "moyennes" },
  tx: { code: "TX", short: "max.", plural: "maximales" },
} as const;
export type VarKey = keyof typeof VARIABLES;
export const VAR_ORDER: VarKey[] = ["tn", "tm", "tx"];

const MEMBER_RE = /^(tn|tm|tx)-annuelle-([a-z0-9]+(?:-[a-z0-9]+)*)$/;

export type Member = { entry: ManifestEntry; variable: VarKey; place: string; isComposite: boolean };

export function parseMember(e: ManifestEntry): Member | undefined {
  const m = MEMBER_RE.exec(e.id);
  if (!m) return undefined;
  const place = m[2]!;
  return { entry: e, variable: m[1] as VarKey, place, isComposite: place === e.scale };
}

export function members(scale: Scale): Member[] {
  return listIndicators(scale).flatMap((e) => parseMember(e) ?? []);
}

/** Indicateurs hors famille : listés tels quels sur la page de l'échelle. */
export function nonMembers(scale: Scale): ManifestEntry[] {
  return listIndicators(scale).filter((e) => !parseMember(e));
}

const load = (m: Member) => getIndicator(m.entry.scale, m.entry.id)!;
const href = (m: Member) => `/${m.entry.scale}/${m.entry.id}`;

export function placeName(m: Member, ind: Indicator): string {
  return m.isComposite ? `${SCALE_LABELS[m.entry.scale].name} (composite)` : (ind.stations[0]?.name ?? m.place);
}

/** Tendance sur la période commune à toutes les stations, publiée par l'ETL (critère C5). */
export function commonTrend(ind: Indicator): Trend | undefined {
  return ind.alt_trends.find((t) => t.label.includes("période commune"));
}

/** Composites de l'échelle, dans l'ordre TN, TM, TX. */
export function composites(scale: Scale): { variable: VarKey; ind: Indicator; href: string }[] {
  const ms = members(scale).filter((m) => m.isComposite);
  return VAR_ORDER.flatMap((v) => {
    const m = ms.find((x) => x.variable === v);
    return m ? [{ variable: v, ind: load(m), href: href(m) }] : [];
  });
}

export type Cell = { slope: number; low: number | null; high: number | null; href: string };
export type MatrixRow = { place: string; name: string; isComposite: boolean; cells: Partial<Record<VarKey, Cell>> };
export type Matrix = {
  variables: VarKey[];
  rows: MatrixRow[];
  period: { start: number; end: number } | null;
  /** Écart entre la pente la plus forte et la plus faible des stations (composite exclu). */
  spread: Partial<Record<VarKey, { min: number; max: number; n: number }>>;
};

export function familyMatrix(scale: Scale): Matrix {
  const ms = members(scale);
  const variables = VAR_ORDER.filter((v) => ms.some((m) => m.variable === v));
  const byPlace = new Map<string, MatrixRow>();
  let period: Matrix["period"] = null;
  for (const m of ms) {
    const ind = load(m);
    const t = commonTrend(ind);
    const row = byPlace.get(m.place) ?? { place: m.place, name: placeName(m, ind), isComposite: m.isComposite, cells: {} };
    if (t) {
      row.cells[m.variable] = { slope: t.slope_per_decade, low: t.slope_ci_low, high: t.slope_ci_high, href: href(m) };
      period ??= t.period;
    }
    byPlace.set(m.place, row);
  }
  const rows = [...byPlace.values()].sort(
    (a, b) =>
      Number(a.isComposite) - Number(b.isComposite) ||
      Object.keys(b.cells).length - Object.keys(a.cells).length ||
      a.name.localeCompare(b.name, "fr"),
  );
  const spread: Matrix["spread"] = {};
  for (const v of variables) {
    const vals = rows.filter((r) => !r.isComposite).flatMap((r) => (r.cells[v] ? [r.cells[v]!.slope] : []));
    if (vals.length > 1) spread[v] = { min: Math.min(...vals), max: Math.max(...vals), n: vals.length };
  }
  return { variables, rows, period, spread };
}

export type Line = { name: string; time: string[]; value: (number | null)[]; quality: ("homogenized" | "raw")[] | null };
export type Overlay = {
  /** Périodes de référence des anomalies, distinctes (ex. « 1961-1990 »). */
  references: string[];
  stations: Line[];
  composite: (Line & { trend: { start: number; end: number; fittedStart: number; fittedEnd: number } | null }) | null;
};

/** Séries de toutes les stations d'une variable, plus le composite : pour la vue superposée. */
export function overlays(scale: Scale): Partial<Record<VarKey, Overlay>> {
  const out: Partial<Record<VarKey, Overlay>> = {};
  for (const m of members(scale)) {
    const ind = load(m);
    const o = (out[m.variable] ??= { references: [], stations: [], composite: null });
    const ref = ind.reference_period ? `${ind.reference_period.start}-${ind.reference_period.end}` : null;
    if (ref && !o.references.includes(ref)) o.references.push(ref);
    const line = { name: placeName(m, ind), time: ind.series.time, value: ind.series.value, quality: ind.series.quality };
    if (m.isComposite) {
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

/** Points de carte par variable : une station par indicateur, valeur = pente sur la période commune. */
export function mapPoints(scale: Scale): Partial<Record<VarKey, MapPoint[]>> {
  const out: Partial<Record<VarKey, MapPoint[]>> = {};
  for (const m of members(scale)) {
    if (m.isComposite) continue;
    const ind = load(m);
    const st = ind.stations[0];
    if (!st) continue;
    (out[m.variable] ??= []).push({
      id: st.id,
      name: st.name,
      lat: st.latitude,
      lon: st.longitude,
      value: commonTrend(ind)?.slope_per_decade ?? null,
      href: href(m),
    });
  }
  return out;
}

export type Sibling = { key: string; label: string; href: string | null; active: boolean };

/** Navigation latérale d'une page indicateur : autres variables au même lieu, autres lieux pour la même variable. */
export function siblings(ind: Indicator): { variables: Sibling[]; places: Sibling[]; composite: Indicator | null } | null {
  const self = members(ind.scale).find((m) => m.entry.id === ind.id);
  if (!self) return null;
  const ms = members(ind.scale);
  const variables = VAR_ORDER.flatMap((v) => {
    if (!ms.some((m) => m.variable === v)) return [];
    const m = ms.find((x) => x.variable === v && x.place === self.place);
    return [{ key: v, label: `${VARIABLES[v].code} ${VARIABLES[v].short}`, href: m ? href(m) : null, active: v === self.variable }];
  });
  const same = ms.filter((m) => m.variable === self.variable);
  const places = same
    .map((m) => ({ m, ind: load(m) }))
    .sort((a, b) => Number(b.m.isComposite) - Number(a.m.isComposite) || placeName(a.m, a.ind).localeCompare(placeName(b.m, b.ind), "fr"))
    .map(({ m, ind: i }) => ({
      key: m.place,
      label: m.isComposite ? SCALE_LABELS[ind.scale].name : placeName(m, i),
      href: href(m),
      active: m.place === self.place,
    }));
  const comp = self.isComposite ? undefined : same.find((m) => m.isComposite);
  return { variables, places, composite: comp ? load(comp) : null };
}
