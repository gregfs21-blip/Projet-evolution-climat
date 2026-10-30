// Couche données : seule partie du site qui lit les fichiers.
// Appelée uniquement au build (pages statiques). Un fichier invalide fait
// échouer le build : aucune page ne peut afficher silencieusement un résultat faux.
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { z } from "zod";

import {
  indicatorSchema,
  manifestSchema,
  validationReportSchema,
  coverageSchema,
  departmentMapSchema,
  type Coverage,
  type DepartmentMap,
  type Indicator,
  type Manifest,
  type Scale,
  type ValidationReport,
} from "./schema";

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

const indicatorCache = new Map<string, Indicator>();

export function getIndicator(scale: Scale, id: string): Indicator | undefined {
  const key = `${scale}/${id}`;
  const cached = indicatorCache.get(key);
  if (cached) return cached;
  const entry = getManifest().indicators.find((e) => e.scale === scale && e.id === id);
  if (!entry) return undefined;
  const ind = load(entry.path, indicatorSchema);
  if (ind.scale !== scale || ind.id !== id) {
    throw new Error(`${entry.path} : scale/id incohérents avec le manifeste`);
  }
  indicatorCache.set(key, ind);
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

/**
 * Rapport de validation d'une phase, s'il est publié. Absent = rien n'est affiché (jamais de valeur
 * par défaut). Présent mais invalide = le build échoue, comme pour un indicateur.
 */
export function getValidation(phase: string): ValidationReport | undefined {
  const rel = `validation-${phase}.json`;
  if (!existsSync(join(DATA_DIR, rel))) return undefined;
  return load(rel, validationReportSchema);
}

/** Couverture du projet (paramètres × échelles). Absente = page vide, jamais de valeur par défaut. */
export function getCoverage(): Coverage | undefined {
  if (!existsSync(join(DATA_DIR, "couverture.json"))) return undefined;
  return load("couverture.json", coverageSchema);
}

/** Carte départementale des tendances (P5 bis). Absente = rien n'est affiché. */
export function getDepartmentMap(): DepartmentMap | undefined {
  if (!existsSync(join(DATA_DIR, "carte-departements.json"))) return undefined;
  return load("carte-departements.json", departmentMapSchema);
}
