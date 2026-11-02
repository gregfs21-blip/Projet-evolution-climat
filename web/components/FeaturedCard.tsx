// Carte de chiffre-clé de l'accueil : tout vient du JSON de l'indicateur.
import Link from "next/link";

import ConfidenceBadge from "./ConfidenceBadge";
import MiniBars from "./MiniBars";
import { fmt, fmtSigned, fmtSigned1 } from "@/lib/format";
import type { Indicator, Trend } from "@/lib/schema";

function lastValue(ind: Indicator) {
  for (let i = ind.series.value.length - 1; i >= 0; i--) {
    const v = ind.series.value[i];
    if (v !== null && v !== undefined && ind.series.quality?.[i] !== "raw") return { v, year: ind.series.time[i]! };
  }
  return null;
}

export default function FeaturedCard({ ind, trend: t, label, show, href }: { ind: Indicator; trend: Trend | null; label: string; show: "slope" | "last"; href: string }) {
  const last = lastValue(ind);
  return (
    <Link href={href} className="card flex flex-col gap-1 px-4 pt-3.5 pb-3 transition-colors hover:border-[var(--primary)]">
      <span className="text-sm font-medium">{label}</span>
      {show === "last" && last ? (
        <>
          <span className="text-3xl font-semibold tracking-tight tabular-nums">
            {fmt(last.v)} <span className="text-sm font-normal text-[var(--muted)]">{ind.unit}</span>
          </span>
          <span className="text-xs text-[var(--muted)]">
            en {last.year}
            {t && `, ${fmtSigned(t.slope_per_decade)} ${ind.unit} par décennie depuis ${t.period.start}`}
          </span>
        </>
      ) : t ? (
        <>
          <span className="text-3xl font-semibold tracking-tight tabular-nums">
            {fmtSigned(t.slope_per_decade)} <span className="text-sm font-normal text-[var(--muted)]">{ind.unit}/décennie</span>
          </span>
          <span className="text-xs text-[var(--muted)]">
            {t.period.start}-{t.period.end}, soit {fmtSigned1(t.fitted_end - t.fitted_start)} {ind.unit} sur la période
          </span>
        </>
      ) : null}
      <div className="mt-auto pt-1">
        <MiniBars
          time={ind.series.time}
          value={ind.series.value}
          quality={ind.series.quality}
          isAnomaly={ind.is_anomaly}
          trend={t ? { start: t.period.start, end: t.period.end, fittedStart: t.fitted_start, fittedEnd: t.fitted_end } : null}
        />
      </div>
      <span className="mt-1">
        <ConfidenceBadge level={ind.confidence} />
      </span>
    </Link>
  );
}
