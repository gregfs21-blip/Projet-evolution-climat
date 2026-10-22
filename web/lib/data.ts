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
