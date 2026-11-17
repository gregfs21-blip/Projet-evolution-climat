"use client";

// Courbes annuelles superposées (onglet Démonstration). Générique : affiche les séries qu'on lui donne,
// avec leur couleur (variable CSS du thème), leur épaisseur et leur style. Aucune valeur n'est recalculée ici,
// sauf le tracé d'une droite de Sen entre ses deux extrémités publiées par l'ETL.
import { useEffect, useRef } from "react";

export type Line = {
  name: string;
  values: (number | null)[];
  color: string; // nom de variable CSS, ex. "--warm"
  width?: number;
  dashed?: boolean;
  opacity?: number;
  /** Droite de Sen : tracée entre start et end. */
  sen?: { start: number; end: number; fittedStart: number; fittedEnd: number };
};

function cssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export default function LinesChart({
  years,
  lines,
  unit,
  label,
  height = "h-[320px] sm:h-[400px]",
}: {
  years: number[];
  lines: Line[];
  unit: string;
  label: string;
  height?: string;
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
        const series = lines.map((l) => {
          const data = l.sen
            ? years.map((y) => {
                const s = l.sen!;
                if (y < s.start || y > s.end) return null;
                return s.fittedStart + ((y - s.start) / Math.max(1, s.end - s.start)) * (s.fittedEnd - s.fittedStart);
              })
            : l.values;
          return {
            name: l.name,
            type: "line" as const,
            showSymbol: false,
            connectNulls: false,
            silent: Boolean(l.sen),
            lineStyle: { color: cssVar(l.color), width: l.width ?? 1.5, type: l.dashed ? ("dashed" as const) : ("solid" as const), opacity: l.opacity ?? 1 },
            itemStyle: { color: cssVar(l.color) },
            data,
          };
        });
        chart.setOption(
          {
            animation: false,
            textStyle: { fontFamily: `${cssVar("--font-ui") || "system-ui"}, sans-serif`, color: muted },
            grid: { left: 44, right: 12, top: 16, bottom: 60 },
            tooltip: {
              trigger: "axis" as const,
              backgroundColor: cssVar("--paper"),
              borderColor: rule,
              textStyle: { color: ink },
              valueFormatter: (v: unknown) =>
                typeof v === "number" ? `${v.toLocaleString("fr-FR", { maximumFractionDigits: 2, signDisplay: "always" })} ${unit}` : "—",
            },
            xAxis: {
              type: "category" as const,
              data: years.map(String),
              axisLine: { lineStyle: { color: rule } },
              axisTick: { show: false },
              axisLabel: { color: muted },
            },
            yAxis: {
              type: "value" as const,
              name: unit,
              nameTextStyle: { color: muted, align: "right" as const },
              axisLabel: { color: muted },
              splitLine: { lineStyle: { color: rule, type: "dashed" as const } },
            },
            dataZoom: [
              ...(window.matchMedia("(pointer: coarse)").matches ? [] : [{ type: "inside" as const }]),
              { type: "slider" as const, height: 20, bottom: 10, borderColor: rule, textStyle: { color: muted } },
            ],
            series,
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
  }, [years, lines, unit]);

  return (
    <div>
      <div ref={ref} className={`${height} w-full`} role="img" aria-label={label} />
      <ul className="mt-1 flex flex-wrap gap-x-5 gap-y-1 text-xs text-[var(--muted)]">
        {lines.map((l) => (
          <li key={l.name}>
            <i
              className="mr-1.5 inline-block w-4 align-middle"
              style={{
                borderTop: `${Math.max(2, l.width ?? 1.5)}px ${l.dashed ? "dashed" : "solid"} var(${l.color})`,
                opacity: l.opacity ?? 1,
              }}
            />
            {l.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
