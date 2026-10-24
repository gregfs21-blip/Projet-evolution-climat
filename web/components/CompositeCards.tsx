// Chiffres-clés des composites d'un thème (ex. TN, TM, TX) : une carte cliquable par variable.
import Link from "next/link";

import MiniBars from "./MiniBars";
import { headlineCards } from "@/lib/family";
import { fmt1, fmtPValue, fmtSigned, fmtSigned1 } from "@/lib/format";
import type { Scale } from "@/lib/schema";

export default function CompositeCards({ scale, theme }: { scale: Scale; theme: string }) {
  const items = headlineCards(scale, theme);
  if (items.length === 0) return null;
  return (
    <div className={`grid gap-4 ${items.length >= 3 ? "sm:grid-cols-3" : items.length === 2 ? "sm:grid-cols-2" : ""}`}>
      {items.map(({ variable, ind, href, place }) => {
        const t = ind.trend;
        const c = ind.headline === "normals" ? ind.normals_comparison : null;
        return (
          <Link
            key={`${variable.id}-${place.id}`}
            href={href}
            className="block rounded-lg border border-[var(--rule)] bg-[var(--card)] px-4 pt-3 pb-2 transition-colors hover:border-[var(--muted)]"
          >
            <div className="text-xs uppercase tracking-wide text-[var(--muted)]">
              {variable.label} · {place.kind === "station" ? place.name : variable.code}
            </div>
            {c ? (
              // Indice rare (critère E9) : l'écart entre normales est mis en avant, pas la pente.
              <>
                <div className="mt-1 font-mono text-3xl tabular-nums">
                  {fmtSigned1(c.difference)} <span className="text-sm text-[var(--muted)]">{ind.unit} / an</span>
                </div>
                <div className="font-mono text-xs text-[var(--muted)]">
                  {fmt1(c.first_value)} → {fmt1(c.second_value)} · {c.first.start}-{c.first.end} → {c.second.start}-{c.second.end}
                </div>
                <div className="mt-1.5 text-sm">
                  écart entre normales, {c.significant ? "significatif" : "non significatif"}{" "}
                  <span className="text-[var(--muted)]">({fmtPValue(c.p_value)})</span>
                </div>
              </>
            ) : t ? (
              <>
                <div className="mt-1 font-mono text-3xl tabular-nums">
                  {fmtSigned(t.slope_per_decade)} <span className="text-sm text-[var(--muted)]">{ind.unit} / déc.</span>
                </div>
                <div className="font-mono text-xs text-[var(--muted)]">
                  {t.slope_ci_low !== null && t.slope_ci_high !== null
                    ? `IC 95 % ${fmtSigned(t.slope_ci_low)} à ${fmtSigned(t.slope_ci_high)} · `
                    : ""}
                  {t.period.start}–{t.period.end}
                </div>
                <div className="mt-1.5 text-sm">
                  soit <b className="font-mono">{fmtSigned1(t.fitted_end - t.fitted_start)} {ind.unit}</b> sur la période
                  {!t.significant && <span className="text-[var(--muted)]"> (non significatif)</span>}
                </div>
              </>
            ) : (
              <p className="mt-2 text-sm text-[var(--muted)]">Pas de tendance calculée.</p>
            )}
            <MiniBars
              time={ind.series.time}
              value={ind.series.value}
              quality={ind.series.quality}
              trend={t && !c ? { start: t.period.start, end: t.period.end, fittedStart: t.fitted_start, fittedEnd: t.fitted_end } : null}
              isAnomaly={ind.is_anomaly}
            />
          </Link>
        );
      })}
    </div>
  );
}
