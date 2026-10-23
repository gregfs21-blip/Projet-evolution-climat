"use client";

// Toutes les stations d'une variable superposées, composite en couleur : la concordance se voit d'un coup d'œil.
import { useEffect, useMemo, useRef, useState } from "react";

import Segmented from "./Segmented";
import type { Overlay } from "@/lib/family";

export type VarOption = { id: string; code: string; label: string };

function cssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export default function StationsOverlay({
  data,
  variables,
  initial,
  unit,
}: {
  data: Record<string, Overlay>;
  variables: VarOption[];
  initial: string;
  unit: string;
}) {
  const [variable, setVariable] = useState<string>(initial);
  const ref = useRef<HTMLDivElement>(null);
  const current = data[variable];

  // Axe commun : toutes les années présentes dans l'une des séries.
  const years = useMemo(() => {
    if (!current) return [];
    const all = new Set<string>();
    for (const l of [...current.stations, ...(current.composite ? [current.composite] : [])]) l.time.forEach((t) => all.add(t));
    return [...all].sort();
  }, [current]);

  useEffect(() => {
    if (!current) return;
    let disposed = false;
    let cleanup = () => {};
    (async () => {
      const echarts = await import("echarts");
      if (disposed || !ref.current) return;
      const chart = echarts.init(ref.current, undefined, { renderer: "canvas" as const });
      const align = (time: string[], value: (number | null)[]) => {
        const m = new Map(time.map((t, i) => [t, value[i] ?? null]));
        return years.map((y) => m.get(y) ?? null);
      };
      const render = () => {
        const ink = cssVar("--ink");
        const muted = cssVar("--muted");
        const rule = cssVar("--rule");
        const warm = cssVar("--warm");
        const comp = current.composite;
        const raw = comp ? comp.time.filter((_, i) => comp.quality?.[i] === "raw") : [];
        const tr = comp?.trend ?? null;
        chart.setOption(
          {
            animation: false,
            textStyle: { fontFamily: `${cssVar("--font-plex-sans") || "system-ui"}, sans-serif`, color: muted },
            grid: { left: 40, right: 12, top: 16, bottom: 28 },
            tooltip: {
              trigger: "axis" as const,
              backgroundColor: cssVar("--paper"),
              borderColor: rule,
              textStyle: { color: ink, fontSize: 12 },
              valueFormatter: (v: unknown) =>
                typeof v === "number" ? `${v.toLocaleString("fr-FR", { maximumFractionDigits: 2, signDisplay: "always" })} ${unit}` : "—",
            },
            xAxis: {
              type: "category" as const,
              data: years,
              axisLine: { lineStyle: { color: rule } },
              axisTick: { show: false },
              axisLabel: { color: muted },
            },
            yAxis: {
              type: "value" as const,
              axisLabel: { color: muted },
              splitLine: { lineStyle: { color: rule, type: "dashed" as const } },
            },
            series: [
              ...current.stations.map((s) => ({
                name: s.name,
                type: "line" as const,
                showSymbol: false,
                connectNulls: false,
                lineStyle: { color: muted, width: 1, opacity: 0.55 },
                itemStyle: { color: muted },
                emphasis: { disabled: true },
                data: align(s.time, s.value),
              })),
              ...(comp
                ? [
                    {
                      name: comp.name,
                      type: "line" as const,
                      showSymbol: false,
                      z: 4,
                      lineStyle: { color: warm, width: 2.4 },
                      itemStyle: { color: warm },
                      data: align(comp.time, comp.value),
                      markArea: raw.length
                        ? {
                            silent: true,
                            itemStyle: { color: muted, opacity: 0.12 },
                            data: [[{ xAxis: raw[0]! }, { xAxis: raw[raw.length - 1]! }]],
                          }
                        : undefined,
                    },
                  ]
                : []),
              ...(tr
                ? [
                    {
                      name: "Tendance du composite (Sen)",
                      type: "line" as const,
                      showSymbol: false,
                      silent: true,
                      tooltip: { show: false },
                      z: 5,
                      lineStyle: { color: ink, width: 1.6, type: "dashed" as const },
                      data: years.map((t) => {
                        const y = Number(t.slice(0, 4));
                        if (y < tr.start || y > tr.end) return null;
                        return tr.fittedStart + ((y - tr.start) / Math.max(1, tr.end - tr.start)) * (tr.fittedEnd - tr.fittedStart);
                      }),
                    },
                  ]
                : []),
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
  }, [current, years, unit]);

  if (!current) return null;
  return (
    <figure className="space-y-2">
      <div className="flex justify-end">
        <Segmented
          label="Variable"
          value={variable}
          onChange={setVariable}
          options={variables.map((v) => ({ key: v.id, label: v.code, title: v.label, disabled: !data[v.id] }))}
        />
      </div>
      <div ref={ref} className="h-[260px] w-full sm:h-[300px]" role="img" aria-label={`Séries ${variables.find((v) => v.id === variable)?.label ?? variable} de toutes les stations`} />
      <figcaption className="text-xs text-[var(--muted)]">
        {current.references.length
          ? `Écart annuel de chaque station à sa propre moyenne de référence (${current.references.join(" ou ")}), en ${unit}.`
          : `Valeur annuelle de chaque station, en ${unit}.`}{" "}
        Gris :
        les {current.stations.length} stations ; rouge :
        composite ; pointillés : sa tendance ; zone grisée : années non homogénéisées.
      </figcaption>
    </figure>
  );
}
