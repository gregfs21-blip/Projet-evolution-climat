"use client";

// Niveaux de retour (P10.2) : intensité en fonction de la période de retour, axe des périodes logarithmique,
// pour deux climats (passé et aujourd'hui) avec leur intervalle à 95 %, et les observations ramenées à chaque climat.
// Tous les points viennent de demonstration.json (courbe calculée par etl/demo_extremes.py) ; rien n'est recalculé.
import { useEffect, useRef } from "react";

import type { GevCurve } from "@/lib/schema";

function cssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

const nf = (v: number, d = 1) => v.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });

export default function ReturnLevelChart({
  curve,
  pastLabel,
  todayLabel,
  marker,
  ciLabel,
  label,
}: {
  curve: GevCurve;
  pastLabel: string;
  todayLabel: string;
  /** Valeur observée remarquable (ligne horizontale), ex. le record. */
  marker?: { value: number; label: string };
  /** Niveau des intervalles, déjà mis en forme (ex. « 95 % »). */
  ciLabel: string;
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
        const cold = cssVar("--cold");
        const P = curve.periods;
        const all = [...P, ...curve.obs_periods];
        const xMin = 10 ** Math.floor(Math.log10(Math.min(...all)));
        const xMax = 10 ** Math.ceil(Math.log10(Math.max(...all)));
        // Bande = borne basse (transparente) + écart haut − bas empilé et rempli.
        const band = (low: number[], high: number[], color: string, stack: string) => [
          {
            name: `${stack}-bas`,
            type: "line" as const,
            stack,
            silent: true,
            symbol: "none",
            lineStyle: { opacity: 0 },
            data: P.map((p, i) => [p, low[i]!]),
            tooltip: { show: false },
          },
          {
            name: `${stack}-haut`,
            type: "line" as const,
            stack,
            silent: true,
            symbol: "none",
            lineStyle: { opacity: 0 },
            areaStyle: { color, opacity: 0.15 },
            data: P.map((p, i) => [p, high[i]! - low[i]!]),
            tooltip: { show: false },
          },
        ];
        const line = (name: string, values: number[], color: string) => ({
          name,
          type: "line" as const,
          symbol: "none",
          lineStyle: { color, width: 2 },
          itemStyle: { color },
          data: P.map((p, i) => [p, values[i]!]),
        });
        const points = (name: string, values: number[], color: string, hollow: boolean) => ({
          name,
          type: "scatter" as const,
          symbolSize: 5,
          itemStyle: hollow ? { color: "transparent", borderColor: color, borderWidth: 1 } : { color },
          data: curve.obs_periods.map((p, i) => [p, values[i]!]),
        });
        chart.setOption(
          {
            animation: false,
            textStyle: { fontFamily: `${cssVar("--font-ui") || "system-ui"}, sans-serif`, color: muted },
            grid: { left: 44, right: 16, top: 16, bottom: 36 },
            tooltip: {
              trigger: "item" as const,
              backgroundColor: cssVar("--paper"),
              borderColor: rule,
              textStyle: { color: ink },
              formatter: (p: unknown) => {
                const q = p as { seriesName: string; value: [number, number] };
                return `${q.seriesName}<br/>période de retour ${nf(q.value[0], q.value[0] < 10 ? 1 : 0)} ans : <b>${nf(q.value[1])} °C</b>`;
              },
            },
            xAxis: {
              type: "log" as const,
              min: xMin,
              max: xMax,
              name: "ans",
              nameLocation: "end" as const,
              nameTextStyle: { color: muted },
              axisLine: { lineStyle: { color: rule } },
              axisLabel: { color: muted },
              splitLine: { lineStyle: { color: rule, type: "dashed" as const } },
            },
            yAxis: {
              type: "value" as const,
              scale: true,
              name: "°C",
              nameTextStyle: { color: muted, align: "right" as const },
              axisLabel: { color: muted },
              splitLine: { lineStyle: { color: rule, type: "dashed" as const } },
            },
            series: [
              ...band(curve.past_low, curve.past_high, cold, "passe"),
              ...band(curve.today_low, curve.today_high, warm, "auj"),
              {
                ...line(pastLabel, curve.past, cold),
                ...(marker
                  ? {
                      markLine: {
                        silent: true,
                        symbol: "none",
                        lineStyle: { color: ink, type: "dashed" as const, width: 1 },
                        label: { formatter: marker.label, color: ink, position: "insideStartTop" as const },
                        data: [{ yAxis: marker.value }],
                      },
                    }
                  : {}),
              },
              line(todayLabel, curve.today, warm),
              points(`Observations ramenées au climat ${pastLabel.toLowerCase().replace(/^climat /, "")}`, curve.obs_past, cold, true),
              points(`Observations ramenées au climat ${todayLabel.toLowerCase().replace(/^climat /, "")}`, curve.obs_today, warm, false),
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
  }, [curve, pastLabel, todayLabel, marker]);

  const legend: { name: string; color: string; kind: "line" | "dot" | "ring" }[] = [
    { name: `${todayLabel} (bande : intervalle à ${ciLabel})`, color: "--warm", kind: "line" },
    { name: `${pastLabel} (bande : intervalle à ${ciLabel})`, color: "--cold", kind: "line" },
    { name: "Années observées, ramenées au climat d'aujourd'hui", color: "--warm", kind: "dot" },
    { name: "Les mêmes, ramenées au climat passé", color: "--cold", kind: "ring" },
  ];
  return (
    <div>
      <div ref={ref} className="h-[320px] w-full sm:h-[400px]" role="img" aria-label={label} />
      <ul className="mt-1 flex flex-wrap gap-x-5 gap-y-1 text-xs text-[var(--muted)]">
        {legend.map((l) => (
          <li key={l.name}>
            {l.kind === "line" ? (
              <i className="mr-1.5 inline-block w-4 align-middle" style={{ borderTop: `2px solid var(${l.color})` }} />
            ) : (
              <i
                className="mr-1.5 inline-block h-2 w-2 rounded-full align-middle"
                style={l.kind === "dot" ? { background: `var(${l.color})` } : { border: `1px solid var(${l.color})` }}
              />
            )}
            {l.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
