// Couche données : seule partie du site qui lit les fichiers.
// Appelée uniquement au build (pages statiques). Un fichier invalide fait
// échouer le build : aucune page ne peut afficher silencieusement un résultat faux.
import { readFileSync } from "node:fs";
import { join } from "node:path";
import type { z } from "zod";

import { indicatorSchema, manifestSchema, type Indicator, type Manifest, type Scale } from "./schema";

const DATA_DIR = join(process.cwd(), ".data");

function load<T>(relPath: string, schema: z.ZodType<T>): T {
  const raw = JSON.parse(readFileSync(join(DATA_DIR, relPath), "utf-8"));
  const parsed = schema.safeParse(raw);
  if (!parsed.success) {
    const issues = parsed.error.issues.map((i) => `  - ${i.path.join(".") || "(racine)"} : ${i.message}`);
    throw new Error(`Données invalides dans ${relPath} :\n${issues.join("\n")}`);
  }
  return parsed.data;
}

let manifestCache: Manifest | undefined;

export function getManifest(): Manifest {
  manifestCache ??= load("manifest.json", manifestSchema);
  return manifestCache;
}

export function listIndicators(scale: Scale) {
  return getManifest().indicators.filter((e) => e.scale === scale);
}

export function getIndicator(scale: Scale, id: string): Indicator | undefined {
  const entry = getManifest().indicators.find((e) => e.scale === scale && e.id === id);
  if (!entry) return undefined;
  const ind = load(entry.path, indicatorSchema);
  if (ind.scale !== scale || ind.id !== id) {
    throw new Error(`${entry.path} : scale/id incohérents avec le manifeste`);
  }
  return ind;
}

/** Indicateurs d'une échelle regroupés par `group`, synthèses d'abord, dans l'ordre du manifeste. */
export function groupedIndicators(scale: Scale) {
  const groups = new Map<string, ReturnType<typeof listIndicators>>();
  for (const e of listIndicators(scale)) {
    const g = e.group ?? "Indicateurs";
    groups.set(g, [...(groups.get(g) ?? []), e]);
  }
  return [...groups.entries()].sort(([a], [b]) => Number(b.startsWith("Synthèse")) - Number(a.startsWith("Synthèse")));
}

/** Points de carte : une station par indicateur mono-station dont l'identifiant commence par `prefix`. */
export function stationPoints(scale: Scale, prefix: string, trendLabelStart: string) {
  return listIndicators(scale)
    .filter((e) => e.id.startsWith(prefix))
    .map((e) => getIndicator(scale, e.id)!)
    .filter((ind) => ind.stations.length === 1)
    .map((ind) => {
      const st = ind.stations[0]!;
      const t = ind.alt_trends.find((a) => a.label.startsWith(trendLabelStart));
      return {
        id: st.id,
        name: st.name,
        lat: st.latitude,
        lon: st.longitude,
        value: t ? t.slope_per_decade : null,
        href: `/${scale}/${ind.id}`,
      };
    });
}
