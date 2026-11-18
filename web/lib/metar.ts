// P11 — localités la plus chaude et la plus froide à l'instant t (décisions D-AJ à D-AL, docs/phases.md).
// Lecture du fichier METAR mondial de la NOAA (Aviation Weather Center), contrôle qualité fixé avant développement,
// classement. Fonctions pures, sans dépendance : testées par `npm test` (tests/metar.test.mjs).
// Aucune valeur n'est corrigée : une observation qui échoue à une règle est exclue et comptée.

export const MAX_AGE_MIN = 120;
export const T_MIN = -90;
export const T_MAX = 60;
export const TOP = 5;
export const REFERENCE_ID = "LFBD";
/** Au-delà, la page signale qu'elle n'a pas été régénérée (3 périodes de régénération de 10 min). */
export const STALE_AFTER_MIN = 30;

export type Station = { name: string; country: string | null; elev: number | null };

export type Observation = {
  id: string;
  name: string;
  country: string | null;
  elev: number | null;
  lat: number;
  lon: number;
  temp: number;
  dew: number | null;
  time: string; // ISO UTC
  ageMin: number;
  raw: string;
};

export type Exclusion =
  | "sans température"
  | "trop ancienne"
  | "hors bornes"
  | "point de rosée supérieur à la température"
  | "maintenance"
  | "différente du METAR brut"
  | "station inconnue";

export const EXCLUSIONS: Exclusion[] = [
  "sans température",
  "trop ancienne",
  "hors bornes",
  "point de rosée supérieur à la température",
  "maintenance",
  "différente du METAR brut",
  "station inconnue",
];

export type Snapshot = {
  readAt: string; // ISO UTC
  fileModified: string | null;
  total: number; // stations dans le fichier
  kept: number;
  excluded: Record<Exclusion, number>;
  hottest: Observation[];
  coldest: Observation[];
  reference: Observation | null;
  referenceExclusion: Exclusion | "absente du fichier" | null;
};

