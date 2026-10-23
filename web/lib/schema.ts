// Miroir exact de etl/schema.py. Toute modification côté ETL doit être reportée ici.
import { z } from "zod";

export const SCALES = ["gironde", "france", "monde"] as const;
export const scaleSchema = z.enum(SCALES);
export type Scale = z.infer<typeof scaleSchema>;

export const confidenceSchema = z.enum(["elevee", "moyenne", "faible", "non_etabli"]);
export type Confidence = z.infer<typeof confidenceSchema>;

const isoDate = z.string().refine((s) => !Number.isNaN(Date.parse(s)), "date ISO invalide");

const periodSchema = z
  .strictObject({ start: z.number().int().min(1700).max(2200), end: z.number().int().min(1700).max(2200) })
  .refine((p) => p.end >= p.start, "period.end doit être >= period.start");

const provenanceSchema = z.strictObject({
  source_name: z.string().min(1),
  source_url: z.string().regex(/^https?:\/\//),
  license: z.string().min(1),
  extracted_at: isoDate,
  script: z.string().min(1),
  etl_version: z.string().min(1),
  homogenized: z.boolean(),
});

const trendSchema = z.strictObject({
  label: z.string(),
  method: z.string().min(1),
  period: periodSchema,
  slope_per_decade: z.number(),
  slope_ci_low: z.number().nullable(),
  slope_ci_high: z.number().nullable(),
  fitted_start: z.number(),
  fitted_end: z.number(),
  p_value: z.number().min(0).max(1),
  significant: z.boolean(),
  alpha: z.number().gt(0).lt(1),
  p_value_classical: z.number().min(0).max(1).nullable(),
});

const breakpointSchema = z.strictObject({
  time: z.string(),
  method: z.string(),
  p_value: z.number().min(0).max(1).nullable(),
  possible_artifact: z.boolean(),
  detrended_p_value: z.number().min(0).max(1).nullable(),
  note: z.string().nullable(),
});

const normalSchema = z.strictObject({ period: periodSchema, value: z.number() });

// Écart entre deux normales, avec un test : chiffre mis en avant pour un indice rare (critère E9).
const normalsComparisonSchema = z
  .strictObject({
    first: periodSchema,
    second: periodSchema,
    first_value: z.number(),
    second_value: z.number(),
    difference: z.number(),
    p_value: z.number().min(0).max(1),
    significant: z.boolean(),
    alpha: z.number().gt(0).lt(1),
    method: z.string().min(1),
  })
  .refine((c) => c.significant === c.p_value < c.alpha, "comparaison des normales : significant incohérent")
  .refine((c) => Math.abs(c.difference - (c.second_value - c.first_value)) < 1e-6, "comparaison des normales : difference incohérente");
export type NormalsComparison = z.infer<typeof normalsComparisonSchema>;

const stationSchema = z.strictObject({
  id: z.string().min(1),
  name: z.string().min(1),
  latitude: z.number().min(-90).max(90),
  longitude: z.number().min(-180).max(180),
  altitude: z.number(),
  series_id: z.string().nullable(),
  homogenized_period: periodSchema.nullable(),
  min_detectable_amplitude: z.number().nullable(),
  homogenization_breaks: z.array(z.string()),
  file_produced: z.string().nullable(),
});
export type Station = z.infer<typeof stationSchema>;

const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;

// Grandeur mesurée (vocabulaire etl/config/variables.yaml) : rassemble une famille d'indicateurs.
const variableSchema = z.strictObject({
  id: z.string().regex(SLUG),
  code: z.string().min(1).max(12),
  label: z.string().min(1),
  theme: z.string().regex(SLUG),
  theme_label: z.string().min(1),
  order: z.number().int().min(0),
});
export type Variable = z.infer<typeof variableSchema>;

// Lieu : une station, ou le composite de l'échelle.
const placeSchema = z.strictObject({
  id: z.string().regex(SLUG),
  name: z.string().min(1),
  kind: z.enum(["station", "composite"]),
});
export type Place = z.infer<typeof placeSchema>;

const seriesSchema = z
  .strictObject({
    time: z.array(z.string()).min(1),
    value: z.array(z.number().nullable()),
    quality: z.array(z.enum(["homogenized", "raw"])).nullable(),
  })
  .refine((s) => s.time.length === s.value.length, "series.time et series.value de longueurs différentes")
  .refine((s) => s.quality === null || s.quality.length === s.time.length, "series.quality de longueur différente")
  .refine((s) => s.time.every((t, i) => i === 0 || s.time[i - 1]! < t), "series.time non trié ou dupliqué");

export const indicatorSchema = z
  .strictObject({
    schema_version: z.literal("1.3"),
    id: z.string().regex(SLUG),
    scale: scaleSchema,
    group: z.string().nullable(),
    variable: variableSchema.nullable(),
    place: placeSchema.nullable(),
    title: z.string().min(1),
    unit: z.string(),
    description: z.string().min(1),
    frequency: z.enum(["annual", "seasonal", "monthly", "daily"]),
    is_anomaly: z.boolean(),
    reference_period: periodSchema.nullable(),
    series: seriesSchema,
    normals: z.array(normalSchema),
    trend: trendSchema.nullable(),
    alt_trends: z.array(trendSchema),
    headline: z.enum(["trend", "normals"]),
    normals_comparison: normalsComparisonSchema.nullable(),
    breakpoints: z.array(breakpointSchema),
    stations: z.array(stationSchema),
    method_note: z.string().nullable(),
    finding: z.string().min(1),
    confidence: confidenceSchema,
    limitations: z.array(z.string().trim().min(1)).min(1),
    provenance: provenanceSchema,
    is_demo: z.boolean(),
  })
  .refine((d) => !d.is_anomaly || d.reference_period !== null, "anomalie sans reference_period")
  .refine((d) => d.headline !== "normals" || d.normals_comparison !== null, "headline 'normals' sans normals_comparison")
  .refine((d) => (d.variable === null) === (d.place === null), "variable et place vont ensemble")
  .refine((d) => d.place?.kind !== "composite" || d.place.id === d.scale, "composite : place.id doit valoir l'échelle")
  .refine(
    // Un seul poste ; plusieurs séries possibles (TM de station = séries TN et TX du même poste).
    (d) => d.place?.kind !== "station" || (d.stations.length > 0 && new Set(d.stations.map((s) => s.id)).size === 1),
    "station : un seul poste attendu",
  )
  .refine(
    (d) => [d.trend, ...d.alt_trends].every((t) => !t || t.significant === t.p_value < t.alpha),
    "tendance : significant incohérent avec p_value",
  )
  .refine((d) => {
    // Règle C2 : aucune tendance ni normale ne s'appuie sur un point non homogénéisé.
    if (!d.series.quality) return true;
    const raw = d.series.time.filter((_, i) => d.series.quality![i] === "raw").map((t) => Number(t.slice(0, 4)));
    const spans = [d.trend, ...d.alt_trends].filter((t) => t !== null).map((t) => t!.period);
    spans.push(...d.normals.map((n) => n.period));
    return spans.every((p) => raw.every((y) => y < p.start || y > p.end));
  }, "tendance ou normale incluant des années non homogénéisées")
  .refine((d) => !d.is_demo || d.title.toLowerCase().includes("démo"), "démo non signalée dans le titre");
export type Indicator = z.infer<typeof indicatorSchema>;
export type Trend = NonNullable<Indicator["trend"]>;

const manifestEntrySchema = z.strictObject({
  id: z.string(),
  scale: scaleSchema,
  title: z.string(),
  unit: z.string(),
  path: z.string(),
  confidence: confidenceSchema,
  is_demo: z.boolean(),
  group: z.string().nullable(),
  variable: variableSchema.nullable(),
  place: placeSchema.nullable(),
});
export type ManifestEntry = z.infer<typeof manifestEntrySchema>;

export const manifestSchema = z
  .strictObject({
    schema_version: z.literal("1.3"),
    generated_at: isoDate,
    etl_version: z.string(),
    indicators: z.array(manifestEntrySchema),
  })
  .refine((m) => {
    const keys = m.indicators.filter((e) => e.variable && e.place).map((e) => `${e.scale}/${e.variable!.id}/${e.place!.id}`);
    return new Set(keys).size === keys.length;
  }, "deux indicateurs pour la même variable au même lieu")
  .refine((m) => {
    const seen = new Map<string, string>();
    return m.indicators.every((e) => {
      if (!e.variable) return true;
      const sig = JSON.stringify(e.variable);
      return (seen.get(e.variable.id) ?? (seen.set(e.variable.id, sig), sig)) === sig;
    });
  }, "variable décrite de deux façons différentes");
export type Manifest = z.infer<typeof manifestSchema>;

// ---------------------------------------------------------------- Rapport de validation de phase
// Miroir de ValidationReport (etl/schema.py). Fichier data/processed/validation-<phase>.json.
const validationCheckSchema = z.strictObject({
  name: z.string().min(1),
  kind: z.enum(["critère", "info", "retiré"]),
  status: z.string().min(1),
  satisfied: z.boolean(),
  detail: z.string().min(1),
});
export type ValidationCheck = z.infer<typeof validationCheckSchema>;

export const validationReportSchema = z
  .strictObject({
    schema_version: z.literal("1.0"),
    phase: z.string().regex(/^p[0-9]+[a-z]?$/),
    generated_at: isoDate,
    closure_ok: z.boolean(),
    verdict: z.string().min(1),
    indicators: z.array(z.string()).min(1),
    checks: z.array(validationCheckSchema).min(1),
  })
  .refine(
    (r) => r.closure_ok === r.checks.filter((c) => c.kind === "critère").every((c) => c.satisfied),
    "closure_ok incohérent avec les critères",
  );
export type ValidationReport = z.infer<typeof validationReportSchema>;
