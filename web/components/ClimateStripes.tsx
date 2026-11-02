"use client";

// Bandes climatiques : une ligne par échelle, une bande par année, même référence et même échelle de couleur.
// Posées sur le fond sombre du bandeau d'accueil, quel que soit le thème. Lecture d'une année au survol,
// au doigt ou au curseur (clavier). Aucune valeur calculée ici.
import Link from "next/link";
import { useState, type PointerEvent } from "react";

import { fmtSigned } from "@/lib/format";
import { ANOMALY_MAX, anomalyColor, anomalyGradient } from "@/lib/heat";
import type { ScaleSeries } from "@/lib/home";

type Props = { series: ScaleSeries[]; first: number; last: number; unit: string; reference: string };

const LABEL_MIN_SPAN = 30; // années : en dessous, le trou est trop étroit pour porter un texte

function Row({ s, first, last }: { s: ScaleSeries; first: number; last: number }) {
  const n = last - first + 1;
  const s0 = s.years[0]!;
  const s1 = s.years[s.years.length - 1]!;
  const lead = s0 - first;
  const trail = last - s1;
  return (
    <div className="grid h-full" style={{ gridTemplateColumns: `repeat(${n}, minmax(0, 1fr))` }}>
      {lead > 0 && (
        <div style={{ gridColumn: `span ${lead}` }} className="flex items-center overflow-hidden whitespace-nowrap pl-2 text-xs text-white/60">
          {lead >= LABEL_MIN_SPAN && `pas de série avant ${s0}`}
        </div>
      )}
      {s.years.map((y, i) => {
        const v = s.value[i];
        if (v === null || v === undefined) return <div key={y} />;
        const c = anomalyColor(v);
        // Année non homogénéisée (règle C2) : bande interrompue, pour qu'elle ne se confonde pas avec les autres.
        const style = s.raw[i] ? { background: `repeating-linear-gradient(0deg, ${c} 0 4px, transparent 4px 8px)` } : { background: c };
        return <div key={y} style={style} />;
      })}
      {trail > 0 && <div style={{ gridColumn: `span ${trail}` }} />}
    </div>
  );
}

export default function ClimateStripes({ series, first, last, unit, reference }: Props) {
  // Année affichée au départ : la dernière pour laquelle toutes les échelles ont une valeur.
  const common = Math.min(...series.map((s) => s.years[s.years.length - 1]!));
  const [year, setYear] = useState(common);
  const n = last - first + 1;
  const pos = ((year - first + 0.5) / n) * 100;
  const ticks = [1850, 1900, 1950, 2000].filter((t) => t >= first && t <= last - 10).concat(last);
  const lastK = ticks.length - 1;

  const pick = (e: PointerEvent<HTMLDivElement>) => {
    const r = e.currentTarget.getBoundingClientRect();
    setYear(first + Math.max(0, Math.min(n - 1, Math.floor(((e.clientX - r.left) / r.width) * n))));
  };

  return (
    <figure className="space-y-2">
      <div className="hidden grid-cols-[4.5rem_minmax(0,1fr)_6rem] items-baseline gap-x-3 sm:grid">
        <span />
        <figcaption className="text-sm text-white/75">
          Chaque bande est une année : écart de température à la moyenne {reference}, même couleur pour le même écart.
        </figcaption>
        <span className="text-right text-sm font-semibold tabular-nums text-white">{year}</span>
      </div>
      <figcaption className="text-sm text-white/75 sm:hidden">
        Chaque bande est une année : écart de température à la moyenne {reference}.
      </figcaption>
      <div className="flex items-baseline justify-between sm:hidden">
        <span className="text-xs text-white/75">Année lue</span>
        <span className="text-sm font-semibold tabular-nums text-white">{year}</span>
      </div>

      <div className="space-y-1.5">
        {series.map((s) => {
          const i = s.years.indexOf(year);
          const v = i >= 0 ? s.value[i] : null;
          const raw = i >= 0 && s.raw[i];
          return (
            <div key={s.key} className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-x-3 gap-y-1 sm:grid-cols-[4.5rem_minmax(0,1fr)_6rem]">
              <Link href={s.href} className="text-sm font-medium text-white underline-offset-2 hover:underline">
                {s.name}
              </Link>
              <div
                className="relative order-3 col-span-2 h-11 touch-pan-y overflow-hidden rounded-md bg-white/5 sm:order-none sm:col-span-1 sm:h-14"
                onPointerMove={pick}
                onPointerDown={pick}
              >
                <Row s={s} first={first} last={last} />
                <div className="pointer-events-none absolute inset-y-0 w-px bg-white shadow-[0_0_0_1px_rgb(0_0_0_/_0.35)]" style={{ left: `${pos}%` }} />
              </div>
              <span className="text-right text-sm tabular-nums text-white">
                {v === null || v === undefined ? <span className="text-white/60">pas de valeur</span> : `${fmtSigned(v)} ${unit}`}
                {raw && <span className="ml-1 text-xs text-white/70">brut</span>}
              </span>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 gap-x-3 sm:grid-cols-[4.5rem_minmax(0,1fr)_6rem]">
        <span className="hidden sm:block" />
        <div>
          <input
            type="range"
            min={first}
            max={last}
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            aria-label="Année lue sur les bandes"
            className="year-range block"
          />
          <div className="relative h-4 text-xs tabular-nums text-white/75" aria-hidden>
            {ticks.map((t, k) => (
              <span
                key={t}
                // Sur mobile, l'avant-dernier repère toucherait le dernier : il est masqué.
                className={`absolute ${k === lastK - 1 ? "hidden sm:inline" : ""}`}
                style={{ left: `${((t - first + 0.5) / n) * 100}%`, transform: k === lastK ? "translateX(-100%)" : k === 0 ? "none" : "translateX(-50%)" }}
              >
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-x-5 gap-y-1 pt-1 text-xs text-white/75 sm:pl-[5.25rem]">
        <span className="flex items-center gap-2 tabular-nums">
          −{ANOMALY_MAX} {unit}
          <i className="inline-block h-2.5 w-28 rounded-sm" style={{ background: anomalyGradient() }} />+{ANOMALY_MAX} {unit}
        </span>
        <span className="flex items-center gap-2">
          <i className="inline-block h-3 w-3 rounded-sm" style={{ background: `repeating-linear-gradient(0deg, ${anomalyColor(1.5)} 0 2px, transparent 2px 4px)` }} />
          bande interrompue : année non homogénéisée, hors tendance
        </span>
      </div>
    </figure>
  );
}
