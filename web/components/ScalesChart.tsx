"use client";

// Courbes de température par échelle, en SVG : écarts annuels (trait fin), droite de Sen publiée (trait épais),
// années non homogénéisées en pointillés. Le site ne calcule ni moyenne mobile ni intervalle : il trace ce que l'ETL publie.
import Link from "next/link";
import { useEffect, useMemo, useRef, useState, type PointerEvent } from "react";

import Segmented from "./Segmented";
import { fmtSigned } from "@/lib/format";
import type { ScaleSeries } from "@/lib/home";

type Props = { series: ScaleSeries[]; first: number; last: number; unit: string; reference: string };
type Pt = { x: number; y: number };

const fmtTick = new Intl.NumberFormat("fr-FR", { signDisplay: "exceptZero", maximumFractionDigits: 1 });

function path(pts: Pt[]): string {
  return pts.map((p, i) => `${i ? "L" : "M"}${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join("");
}

export default function ScalesChart({ series, first, last, unit, reference }: Props) {
  const box = useRef<HTMLDivElement>(null);
  const [w, setW] = useState(960);
  const [range, setRange] = useState<"all" | "1950" | "50" | "30">("1950");
  const [hover, setHover] = useState<number | null>(null);

  useEffect(() => {
    const el = box.current;
    if (!el) return;
    const ro = new ResizeObserver(([e]) => e && setW(Math.max(280, Math.round(e.contentRect.width))));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const start = range === "all" ? first : range === "1950" ? 1950 : last - Number(range) + 1;
  const narrow = w < 560;
  const H = narrow ? 280 : 360;
  const m = { l: 40, r: narrow ? 64 : 138, t: 26, b: 26 };
  const X = (y: number) => m.l + ((y - start) / Math.max(1, last - start)) * (w - m.l - m.r);

  const { lo, hi, ticksY } = useMemo(() => {
    const vals = series.flatMap((s) => s.years.flatMap((y, i) => (y >= start && s.value[i] != null ? [s.value[i]!] : [])));
    const span = Math.max(...vals) - Math.min(...vals);
    const step = span > 3 ? 1 : 0.5;
    const lo = Math.floor(Math.min(0, ...vals) / step) * step;
    const hi = Math.ceil(Math.max(0, ...vals) / step) * step;
    const ticksY: number[] = [];
    for (let v = lo; v <= hi + 1e-9; v += step) ticksY.push(Math.round(v * 10) / 10);
    return { lo, hi, ticksY };
  }, [series, start]);
  const Y = (v: number) => m.t + ((hi - v) / (hi - lo || 1)) * (H - m.t - m.b);

  // Pas des repères d'années : assez large pour que les libellés ne se touchent pas à la largeur disponible.
  const xSpan = last - start;
  const xSlots = Math.max(3, Math.floor((w - m.l - m.r) / 56));
  const xStep = [5, 10, 20, 25, 50].find((st) => xSpan / st <= xSlots) ?? 50;
  const ticksX: number[] = [];
  for (let y = Math.ceil(start / xStep) * xStep; y <= last; y += xStep) ticksX.push(y);

  const lines = series.map((s) => {
    const solid: Pt[][] = [[]];
    const dotted: Pt[][] = [];
    let prev: Pt | null = null;
    s.years.forEach((y, i) => {
      const v = s.value[i];
      if (y < start) return;
      if (v === null || v === undefined) {
        solid.push([]);
        prev = null;
        return;
      }
      const p = { x: X(y), y: Y(v) };
      if (s.raw[i]) dotted.push(prev ? [prev, p] : [p]);
      else solid[solid.length - 1]!.push(p);
      prev = p;
    });
    const t = s.trend;
    let sen: { a: Pt; b: Pt } | null = null;
    if (t && t.end > start) {
      const y0 = Math.max(t.start, start);
      const f = (y: number) => t.fittedStart + ((y - t.start) / Math.max(1, t.end - t.start)) * (t.fittedEnd - t.fittedStart);
      sen = { a: { x: X(y0), y: Y(f(y0)) }, b: { x: X(t.end), y: Y(t.fittedEnd) } };
    }
    return { s, solid, dotted, sen };
  });

  // Étiquettes directes en marge droite, écartées si elles se touchent.
  const labels = lines
    .filter((l) => l.sen)
    .map((l) => ({ s: l.s, y: l.sen!.b.y }))
    .sort((a, b) => a.y - b.y);
  labels.forEach((l, i) => {
    const before = labels[i - 1];
    if (before && l.y - before.y < 18) l.y = before.y + 18;
  });

  const onMove = (e: PointerEvent<SVGSVGElement>) => {
    const r = e.currentTarget.getBoundingClientRect();
    const y = Math.round(start + ((e.clientX - r.left - m.l) / (w - m.l - m.r)) * (last - start));
    setHover(y < start || y > last ? null : y);
  };

  const rows = useMemo(() => {
    const out: number[] = [];
    for (let y = last; y >= start; y--) out.push(y);
    return out;
  }, [last, start]);
  const valueAt = (s: ScaleSeries, y: number) => {
    const i = s.years.indexOf(y);
    return i >= 0 ? { v: s.value[i] ?? null, raw: s.raw[i]! } : { v: null, raw: false };
  };

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <ul className="flex flex-wrap gap-x-4 gap-y-1 text-sm">
          {series.map((s) => (
            <li key={s.key}>
              <Link href={s.href} className="inline-flex items-center gap-1.5 underline-offset-2 hover:underline">
                <i className="inline-block h-2.5 w-2.5 rounded-full" style={{ background: s.color }} />
                {s.name}
              </Link>
            </li>
          ))}
        </ul>
        <Segmented
          label="Période affichée"
          value={range}
          onChange={setRange}
          options={[
            { key: "all", label: "Tout" },
            { key: "1950", label: "Depuis 1950" },
            { key: "50", label: "50 ans" },
            { key: "30", label: "30 ans" },
          ]}
        />
      </div>

      <div ref={box} className="relative">
        <svg
          viewBox={`0 0 ${w} ${H}`}
          width="100%"
          height={H}
          role="img"
          aria-label={`Écart annuel de température à la moyenne ${reference}, par échelle, de ${start} à ${last}`}
          className="touch-pan-y"
          onPointerMove={onMove}
          onPointerDown={onMove}
          onPointerLeave={() => setHover(null)}
        >
          {ticksY.map((v) => (
            <g key={v}>
              <line x1={m.l} x2={w - m.r} y1={Y(v)} y2={Y(v)} style={{ stroke: v === 0 ? "var(--muted)" : "var(--rule)" }} strokeWidth={1} strokeDasharray={v === 0 ? undefined : "2 4"} />
              <text x={m.l - 8} y={Y(v) + 4} textAnchor="end" fontSize={12} style={{ fill: "var(--muted)", fontVariantNumeric: "tabular-nums" }}>
                {fmtTick.format(v)}
              </text>
            </g>
          ))}
          <text x={m.l - 8} y={12} textAnchor="end" fontSize={11} style={{ fill: "var(--muted)" }}>
            {unit}
          </text>
          {ticksX.map((y) => (
            <text key={y} x={X(y)} y={H - 6} textAnchor="middle" fontSize={12} style={{ fill: "var(--muted)", fontVariantNumeric: "tabular-nums" }}>
              {y}
            </text>
          ))}
          {lines.map(({ s, solid, dotted, sen }) => (
            <g key={s.key} fill="none" style={{ stroke: s.color }}>
              {solid.filter((p) => p.length > 1).map((p, i) => (
                <path key={i} d={path(p)} strokeWidth={1.25} opacity={0.7} strokeLinejoin="round" />
              ))}
              {dotted.filter((p) => p.length > 1).map((p, i) => (
                <path key={i} d={path(p)} strokeWidth={1.75} strokeDasharray="1 4" strokeLinecap="round" />
              ))}
              {sen && <line x1={sen.a.x} y1={sen.a.y} x2={sen.b.x} y2={sen.b.y} strokeWidth={2.5} strokeLinecap="round" />}
            </g>
          ))}
          {labels.map(({ s, y }) => (
            <g key={s.key}>
              <circle cx={w - m.r + 9} cy={y - 4} r={3.5} style={{ fill: s.color }} />
              <text x={w - m.r + 16} y={y} fontSize={12} style={{ fill: "var(--ink)", fontVariantNumeric: "tabular-nums" }}>
                {narrow ? s.name : `${s.name} ${s.trend ? `${fmtSigned(s.trend.slope)}/déc.` : ""}`}
              </text>
            </g>
          ))}
          {hover !== null && (
            <g>
              <line x1={X(hover)} x2={X(hover)} y1={m.t} y2={H - m.b} style={{ stroke: "var(--muted)" }} strokeWidth={1} />
              {series.map((s) => {
                const { v } = valueAt(s, hover);
                return v === null ? null : <circle key={s.key} cx={X(hover)} cy={Y(v)} r={4} style={{ fill: s.color, stroke: "var(--card)" }} strokeWidth={2} />;
              })}
            </g>
          )}
        </svg>
        {hover !== null && (
          <div
            className="card pointer-events-none absolute top-2 z-10 min-w-40 px-3 py-2 text-sm"
            style={X(hover) > w / 2 ? { right: w - X(hover) + 12 } : { left: X(hover) + 12 }}
          >
            <div className="font-semibold tabular-nums">{hover}</div>
            {series.map((s) => {
              const { v, raw } = valueAt(s, hover);
              return (
                <div key={s.key} className="flex items-center justify-between gap-4 tabular-nums">
                  <span className="inline-flex items-center gap-1.5 text-[var(--muted)]">
                    <i className="inline-block h-2 w-2 rounded-full" style={{ background: s.color }} />
                    {s.name}
                  </span>
                  <span>
                    {v === null ? <span className="text-[var(--muted)]">pas de valeur</span> : `${fmtSigned(v)} ${unit}`}
                    {raw && <span className="ml-1 text-xs text-[var(--muted)]">brut</span>}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <p className="text-xs text-[var(--muted)]">
        Trait fin : écart annuel à la moyenne {reference}. Trait épais : droite de Sen, sur la période propre à chaque série. Pointillés : années non
        homogénéisées, hors tendance. Le chiffre mondial inclut les océans, qui se réchauffent moins vite que les terres : l&apos;écart avec la Gironde
        ou la France n&apos;est pas un effet purement local.
      </p>

      <details className="text-sm">
        <summary className="cursor-pointer select-none text-[var(--muted)]">
          <span className="chevron mr-1">▸</span>Voir les valeurs en tableau
        </summary>
        <div className="mt-2 max-h-64 overflow-auto rounded-lg border border-[var(--rule)]">
          <table className="w-full text-right tabular-nums">
            <thead className="sticky top-0 bg-[var(--card)] text-[var(--muted)]">
              <tr>
                <th className="px-3 py-1.5 text-left font-medium">Année</th>
                {series.map((s) => (
                  <th key={s.key} className="px-3 py-1.5 font-medium">
                    {s.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((y) => (
                <tr key={y} className="border-t border-[var(--rule)]">
                  <td className="px-3 py-1 text-left">{y}</td>
                  {series.map((s) => {
                    const { v, raw } = valueAt(s, y);
                    return (
                      <td key={s.key} className="px-3 py-1">
                        {v === null ? "" : fmtSigned(v)}
                        {raw && <span className="ml-1 text-xs text-[var(--muted)]">brut</span>}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </div>
  );
}
