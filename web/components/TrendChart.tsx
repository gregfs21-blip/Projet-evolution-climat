"use client";

// Courbe générique : ne connaît rien du climat, affiche ce qu'on lui donne.
// - anomalies : barres bleues/rouges autour de zéro ;
// - valeurs absolues : ligne ;
// - droite de Sen en pointillés si une tendance est fournie ;
// - points non homogénéisés en gris : affichés pour information, jamais utilisés pour la tendance ;
// - série de comparaison optionnelle (ex. composite départemental) en trait fin ;
// - zoom à la molette et réglette en bas (séries longues). Pas de zoom au doigt sur écran tactile :
//   le glissé doit faire défiler la page, pas le graphique.
import { useEffect, useRef } from "react";

type Props = {
  time: string[];
  value: (number | null)[];
  unit: string;
  isAnomaly: boolean;
  trend: { start: number; end: number; fittedStart: number; fittedEnd: number } | null;
  breakpoints: string[];
  quality?: ("homogenized" | "raw")[] | null;
  /** Série de comparaison, alignée sur `time`. */
  overlay?: { name: string; value: (number | null)[] } | null;
};

function cssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export default function TrendChart({ time, value, unit, isAnomaly, trend, breakpoints, quality, overlay }: Props) {
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
        const accent = cssVar("--accent");
        // Tracé de la droite de Sen entre ses deux extrémités publiées par l'ETL.
        const tr = trend;
        const trendLine = tr
          ? time.map((t) => {
              const year = Number(t.slice(0, 4));
              if (year < tr.start || year > tr.end) return null;
              const k = (year - tr.start) / Math.max(1, tr.end - tr.start);
              return tr.fittedStart + k * (tr.fittedEnd - tr.fittedStart);
            })
          : null;

        chart.setOption(
          {
            animation: false,
            textStyle: { fontFamily: `${cssVar("--font-plex-sans") || "system-ui"}, sans-serif`, color: muted },
            grid: { left: 48, right: 16, top: 24, bottom: 72 },
            tooltip: {
              trigger: "axis" as const,
              backgroundColor: cssVar("--paper"),
              borderColor: rule,
              textStyle: { color: ink },
              formatter: (items: unknown) => {
                const list = (Array.isArray(items) ? items : [items]) as { dataIndex: number; seriesName: string; value: unknown }[];
                const first = list[0];
                if (!first) return "";
                const i = first.dataIndex;
                const fmt = (v: unknown) =>
                  typeof v === "number"
                    ? `${v.toLocaleString("fr-FR", { maximumFractionDigits: 2, signDisplay: isAnomaly ? "always" : "auto" })} ${unit}`
                    : "lacune";
                const raw = quality?.[i] === "raw" ? " <em>(non homogénéisé)</em>" : "";
                const rows = list
                  .filter((it) => it.value !== null && it.value !== undefined)
                  .map((it) => {
                    const v = typeof it.value === "object" && it.value !== null ? (it.value as { value: unknown }).value : it.value;
                    return `${it.seriesName} : <b>${fmt(v)}</b>`;
                  });
                return `<b>${time[i]}</b>${raw}<br/>${rows.join("<br/>")}`;
              },
            },
            xAxis: {
              type: "category" as const,
              data: time,
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
              { type: "slider" as const, height: 22, bottom: 16, borderColor: rule, textStyle: { color: muted } },
            ],
            series: [
              isAnomaly
                ? {
                    name: "Anomalie",
                    type: "bar" as const,
                    barCategoryGap: "15%",
                    data: value.map((v, i) =>
                      v === null
                        ? null
                        : {
                            value: v,
                            itemStyle:
                              quality?.[i] === "raw"
                                ? { color: muted, opacity: 0.45 }
                                : { color: v >= 0 ? warm : cold },
                          },
                    ),
                    markLine: {
                      silent: true,
                      symbol: "none" as const,
                      lineStyle: { color: muted, type: "dashed" as const, width: 1 },
                      label: { color: muted, formatter: "rupture" },
                      data: breakpoints.map((b) => ({ xAxis: b })),
                    },
                  }
                : {
                    name: "Valeur",
                    type: "line" as const,
                    showSymbol: false,
                    connectNulls: false,
                    lineStyle: { color: ink, width: 1.5 },
                    itemStyle: { color: ink },
                    data: value,
                    // Années non homogénéisées : zone grisée, comme les barres grises du mode anomalie.
                    markArea: (() => {
                      const raw = time.filter((_, i) => quality?.[i] === "raw");
                      return raw.length
                        ? { silent: true, itemStyle: { color: muted, opacity: 0.12 }, data: [[{ xAxis: raw[0]! }, { xAxis: raw[raw.length - 1]! }]] }
                        : undefined;
                    })(),
                  },
              ...(overlay
                ? [
                    {
                      name: overlay.name,
                      type: "line" as const,
                      showSymbol: false,
                      connectNulls: false,
                      z: 3,
                      lineStyle: { color: ink, width: 1.5, opacity: 0.55 },
                      itemStyle: { color: ink },
                      data: overlay.value,
                    },
                  ]
                : []),
              ...(trendLine
                ? [
                    {
                      name: "Tendance (Sen)",
                      type: "line" as const,
                      showSymbol: false,
                      silent: true,
                      tooltip: { show: false },
                      lineStyle: { color: accent, width: 2, type: "dashed" as const },
                      data: trendLine,
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
  }, [time, value, unit, isAnomaly, trend, breakpoints, quality, overlay]);

  return <div ref={ref} className="h-[360px] w-full sm:h-[420px]" role="img" aria-label="Graphique de la série" />;
}
