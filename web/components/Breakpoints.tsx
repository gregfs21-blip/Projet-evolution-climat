// Ruptures détectées, avec leur statut : une rupture n'est « établie » que si elle résiste
// au retrait de la tendance et ne coïncide pas avec une correction d'homogénéité.
import type { Indicator } from "@/lib/schema";

export function establishedBreaks(ind: Indicator): string[] {
  return ind.breakpoints
    .filter((b) => !b.possible_artifact && b.detrended_p_value !== null && b.detrended_p_value < 0.05)
    .map((b) => b.time);
}

export default function Breakpoints({ ind }: { ind: Indicator }) {
  if (!ind.trend && !!ind.series.quality?.length && ind.series.quality.every((q) => q === "raw")) {
    return <p className="text-xs text-[var(--muted)]">Pas de test de rupture : série brute, non homogénéisée (règle C2).</p>;
  }
  if (ind.breakpoints.length === 0) {
    return <p className="text-xs text-[var(--muted)]">Aucune rupture significative détectée (test de Pettitt).</p>;
  }
  return (
    <ul className="space-y-1 text-xs text-[var(--muted)]">
      {ind.breakpoints.map((b) => {
        const established = !b.possible_artifact && b.detrended_p_value !== null && b.detrended_p_value < 0.05;
        return (
          <li key={b.time}>
            <span className="font-medium text-[var(--ink)]">
              Rupture {b.time} ({b.method}) — {established ? "établie" : "non établie"}
            </span>
            {b.note ? ` : ${b.note}.` : "."}
          </li>
        );
      })}
    </ul>
  );
}