/** CSV RFC 4180 minimal : champs entre guillemets, guillemets doublés. */
export function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i]!;
    if (quoted) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else quoted = false;
      } else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") {
      row.push(field);
      field = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      if (row.length > 1 || row[0] !== "") rows.push(row);
      row = [];
      field = "";
    } else field += c;
  }
  if (field !== "" || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function signed(token: string): number {
  return token.startsWith("M") ? -Number(token.slice(1)) : Number(token);
}

/** Groupe température / point de rosée du corps du METAR (degrés entiers, « M » = négatif), avant les remarques. */
export function bodyTemperature(raw: string): { temp: number; dew: number | null } | null {
  const body = raw.split(/\sRMK\s/)[0] ?? raw;
  for (const tok of body.trim().split(/\s+/)) {
    const m = /^(M?\d{2})\/(M?\d{2})?$/.exec(tok);
    if (m) return { temp: signed(m[1]!), dew: m[2] ? signed(m[2]) : null };
  }
  return null;
}

/** Groupe T des remarques nord-américaines (dixièmes de degré) : T12941320 = −29,4 °C / −32,0 °C. */
export function remarkTemperature(raw: string): { temp: number; dew: number | null } | null {
  const rmk = raw.split(/\sRMK\s/)[1];
  if (!rmk) return null;
  for (const tok of rmk.trim().split(/\s+/)) {
    const m = /^T([01])(\d{3})(?:([01])(\d{3}))?$/.exec(tok);
    if (m) {
      const t = (m[1] === "1" ? -1 : 1) * Number(m[2]) / 10;
      const d = m[3] !== undefined ? (m[3] === "1" ? -1 : 1) * Number(m[4]) / 10 : null;
      return { temp: t, dew: d };
    }
  }
  return null;
}

/** Contrôle Q3 : la température du fichier est celle du METAR brut (groupe T s'il existe, sinon groupe du corps). */
export function matchesRaw(temp: number, raw: string): boolean {
  const ref = remarkTemperature(raw) ?? bodyTemperature(raw);
  return ref !== null && Math.abs(ref.temp - temp) <= 0.05;
}

export function isMaintenance(raw: string, flag: string | undefined): boolean {
  return (flag ?? "").toUpperCase() === "TRUE" || /\$\s*=?\s*$/.test(raw.trim());
}

type Row = Record<string, string>;

/** Applique les règles dans l'ordre ; renvoie l'observation retenue ou la première règle échouée. */
export function check(row: Row, stations: Map<string, Station>, now: Date): Observation | Exclusion {
  const raw = (row.raw_text ?? "").trim();
  const id = (row.station_id ?? "").trim();
  const temp = row.temp_c === undefined || row.temp_c === "" ? NaN : Number(row.temp_c);
  if (!Number.isFinite(temp)) return "sans température";
  const time = new Date(row.observation_time ?? "");
  const ageMin = (now.getTime() - time.getTime()) / 60000;
  if (!Number.isFinite(ageMin) || ageMin > MAX_AGE_MIN || ageMin < -10) return "trop ancienne";
  if (temp < T_MIN || temp > T_MAX) return "hors bornes";
  const dew = row.dewpoint_c === undefined || row.dewpoint_c === "" ? null : Number(row.dewpoint_c);
  if (dew !== null && Number.isFinite(dew) && dew > temp + 0.05) return "point de rosée supérieur à la température";
  if (isMaintenance(raw, row.maintenance_indicator_on)) return "maintenance";
  if (!matchesRaw(temp, raw)) return "différente du METAR brut";
  const st = stations.get(id);
  if (!st) return "station inconnue";
  return {
    id,
    name: st.name,
    country: st.country,
    elev: st.elev,
    lat: Number(row.latitude),
    lon: Number(row.longitude),
    temp,
    dew: dew !== null && Number.isFinite(dew) ? dew : null,
    time: time.toISOString(),
    ageMin: Math.max(0, Math.round(ageMin)),
    raw,
  };
}

/** Fichier des stations de l'AWC (JSON) → indicatif OACI (ou identifiant) → nom, pays, altitude. */
export function stationIndex(json: unknown): Map<string, Station> {
  const out = new Map<string, Station>();
  if (!Array.isArray(json)) return out;
  for (const s of json as Record<string, unknown>[]) {
    const key = (s.icaoId as string | null) ?? (s.id as string | null);
    if (!key) continue;
    out.set(key, {
      name: String(s.site ?? key),
      country: typeof s.country === "string" && s.country ? s.country : null,
      elev: typeof s.elev === "number" ? s.elev : null,
    });
  }
  return out;
}

/** Fichier METAR (CSV décompressé) → instantané contrôlé et classé. */
export function snapshot(csv: string, stations: Map<string, Station>, now: Date, fileModified: string | null = null): Snapshot {
  const rows = parseCsv(csv);
  const h = rows.findIndex((r) => r[0] === "raw_text");
  if (h < 0) throw new Error("METAR : en-tête « raw_text » introuvable, format changé");
  const header = rows[h]!;
  // Une ligne par station : la plus récente.
  const latest = new Map<string, Row>();
  for (const r of rows.slice(h + 1)) {
    const row: Row = Object.fromEntries(header.map((k, i) => [k, r[i] ?? ""]));
    const id = row.station_id;
    if (!id) continue;
    const prev = latest.get(id);
    if (!prev || (row.observation_time ?? "") > (prev.observation_time ?? "")) latest.set(id, row);
  }
  const excluded = Object.fromEntries(EXCLUSIONS.map((e) => [e, 0])) as Record<Exclusion, number>;
  const kept: Observation[] = [];
  let reference: Observation | null = null;
  let referenceExclusion: Snapshot["referenceExclusion"] = "absente du fichier";
  for (const [id, row] of latest) {
    const r = check(row, stations, now);
    if (typeof r === "string") {
      excluded[r]++;
      if (id === REFERENCE_ID) referenceExclusion = r;
    } else {
      kept.push(r);
      if (id === REFERENCE_ID) {
        reference = r;
        referenceExclusion = null;
      }
    }
  }
  if (kept.length === 0) throw new Error("METAR : aucune observation retenue");
  // Égalité de température : la mesure la plus récente d'abord, puis l'indicatif (ordre stable et reproductible).
  const order = (a: Observation, b: Observation) => a.ageMin - b.ageMin || a.id.localeCompare(b.id);
  const hottest = [...kept].sort((a, b) => b.temp - a.temp || order(a, b)).slice(0, TOP);
  const coldest = [...kept].sort((a, b) => a.temp - b.temp || order(a, b)).slice(0, TOP);
  return {
    readAt: now.toISOString(),
    fileModified,
    total: latest.size,
    kept: kept.length,
    excluded,
    hottest,
    coldest,
    reference,
    referenceExclusion,
  };
}

/** Âge de la lecture affichée, en minutes ; au-delà de STALE_AFTER_MIN, la page le signale (critère Q5). */
export function staleMinutes(readAt: string, now: Date): number | null {
  const age = (now.getTime() - new Date(readAt).getTime()) / 60000;
  return age > STALE_AFTER_MIN ? Math.round(age) : null;
}
