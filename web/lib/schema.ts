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

// Référence publiée fixée avant calcul (méthode « largeur d'abord ») et verdict du contrôle.
const referenceCheckSchema = z.strictObject({
  statement: z.string().min(1),
  source: z.string().min(1),
  source_url: z.string().regex(/^https?:\/\//),
  kind: z.enum(["slope", "rate", "difference", "relative_slope", "not_significant", "mean"]),
  period: periodSchema,
  expected_low: z.number().nullable(),
  expected_high: z.number().nullable(),
  measured: z.number().nullable(),
  unit: z.string(),
  satisfied: z.boolean(),
  fixed_on: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
});
export type ReferenceCheck = z.infer<typeof referenceCheckSchema>;

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
    schema_version: z.literal("1.5"),
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
    reference_check: referenceCheckSchema.nullable(),
    indicative: z.boolean(),
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
  .refine(
    (d) => !d.indicative || ((d.confidence === "faible" || d.confidence === "non_etabli") && d.normals.length === 0),
    "tendance indicative : confiance au plus « faible », sans normale",
  )
  .refine((d) => {
    // Règle C2 : aucune tendance ni normale ne s'appuie sur un point non homogénéisé.
    // Exception : tendance indicative sur série brute (décision de Grég du 25/10/2026), bornée ci-dessus.
    if (!d.series.quality || d.indicative) return true;
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
    schema_version: z.literal("1.5"),
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

// ---------------------------------------------------------------- Couverture du projet
// Miroir de Coverage (etl/schema.py). « publie » est calculé par l'ETL à partir du manifeste.
const coverageCellSchema = z
  .strictObject({
    scale: scaleSchema,
    status: z.enum(["publie", "prevu", "sans-donnee", "instantane"]),
    source: z.string().nullable(),
    note: z.string().nullable(),
    indicators: z.array(z.strictObject({ id: z.string(), title: z.string(), confidence: confidenceSchema })),
  })
  .refine((c) => (c.status === "publie") === c.indicators.length > 0, "couverture : « publie » ssi indicateurs publiés");
export type CoverageCell = z.infer<typeof coverageCellSchema>;

export const coverageSchema = z.strictObject({
  schema_version: z.literal("1.0"),
  generated_at: isoDate,
  parameters: z.array(
    z.strictObject({ id: z.string().regex(SLUG), label: z.string().min(1), cells: z.array(coverageCellSchema).min(1) }),
  ),
});
export type Coverage = z.infer<typeof coverageSchema>;

// ---------------------------------------------------------------- Carte départementale (P5 bis)
// Miroir de DepartmentMap (etl/schema.py).
const departmentValueSchema = z.strictObject({
  code: z.string().regex(/^[0-9]{2}$/),
  n_stations: z.number().int().min(1),
  slope_per_decade: z.number(),
  slope_ci_low: z.number().nullable(),
  slope_ci_high: z.number().nullable(),
  p_value: z.number().min(0).max(1),
  significant: z.boolean(),
});

export const departmentMapSchema = z
  .strictObject({
    schema_version: z.literal("1.0"),
    generated_at: isoDate,
    title: z.string().min(1),
    unit: z.string().min(1),
    period: periodSchema,
    method_note: z.string().min(1),
    limitations: z.array(z.string()).min(1),
    provenance: provenanceSchema,
    geometry_source: z.string().min(1),
    variables: z
      .array(
        z.strictObject({
          id: z.string().regex(SLUG),
          code: z.string().min(1),
          label: z.string().min(1),
          national_slope_per_decade: z.number(),
          departments: z.array(departmentValueSchema).min(1),
        }),
      )
      .min(1),
    shapes: z
      .array(
        z.strictObject({
          code: z.string().regex(/^(?:[0-9]{2}|2A|2B)$/),
          name: z.string().min(1),
          value_code: z.string().regex(/^[0-9]{2}$/),
          geometry: z.strictObject({ type: z.enum(["Polygon", "MultiPolygon"]), coordinates: z.array(z.any()) }),
        }),
      )
      .min(90),
  })
  .refine((m) => {
    const codes = new Set(m.shapes.map((s) => s.value_code));
    return m.variables.every((v) => v.departments.every((d) => codes.has(d.code)));
  }, "carte : département sans contour");
export type DepartmentMap = z.infer<typeof departmentMapSchema>;

// ---------------------------------------------------------------- Synthèse (P8)
// Miroir de Synthesis (etl/schema.py). Le texte est rendu par l'ETL ; le site l'affiche tel quel.
const claimSchema = z
  .strictObject({
    id: z.string().regex(SLUG),
    kind: z.enum(["signal", "absence", "comparaison", "acceleration", "information", "contexte", "lacune"]),
    params: z.array(z.string()).default([]),
    text: z.string().min(1),
    confidence: confidenceSchema.optional(),
    indicators: z
      .array(z.strictObject({ id: z.string(), scale: scaleSchema, title: z.string(), confidence: confidenceSchema }))
      .default([]),
    source: z.strictObject({ label: z.string().min(1), url: z.string().regex(/^https:\/\//) }).optional(),
    problem: z.string().optional(),
  })
  .refine(
    (c) =>
      ["signal", "absence", "comparaison", "acceleration"].includes(c.kind) === (c.confidence !== undefined),
    "synthèse : confiance présente ssi l'affirmation est qualifiée",
  );
export type Claim = z.infer<typeof claimSchema>;

export const synthesisSchema = z.strictObject({
  schema_version: z.literal("1.0"),
  generated_at: isoDate,
  sections: z
    .array(
      z.strictObject({
        id: z.string().regex(SLUG),
        title: z.string().min(1),
        scale: scaleSchema.optional(),
        intro: z.string().optional(),
        groups: z.array(z.strictObject({ title: z.string().min(1), claims: z.array(claimSchema).min(1) })).default([]),
        conclusion: z.string().optional(),
        pending: z.string().optional(),
      }),
    )
    .min(1),
});
export type Synthesis = z.infer<typeof synthesisSchema>;

// ---------------------------------------------------------------- Démonstration (P10)
// Miroir de Demonstration (etl/schema.py). Résultats produits par etl/demonstration.py ; le site les affiche tels quels.
const estimateSchema = z.strictObject({
  value: z.number(),
  ci_low: z.number().nullable(),
  ci_high: z.number().nullable(),
});
export type Estimate = z.infer<typeof estimateSchema>;

const coefficientSchema = z
  .strictObject({
    name: z.string().regex(SLUG),
    label: z.string().min(1),
    unit: z.string().min(1),
    value: z.number(),
    ci_low: z.number(),
    ci_high: z.number(),
    p_value: z.number().min(0).max(1),
  })
  .refine((c) => c.ci_low <= c.value && c.value <= c.ci_high, "coefficient hors de son intervalle");
export type Coefficient = z.infer<typeof coefficientSchema>;

const attributionSchema = z.strictObject({
  window: periodSchema,
  baseline: periodSchema,
  anthropogenic: estimateSchema,
  natural: estimateSchema,
  observed: z.number().nullable(),
  reference_anthropogenic: estimateSchema,
  reference_natural: estimateSchema,
  reference_source: z.string().min(1),
});
export type Attribution = z.infer<typeof attributionSchema>;

const robustnessCaseSchema = z.strictObject({
  group: z.enum(["decalages", "forcage", "sous-periode"]),
  label: z.string().min(1),
  period: periodSchema,
  beta_anthro: estimateSchema,
  attributable: z.number(),
  tcr: z.number(),
  rho: z.number().gt(-1).lt(1),
  r2: z.number().max(1),
  in_range: z.boolean(),
});
export type RobustnessCase = z.infer<typeof robustnessCaseSchema>;

const regressionSeriesSchema = z
  .strictObject({
    years: z.array(z.number().int()).min(10),
    observed: z.array(z.number()),
    fitted: z.array(z.number()),
    adjusted: z.array(z.number()),
    anthropogenic: z.array(z.number()),
    volcanic: z.array(z.number()),
    solar: z.array(z.number()),
    enso: z.array(z.number()),
    observed_rebased: z.array(z.number()),
  })
  .refine(
    (s) =>
      [s.observed, s.fitted, s.adjusted, s.anthropogenic, s.volcanic, s.solar, s.enso, s.observed_rebased].every(
        (a) => a.length === s.years.length,
      ),
    "séries de longueurs différentes",
  )
  .refine((s) => s.years.every((y, i) => i === 0 || y === s.years[i - 1]! + 1), "années non consécutives");
export type RegressionSeries = z.infer<typeof regressionSeriesSchema>;

const regressionDatasetSchema = z.strictObject({
  id: z.string().regex(SLUG),
  indicator_id: z.string().regex(SLUG),
  label: z.string().min(1),
  period: periodSchema,
  n: z.number().int().min(10),
  method: z.string().min(1),
  rho: z.number().gt(-1).lt(1),
  r2: z.number().max(1),
  residual_sd: z.number().min(0),
  coefficients: z.array(coefficientSchema).min(1),
  coefficients_ols: z.array(coefficientSchema).min(1),
  vif: z.record(z.string(), z.number()),
  tcr: estimateSchema,
  attributions: z.array(attributionSchema).min(1),
  trend_observed: trendSchema,
  trend_adjusted: trendSchema,
  slope_observed: estimateSchema,
  slope_adjusted: estimateSchema,
  residual_trend_p: z.number().min(0).max(1),
  robustness: z.array(robustnessCaseSchema),
  series: regressionSeriesSchema,
});
export type RegressionDataset = z.infer<typeof regressionDatasetSchema>;

const criterionSchema = z.strictObject({
  id: z.string().regex(/^[A-Z][0-9]+$/),
  label: z.string().min(1),
  satisfied: z.boolean(),
  detail: z.string().min(1),
});

const inputSourceSchema = z.strictObject({
  name: z.string().min(1),
  url: z.string().regex(/^https?:\/\//),
  license: z.string().min(1),
  note: z.string().nullable(),
});

const regressionSchema = z
  .strictObject({
    question: z.string().min(1),
    model: z.string().min(1),
    finding: z.string().min(1),
    confidence: confidenceSchema,
    confidence_reason: z.string().min(1),
    method_note: z.string().min(1),
    limitations: z.array(z.string()).min(1),
    inputs: z.array(inputSourceSchema).min(1),
    enso_oni_correlation: z.number().min(-1).max(1),
    tcr_reference: estimateSchema,
    datasets: z.array(regressionDatasetSchema).min(1),
    criteria: z.array(criterionSchema).min(1),
    script: z.string().min(1),
    etl_version: z.string().min(1),
    extracted_at: isoDate,
  })
  .refine((r) => {
    const ok = new Map(r.criteria.map((c) => [c.id, c.satisfied]));
    const core = [2, 3, 4, 5, 6, 7, 8].every((i) => ok.get(`O${i}`) === true);
    const expected = core ? "elevee" : ok.get("O3") ? "moyenne" : "non_etabli";
    return r.confidence === expected;
  }, "régression : confiance incohérente avec les critères (règle D-AG)");
export type Regression = z.infer<typeof regressionSchema>;

/** Grandeur qui peut être infinie : null = infini (période de retour hors de la loi, rapport de probabilités). */
const unboundedSchema = z.strictObject({
  value: z.number().nullable(),
  ci_low: z.number().nullable(),
  ci_high: z.number().nullable(),
  undefined_draws: z.number().int().min(0),
  infinite_draws: z.number().int().min(0),
});
export type Unbounded = z.infer<typeof unboundedSchema>;

const extremeEventSchema = z.strictObject({
  id: z.string().regex(SLUG),
  label: z.string().min(1),
  value: estimateSchema,
  date: z.string().nullable(),
  return_period_today: unboundedSchema,
  return_period_past: unboundedSchema,
  return_period_preindustrial: unboundedSchema,
  probability_ratio: unboundedSchema,
  probability_ratio_preindustrial: unboundedSchema,
  intensity_change: estimateSchema,
  intensity_change_preindustrial: estimateSchema,
});
export type ExtremeEvent = z.infer<typeof extremeEventSchema>;

const gevCurveSchema = z
  .strictObject({
    periods: z.array(z.number()).min(5),
    today: z.array(z.number()),
    today_low: z.array(z.number()),
    today_high: z.array(z.number()),
    past: z.array(z.number()),
    past_low: z.array(z.number()),
    past_high: z.array(z.number()),
    obs_periods: z.array(z.number()),
    obs_today: z.array(z.number()),
    obs_past: z.array(z.number()),
  })
  .refine(
    (c) => [c.today, c.today_low, c.today_high, c.past, c.past_low, c.past_high].every((a) => a.length === c.periods.length),
    "courbe : longueurs différentes",
  )
  .refine((c) => c.obs_today.length === c.obs_periods.length && c.obs_past.length === c.obs_periods.length, "courbe : observations de longueurs différentes");
export type GevCurve = z.infer<typeof gevCurveSchema>;

const extremeSeriesSchema = z
  .strictObject({
    years: z.array(z.number().int()).min(20),
    values: z.array(z.number()),
    raw_years: z.array(z.number().int()),
    mu: z.array(z.number()),
    level20: z.array(z.number()),
  })
  .refine((s) => [s.values, s.mu, s.level20].every((a) => a.length === s.years.length), "série : longueurs différentes");
export type ExtremeSeries = z.infer<typeof extremeSeriesSchema>;

const extremeVariantSchema = z.strictObject({
  group: z.enum(["robustesse", "station"]),
  label: z.string().min(1),
  period: periodSchema,
  n: z.number().int(),
  alpha: estimateSchema,
  xi: z.number(),
  probability_ratio: z.number().nullable(),
  probability_ratio_status: z.enum(["fini", "infini", "indefini", "sans_objet"]),
  return_period_today: z.number().nullable(),
  ok: z.boolean(),
})
  .refine((v) => (v.probability_ratio !== null) === (v.probability_ratio_status === "fini"), "variante : rapport de probabilité incohérent avec son statut")
  .refine(
    (v) => (v.return_period_today !== null) === (v.probability_ratio_status === "fini" || v.probability_ratio_status === "infini"),
    "variante : période de retour incohérente avec le statut",
  );
export type ExtremeVariant = z.infer<typeof extremeVariantSchema>;

const extremesSchema = z
  .strictObject({
    question: z.string().min(1),
    model: z.string().min(1),
    finding: z.string().min(1),
    confidence: confidenceSchema,
    confidence_reason: z.string().min(1),
    method_note: z.string().min(1),
    limitations: z.array(z.string()).min(1),
    inputs: z.array(inputSourceSchema).min(1),
    station: z.string().min(1),
    index_label: z.string().min(1),
    period: periodSchema,
    n: z.number().int().min(20),
    covariate: z.string().min(1),
    today_year: z.number().int(),
    past_year: z.number().int(),
    preindustrial_period: periodSchema,
    past_return_period: z.number().gt(1),
    ci_level: z.number().gt(0).lt(1),
    g_today: z.number(),
    g_past: z.number(),
    g_preindustrial: z.number(),
    mu0: z.number(),
    alpha: estimateSchema,
    sigma: estimateSchema,
    xi: estimateSchema,
    lrt_p: z.number().min(0).max(1),
    ks_p: z.number().min(0).max(1),
    n_boot: z.number().int(),
    n_failed: z.number().int(),
    reference: estimateSchema,
    reference_source: z.string().min(1),
    events: z.array(extremeEventSchema).min(1),
    curve: gevCurveSchema,
    series: extremeSeriesSchema,
    variants: z.array(extremeVariantSchema),
    criteria: z.array(criterionSchema).min(1),
    script: z.string().min(1),
    etl_version: z.string().min(1),
    extracted_at: isoDate,
  })
  .refine((r) => {
    const ok = new Map(r.criteria.map((c) => [c.id, c.satisfied]));
    const core = [1, 2, 3, 4, 5, 6].every((i) => ok.get(`X${i}`) === true);
    const expected = core ? "elevee" : ok.get("X3") ? "moyenne" : "non_etabli";
    return r.confidence === expected;
  }, "extrêmes : confiance incohérente avec les critères (règle D-AO)");
export type Extremes = z.infer<typeof extremesSchema>;

export const demonstrationSchema = z.strictObject({
  schema_version: z.literal("1.0"),
  generated_at: isoDate,
  analyses: z
    .array(
      z
        .strictObject({
          id: z.string().regex(SLUG),
          phase: z.string().regex(/^p10\.[0-9]+$/),
          title: z.string().min(1),
          question: z.string().min(1),
          status: z.enum(["publie", "prevu"]),
          regression: regressionSchema.nullable(),
          extremes: extremesSchema.nullable(),
        })
        .refine((a) => {
          const results = [a.regression, a.extremes].filter((x) => x !== null).length;
          return results <= 1 && (a.status === "publie") === (results === 1);
        }, "« publie » si et seulement si un seul résultat est fourni"),
    )
    .min(1),
});
export type Demonstration = z.infer<typeof demonstrationSchema>;
