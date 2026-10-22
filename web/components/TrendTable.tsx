// Toutes les tendances calculées pour un indicateur : période principale et fenêtres de comparaison.
// La colonne « classique » montre l'effet de la correction de l'autocorrélation (Hamed-Rao).
import { fmtPValue, fmtSigned } from "@/lib/format";
import type { Trend } from "@/lib/schema";

export default function TrendTable({ trends, unit }: { trends: Trend[]; unit: string }) {
  if (trends.length === 0) return null;
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[34rem] text-left text-sm">
        <thead className="text-xs uppercase tracking-wide text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-2 pr-3 font-medium">Période</th>
            <th className="py-2 pr-3 font-medium">Pente de Sen ({unit}/déc.)</th>
            <th className="py-2 pr-3 font-medium">IC 95 %</th>
            <th className="py-2 pr-3 font-medium">Hamed-Rao</th>
            <th className="py-2 font-medium">Classique</th>
          </tr>
        </thead>
        <tbody className="font-mono tabular-nums">
          {trends.map((t) => (
            <tr key={t.label} className="border-b border-[var(--rule)]">
              <td className="py-2 pr-3 font-sans">{t.label || `${t.period.start}–${t.period.end}`}</td>
              <td className="py-2 pr-3">{fmtSigned(t.slope_per_decade)}</td>
              <td className="py-2 pr-3 text-[var(--muted)]">
                {t.slope_ci_low !== null && t.slope_ci_high !== null
                  ? `${fmtSigned(t.slope_ci_low)} à ${fmtSigned(t.slope_ci_high)}`
                  : "—"}
              </td>
              <td className="py-2 pr-3">{fmtPValue(t.p_value)}</td>
              <td className="py-2 text-[var(--muted)]">{t.p_value_classical !== null ? fmtPValue(t.p_value_classical) : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
