// Échelle de couleur des tendances (unité de l'indicateur par décennie).
// ABSOLUE et FIXE par unité : la même pente a toujours la même couleur, quelle que soit la page ou la station.
// (L'ancienne carte normalisait entre le minimum et le maximum observés : un écart de 0,02 °C/déc.,
// très inférieur à l'incertitude, y apparaissait comme un contraste bleu/rouge.)
// Divergente autour de zéro : bleu = baisse, rouge = hausse. Pour les températures, rouge = réchauffement ;
// pour une variable comme les jours de gel, une baisse (bleu) traduit aussi un réchauffement : la légende
// d'un tel thème devra le dire (P2).
// Module pur, utilisable côté serveur comme côté navigateur.

// Saturation par unité de tendance (unité de l'indicateur par décennie). Une unité absente de cette
// table n'est pas colorée : on ne devine pas d'échelle, elle doit être choisie et inscrite ici.
const HEAT_MAX: Record<string, number> = {
  "°C": 0.5,
  // P2a, nombres de jours : ±5 jours par décennie (choix d'affichage, ordre de grandeur des journées estivales).
  jours: 5,
  // Pluie, carte départementale (P5 bis, fixé avant calcul le 30/10/2026) : ± 10 % par décennie.
  "%": 10,
};

// Unités dont la hausse se lit en bleu (plus d'eau) et la baisse en brun (moins d'eau).
const WET_UNITS = new Set(["%"]);

export function heatMax(unit: string): number | null {
  return HEAT_MAX[unit] ?? null;
}

type RGB = [number, number, number];
const NEUTRAL: RGB = [240, 234, 222];
const WARM: [number, RGB][] = [
  [0, NEUTRAL],
  [0.5, [232, 160, 98]],
  [1, [164, 40, 32]],
];
const COLD: [number, RGB][] = [
  [0, NEUTRAL],
  [0.5, [128, 170, 212]],
  [1, [35, 85, 150]],
];
const DRY: [number, RGB][] = [
  [0, NEUTRAL],
  [0.5, [205, 170, 110]],
  [1, [130, 82, 30]],
];

function interp(stops: [number, RGB][], k: number): RGB {
  for (let i = 1; i < stops.length; i++) {
    const [a, ca] = stops[i - 1]!;
    const [b, cb] = stops[i]!;
    if (k <= b) {
      const t = (k - a) / (b - a);
      return [0, 1, 2].map((j) => Math.round(ca[j]! + t * (cb[j]! - ca[j]!))) as RGB;
    }
  }
  return stops[stops.length - 1]![1];
}

/** Couleur de fond et couleur de texte lisible pour une pente, sur l'échelle fixe de son unité. */
export function heatColor(slope: number, unit: string): { bg: string; fg: string } {
  const max = heatMax(unit);
  if (max === null) return { bg: "var(--hover)", fg: "var(--ink)" };
  const k = Math.min(1, Math.abs(slope) / max);
  const wet = WET_UNITS.has(unit);
  const [r, g, b] = interp(slope >= 0 ? (wet ? COLD : WARM) : wet ? DRY : COLD, k);
  return { bg: `rgb(${r} ${g} ${b})`, fg: k > 0.6 ? "#ffffff" : "#1b1e22" };
}

/** Arrêts du dégradé de légende, de −max à +max. */
export function heatGradient(unit: string, steps = 10): string {
  const max = heatMax(unit) ?? 1;
  const stops = Array.from({ length: steps + 1 }, (_, i) => {
    const v = -max + (2 * max * i) / steps;
    return `${heatColor(v, unit).bg} ${(i / steps) * 100}%`;
  });
  return `linear-gradient(90deg, ${stops.join(", ")})`;
}

// Bandes climatiques : écart annuel à la référence, sur une échelle unique pour toutes les échelles géographiques,
// de sorte qu'une même couleur signifie partout le même écart. ±3 °C : choix d'affichage, englobe les extrêmes publiés.
export const ANOMALY_MAX = 3;
const ANOMALY_RAMP: RGB[] = [
  [8, 48, 107], [8, 81, 156], [33, 113, 181], [66, 146, 198], [107, 174, 214], [158, 202, 225], [198, 219, 239], [222, 235, 247],
  [254, 224, 210], [252, 187, 161], [252, 146, 114], [251, 106, 74], [239, 59, 44], [203, 24, 29], [165, 15, 21], [103, 0, 13],
];

/** Couleur d'un écart annuel (°C). */
export function anomalyColor(v: number): string {
  const k = (Math.max(-ANOMALY_MAX, Math.min(ANOMALY_MAX, v)) + ANOMALY_MAX) / (2 * ANOMALY_MAX);
  const pos = k * (ANOMALY_RAMP.length - 1);
  const i = Math.min(ANOMALY_RAMP.length - 2, Math.floor(pos));
  const a = ANOMALY_RAMP[i]!;
  const b = ANOMALY_RAMP[i + 1]!;
  const [r, g, bl] = [0, 1, 2].map((j) => Math.round(a[j]! + (pos - i) * (b[j]! - a[j]!)));
  return `rgb(${r} ${g} ${bl})`;
}

/** Dégradé de légende, de −ANOMALY_MAX à +ANOMALY_MAX. */
export function anomalyGradient(): string {
  const n = ANOMALY_RAMP.length - 1;
  return `linear-gradient(90deg, ${ANOMALY_RAMP.map(([r, g, b], i) => `rgb(${r} ${g} ${b}) ${(i / n) * 100}%`).join(", ")})`;
}
