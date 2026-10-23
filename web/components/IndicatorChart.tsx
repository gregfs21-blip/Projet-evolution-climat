"use client";

// Courbe de la page indicateur, avec deux réglages :
// - anomalie ↔ valeur absolue (possible seulement si la normale de la période de référence est publiée) ;
// - superposition du composite de l'échelle (en mode anomalie, mêmes unités et même référence).
import { useMemo, useState } from "react";

import Segmented from "./Segmented";
import TrendChart from "./TrendChart";

type Props = {
  time: string[];
  value: (number | null)[];
  quality: ("homogenized" | "raw")[] | null;
  unit: string;
  isAnomaly: boolean;
  reference: string | null;
  /** Normale de la période de référence : valeur absolue = anomalie + offset. null = bascule indisponible. */
  offset: number | null;
  trend: { start: number; end: number; fittedStart: number; fittedEnd: number } | null;
  breakpoints: string[];
  composite: { name: string; time: string[]; value: (number | null)[] } | null;
};

export default function IndicatorChart(p: Props) {
  const [mode, setMode] = useState<"anomaly" | "absolute">("anomaly");
  const [withComposite, setWithComposite] = useState(p.composite !== null);
  const absolute = p.isAnomaly && mode === "absolute" && p.offset !== null;
  const off = absolute ? p.offset! : 0;

  const value = useMemo(() => (absolute ? p.value.map((v) => (v === null ? null : v + off)) : p.value), [absolute, off, p.value]);
  const trend = useMemo(
    () => (p.trend && absolute ? { ...p.trend, fittedStart: p.trend.fittedStart + off, fittedEnd: p.trend.fittedEnd + off } : p.trend),
    [absolute, off, p.trend],
  );
  const overlay = useMemo(() => {
    if (!p.composite || !withComposite || absolute) return null;
    const m = new Map(p.composite.time.map((t, i) => [t, p.composite!.value[i] ?? null]));
    return { name: p.composite.name, value: p.time.map((t) => m.get(t) ?? null) };
  }, [p.composite, p.time, withComposite, absolute]);

  return (
    <section aria-label="Série" className="space-y-2">
      {(p.isAnomaly || p.composite) && (
        <div className="flex flex-wrap items-center justify-between gap-3">
          {p.isAnomaly ? (
          <Segmented
            label="Affichage"
            value={mode}
            onChange={setMode}
            options={[
              { key: "anomaly", label: p.reference ? `Écart à ${p.reference}` : "Écart" },
              {
                key: "absolute",
                label: `Valeur absolue (${p.unit})`,
                disabled: p.offset === null,
                title: p.offset === null ? `Indisponible : pas de normale ${p.reference ?? ""} publiée pour cette série` : undefined,
              },
            ]}
          />
          ) : (
            <span />
          )}
          {p.composite && (
            <label className={`flex items-center gap-2 text-sm ${absolute ? "opacity-40" : ""}`}>
              <input
                type="checkbox"
                checked={withComposite}
                disabled={absolute}
                onChange={(e) => setWithComposite(e.target.checked)}
                className="accent-[var(--ink)]"
              />
              Superposer {p.composite.name}
            </label>
          )}
        </div>
      )}
      <TrendChart
        time={p.time}
        value={value}
        unit={p.unit}
        isAnomaly={p.isAnomaly && !absolute}
        trend={trend}
        breakpoints={p.breakpoints}
        quality={p.quality}
        overlay={overlay}
      />
      <ul className="flex flex-wrap gap-x-5 gap-y-1 text-xs text-[var(--muted)]">
        {p.isAnomaly && !absolute ? (
          <>
            <li>
              <i className="mr-1.5 inline-block h-2.5 w-3 bg-[var(--warm)] align-[-1px]" />
              au-dessus de {p.reference ? `la moyenne ${p.reference}` : "la référence"}
            </li>
            <li>
              <i className="mr-1.5 inline-block h-2.5 w-3 bg-[var(--cold)] align-[-1px]" />
              en dessous
            </li>
          </>
        ) : (
          <li>
            <i className="mr-1.5 inline-block h-0.5 w-4 bg-[var(--ink)] align-middle" />
            valeur annuelle
          </li>
        )}
        {p.quality?.includes("raw") && (
          <li>
            <i className="mr-1.5 inline-block h-2.5 w-3 bg-[var(--muted)] opacity-50 align-[-1px]" />
            années non homogénéisées, hors tendance
          </li>
        )}
        {trend && (
          <li>
            <i className="mr-1.5 inline-block w-4 border-t-2 border-dashed border-[var(--accent)] align-middle" />
            droite de Sen
          </li>
        )}
        {overlay && (
          <li>
            <i className="mr-1.5 inline-block h-0.5 w-4 bg-[var(--ink)] opacity-55 align-middle" />
            {overlay.name}
          </li>
        )}
      </ul>
    </section>
  );
}
