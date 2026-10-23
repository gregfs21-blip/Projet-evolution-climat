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
};

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
  const [r, g, b] = interp(slope >= 0 ? WARM : COLD, k);
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
