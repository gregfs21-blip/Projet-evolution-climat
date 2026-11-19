"use client";

// Nuage de points annuel (température mondiale lissée en abscisse, anomalie régionale en ordonnée) et droite ajustée
// (P10.3). Les points et la droite viennent de demonstration.json : la droite relie les valeurs ajustées publiées
// (c + k·G) aux deux extrémités de G, rien n'est réestimé ici.
import { useEffect, useRef } from "react";

function cssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

const nf = (v: number, d = 2, sign = false) =>
  v.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d, signDisplay: sign ? "always" : "auto" });

export default function ScatterFitChart({
  years,
  x,
  y,
  fitted,
  rawYears,
  xLabel,
  yLabel,
  fitLabel,
  label,
}: {
  years: number[];
  x: number[];
  y: number[];
  fitted: number[];
  rawYears: number[];
  xLabel: string;
  yLabel: string;
  fitLabel: string;
  label: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let disposed = false;
    let cleanup = () => {};
    (async () => {
      const echarts = await import("echarts");
      if (disposed || !ref.current) return;
      const chart = echarts.init(ref.current, undefined, { renderer: "canvas" as const });
      const render = () => {
        const ink = cssVar("--ink");
        const muted = cssVar("--muted");
        const rule = cssVar("--rule");
        const warm = cssVar("--warm");
        const accent = cssVar("--accent");
        const raw = new Set(rawYears);
        const pts = years.map((yr, i) => ({ value: [x[i]!, y[i]!, yr], raw: raw.has(yr) }));
        // Extrémités de la droite : années de G minimal et maximal, valeurs ajustées publiées.
        let iMin = 0;
        let iMax = 0;
        x.forEach((v, i) => {
          if (v < x[iMin]!) iMin = i;
          if (v > x[iMax]!) iMax = i;
        });
        chart.setOption(
          {
            animation: false,
            textStyle: { fontFamily: `${cssVar("--font-ui") || "system-ui"}, sans-serif`, color: muted },
            grid: { left: 48, right: 16, top: 16, bottom: 44 },
            tooltip: {
              trigger: "item" as const,
              backgroundColor: cssVar("--paper"),
              borderColor: rule,
              textStyle: { color: ink },
              formatter: (p: unknown) => {
                const q = p as { seriesType: string; value: [number, number, number?] };
                if (q.seriesType !== "scatter") return fitLabel;
                return `${q.value[2]}<br/>${xLabel} : ${nf(q.value[0], 2, true)} °C<br/>${yLabel} : <b>${nf(q.value[1], 2, true)} °C</b>`;
              },
            },
            xAxis: {
              type: "value" as const,
              scale: true,
              name: `${xLabel} (°C)`,
              nameLocation: "middle" as const,
              nameGap: 28,
              nameTextStyle: { color: muted },
              axisLine: { onZero: false, lineStyle: { color: rule } },
              axisLabel: { color: muted, formatter: (v: number) => v.toLocaleString("fr-FR") },
              splitLine: { lineStyle: { color: rule, type: "dashed" as const } },
            },
            yAxis: {
              type: "value" as const,
              scale: true,
              name: "°C",
              nameTextStyle: { color: muted, align: "right" as const },
              axisLine: { onZero: false },
              axisLabel: { color: muted, formatter: (v: number) => v.toLocaleString("fr-FR") },
              splitLine: { lineStyle: { color: rule, type: "dashed" as const } },
            },
            series: [
              {
                type: "scatter" as const,
                symbolSize: 6,
                data: pts.map((p) => ({
                  value: p.value,
                  itemStyle: p.raw ? { color: "transparent", borderColor: warm, borderWidth: 1.2 } : { color: warm, opacity: 0.75 },
                })),
              },
              {
                type: "line" as const,
                symbol: "none",
                lineStyle: { color: accent, width: 2 },
                data: [
                  [x[iMin]!, fitted[iMin]!],
                  [x[iMax]!, fitted[iMax]!],
                ],
              },
            ],
          },
          true,
        );
      };
      render();
      const media = window.matchMedia("(prefers-color-scheme: dark)");
      const onResize = () => chart.resize();
      window.addEventListener("resize", onResize);
      media.addEventListener("change", render);
      cleanup = () => {
        window.removeEventListener("resize", onResize);
        media.removeEventListener("change", render);
        chart.dispose();
      };
    })();
    return () => {
      disposed = true;
      cleanup();
    };
  }, [years, x, y, fitted, rawYears, xLabel, yLabel, fitLabel]);

  return (
    <div>
      <div ref={ref} className="h-[300px] w-full sm:h-[360px]" role="img" aria-label={label} />
      <ul className="mt-1 flex flex-wrap gap-x-5 gap-y-1 text-xs text-[var(--muted)]">
        <li>
          <i className="mr-1.5 inline-block h-2 w-2 rounded-full align-middle" style={{ background: "var(--warm)" }} />
          Une année (homogénéisée)
        </li>
        {rawYears.length > 0 && (
          <li>
            <i className="mr-1.5 inline-block h-2 w-2 rounded-full align-middle" style={{ border: "1px solid var(--warm)" }} />
            Une année non homogénéisée
          </li>
        )}
        <li>
          <i className="mr-1.5 inline-block w-4 align-middle" style={{ borderTop: "2px solid var(--accent)" }} />
          {fitLabel}
        </li>
      </ul>
    </div>
  );
}
