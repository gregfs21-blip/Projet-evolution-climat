// Chiffres-clés des composites d'une échelle (TN, TM, TX) : une carte cliquable par variable.
import Link from "next/link";

import MiniBars from "./MiniBars";
import { composites, VARIABLES } from "@/lib/family";
import { fmtSigned, fmtSigned1 } from "@/lib/format";
import type { Scale } from "@/lib/schema";

export default function CompositeCards({ scale }: { scale: Scale }) {
  const items = composites(scale);
  if (items.length === 0) return null;
  return (
    <div className="grid gap-4 sm:grid-cols-3">
      {items.map(({ variable, ind, href }) => {
        const t = ind.trend;
        const v = VARIABLES[variable];
        return (
          <Link
            key={variable}
            href={href}
            className="block rounded-lg border border-[var(--rule)] bg-[var(--card)] px-4 pt-3 pb-2 transition-colors hover:border-[var(--muted)]"
          >
            <div className="text-xs uppercase tracking-wide text-[var(--muted)]">
              Températures {v.plural} · {v.code}
            </div>
            {t ? (
              <>
                <div className="mt-1 font-mono text-3xl tabular-nums">
                  {fmtSigned(t.slope_per_decade)} <span className="text-sm text-[var(--muted)]">°C / déc.</span>
                </div>
                <div className="font-mono text-xs text-[var(--muted)]">
                  {t.slope_ci_low !== null && t.slope_ci_high !== null
                    ? `IC 95 % ${fmtSigned(t.slope_ci_low)} à ${fmtSigned(t.slope_ci_high)} · `
                    : ""}
                  {t.period.start}–{t.period.end}
                </div>
                <div className="mt-1.5 text-sm">
                  soit <b className="font-mono">{fmtSigned1(t.fitted_end - t.fitted_start)} °C</b> sur la période
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
              trend={t ? { start: t.period.start, end: t.period.end, fittedStart: t.fitted_start, fittedEnd: t.fitted_end } : null}
            />
          </Link>
        );
      })}
    </div>
  );
}
