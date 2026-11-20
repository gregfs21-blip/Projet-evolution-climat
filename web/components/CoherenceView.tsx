"use client";

// Contrôles de cohérence physique (P10.4). Tous les chiffres viennent de data/processed/demonstration.json ;
// la page ne fait que les mettre en forme.
import { useState } from "react";

import LinesChart from "./LinesChart";
import type { Coherence, CoherenceCheck, CoherenceValue } from "@/lib/schema";

const nf = (v: number, d: number, sign = false) =>
  v.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d, signDisplay: sign ? "exceptZero" : "auto" });

// Une décimale de plus que l'unité ne l'exige pour les petites tendances (°C/décennie, W/m²/décennie).
function digits(unit: string): number {
  if (unit.startsWith("°C")) return 3;
  if (unit.startsWith("W/m²")) return 2;
  if (unit === "%" || unit.startsWith("% ")) return 1;
  return 2;
}

function Val({ v }: { v: CoherenceValue }) {
  const d = digits(v.unit);
  const e = v.estimate;
  const sign = v.unit.includes("par") || v.unit.endsWith("/an");
  return (
    <tr className="border-t border-[var(--rule)] align-top">
      <td className="py-1.5 pr-3">{v.label}</td>
      <td className="py-1.5 pr-3 text-xs whitespace-nowrap text-[var(--muted)]">
        {v.period.start}-{v.period.end}
      </td>
      <td className="py-1.5 text-right whitespace-nowrap tabular-nums">
        <b>{nf(e.value, d, sign)}</b>
        {e.ci_low !== null && e.ci_high !== null && (
          <span className="text-xs text-[var(--muted)]">
            {" "}
            [{nf(e.ci_low, d, sign)} ; {nf(e.ci_high, d, sign)}]
          </span>
        )}{" "}
        <span className="text-xs text-[var(--muted)]">{v.unit}</span>
      </td>
    </tr>
  );
}

const COLORS = ["--warm", "--accent", "--cold", "--forest"];

function Check({ c }: { c: CoherenceCheck }) {
  return (
    <div className="space-y-5">
      <div className="max-w-3xl space-y-2">
        <p className="text-[var(--muted)] italic">{c.question}</p>
        <p className="leading-relaxed">
          <span className={c.satisfied ? "text-[var(--good)]" : "text-[var(--warm)]"}>{c.satisfied ? "✓" : "✗"}</span> {c.result}{" "}
          <span className="text-xs text-[var(--muted)]">(critère {c.criterion})</span>
        </p>
      </div>
      {c.charts.map((ch) => (
        <figure key={ch.title} className="space-y-2">
          <figcaption className="text-sm font-semibold">{ch.title}</figcaption>
          <LinesChart
            years={ch.years}
            unit={ch.unit}
            label={ch.title}
            height="h-[300px] sm:h-[360px]"
            lines={ch.lines.map((l, i) => ({
              name: l.name,
              values: l.values,
              color: COLORS[i % COLORS.length] ?? "--ink",
              width: i === 0 ? 2 : 1.4,
              dashed: c.id === "niveau-marin" && i >= 2,
              opacity: c.id === "niveau-marin" && i >= 2 ? 0.7 : 1,
            }))}
          />
          <p className="text-xs leading-relaxed text-[var(--muted)]">{ch.note}</p>
        </figure>
      ))}
      <div className="grid max-w-5xl gap-6 lg:grid-cols-2">
        <table className="w-full text-sm">
          <caption className="pb-1 text-left text-xs font-semibold text-[var(--muted)]">Résultat (intervalle à 95 %)</caption>
          <tbody>
            {c.values.map((v) => (
              <Val key={v.label} v={v} />
            ))}
          </tbody>
        </table>
        {c.information.length > 0 && (
          <table className="w-full text-sm">
            <caption className="pb-1 text-left text-xs font-semibold text-[var(--muted)]">Pour information</caption>
            <tbody>
              {c.information.map((v) => (
                <Val key={v.label} v={v} />
              ))}
            </tbody>
          </table>
        )}
      </div>
      <div className="max-w-3xl space-y-1 text-xs leading-relaxed text-[var(--muted)]">
        <p>Référence : {c.reference}</p>
        <p>Limite : {c.limitation}</p>
      </div>
    </div>
  );
}

export default function CoherenceView({ a }: { a: Coherence }) {
  const [id, setId] = useState<string>(a.checks[0]?.id ?? "");
  const c = a.checks.find((x) => x.id === id) ?? a.checks[0];
  if (!c) return null;
  return (
    <div className="space-y-6">
      <div className="grid max-w-5xl gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {a.checks.map((x) => (
          <button
            key={x.id}
            type="button"
            onClick={() => setId(x.id)}
            aria-pressed={x.id === c.id}
            className={`rounded-lg border px-3 py-2 text-left text-sm ${x.id === c.id ? "border-[var(--ink)]" : "border-[var(--rule)]"}`}
          >
            <span className={x.satisfied ? "text-[var(--good)]" : "text-[var(--warm)]"}>{x.satisfied ? "✓" : "✗"}</span>{" "}
            <span className="font-medium">
              {x.letter} · {x.title}
            </span>
          </button>
        ))}
      </div>
      <Check c={c} />
    </div>
  );
}
