// Échelle de couleur des tendances, en °C par décennie.
// ABSOLUE et FIXE : la même pente a toujours la même couleur, quelle que soit la page ou la station.
// (L'ancienne carte normalisait entre le minimum et le maximum observés : un écart de 0,02 °C/déc.,
// très inférieur à l'incertitude, y apparaissait comme un contraste bleu/rouge.)
// Divergente autour de zéro : bleu = refroidissement, rouge = réchauffement.
// Module pur, utilisable côté serveur comme côté navigateur.

export const HEAT_MAX = 0.5; // °C/déc. ; au-delà, la couleur sature

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

/** Couleur de fond et couleur de texte lisible pour une pente (°C/déc.). */
export function heatColor(slope: number): { bg: string; fg: string } {
  const k = Math.min(1, Math.abs(slope) / HEAT_MAX);
  const [r, g, b] = interp(slope >= 0 ? WARM : COLD, k);
  return { bg: `rgb(${r} ${g} ${b})`, fg: k > 0.6 ? "#ffffff" : "#1b1e22" };
}

/** Arrêts du dégradé de légende, de −HEAT_MAX à +HEAT_MAX. */
export function heatGradient(steps = 10): string {
  const stops = Array.from({ length: steps + 1 }, (_, i) => {
    const v = -HEAT_MAX + (2 * HEAT_MAX * i) / steps;
    return `${heatColor(v).bg} ${(i / steps) * 100}%`;
  });
  return `linear-gradient(90deg, ${stops.join(", ")})`;
}
