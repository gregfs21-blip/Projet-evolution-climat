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
});

const breakpointSchema = z.strictObject({
  time: z.string(),
  method: z.string(),
  p_value: z.number().min(0).max(1).nullable(),
});

const seriesSchema = z
  .strictObject({ time: z.array(z.string()).min(1), value: z.array(z.number().nullable()) })
  .refine((s) => s.time.length === s.value.length, "series.time et series.value de longueurs différentes")
  .refine((s) => s.time.every((t, i) => i === 0 || s.time[i - 1]! < t), "series.time non trié ou dupliqué");

export const indicatorSchema = z
  .strictObject({
    schema_version: z.literal("1.0"),
    id: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/),
    scale: scaleSchema,
    title: z.string().min(1),
    unit: z.string(),
    description: z.string().min(1),
    frequency: z.enum(["annual", "seasonal", "monthly", "daily"]),
    is_anomaly: z.boolean(),
    reference_period: periodSchema.nullable(),
    series: seriesSchema,
    trend: trendSchema.nullable(),
    breakpoints: z.array(breakpointSchema),
    finding: z.string().min(1),
    confidence: confidenceSchema,
    limitations: z.array(z.string().trim().min(1)).min(1),
    provenance: provenanceSchema,
    is_demo: z.boolean(),
  })
  .refine((d) => !d.is_anomaly || d.reference_period !== null, "anomalie sans reference_period")
  .refine(
    (d) => !d.trend || d.trend.significant === d.trend.p_value < d.trend.alpha,
    "trend.significant incohérent avec p_value",
  )
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
});
export type ManifestEntry = z.infer<typeof manifestEntrySchema>;

export const manifestSchema = z.strictObject({
  schema_version: z.literal("1.0"),
  generated_at: isoDate,
  etl_version: z.string(),
  indicators: z.array(manifestEntrySchema),
});
export type Manifest = z.infer<typeof manifestSchema>;
