// Indicateur clé : la tendance résumée en un chiffre, avec son incertitude.
import { fmtPValue, fmtSigned } from "@/lib/format";
import type { Trend } from "@/lib/schema";

export default function KeyFigure({ trend, unit }: { trend: Trend | null; unit: string }) {
  if (!trend) {
    return <p className="text-sm text-[var(--muted)]">Pas de tendance calculée pour cet indicateur.</p>;
  }
  const ci =
    trend.slope_ci_low !== null && trend.slope_ci_high !== null
      ? `IC ${Math.round((1 - trend.alpha) * 100)} % : ${fmtSigned(trend.slope_ci_low)} à ${fmtSigned(trend.slope_ci_high)}`
      : null;

  return (
    <dl className="grid grid-cols-2 gap-x-6 gap-y-4 sm:grid-cols-4">
      <div className="col-span-2">
        <dt className="text-xs uppercase tracking-wide text-[var(--muted)]">Pente de Sen</dt>
        <dd className="font-mono text-3xl tabular-nums">
          {fmtSigned(trend.slope_per_decade)} <span className="text-base">{unit} / décennie</span>
        </dd>
        {ci && <dd className="font-mono text-xs text-[var(--muted)]">{ci}</dd>}
      </div>
      <div>
        <dt className="text-xs uppercase tracking-wide text-[var(--muted)]">Significativité</dt>
        <dd className="font-mono tabular-nums">{fmtPValue(trend.p_value)}</dd>
        <dd className="text-xs text-[var(--muted)]">
          {trend.significant ? "significative" : "non significative"} au seuil {Math.round(trend.alpha * 100)} %
        </dd>
      </div>
      <div>
        <dt className="text-xs uppercase tracking-wide text-[var(--muted)]">Période</dt>
        <dd className="font-mono tabular-nums">
          {trend.period.start}–{trend.period.end}
        </dd>
      </div>
      <div className="col-span-2 sm:col-span-4">
        <dt className="sr-only">Méthode</dt>
        <dd className="text-xs text-[var(--muted)]">Méthode : {trend.method}</dd>
      </div>
    </dl>
  );
}
