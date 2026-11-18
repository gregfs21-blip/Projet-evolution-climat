"use client";

// Résultats de la régression multiple (P10.1), jeu de températures au choix. Tous les chiffres viennent de
// data/processed/demonstration.json ; seul le total des contributions affiché est une somme de séries publiées.
import { useMemo, useState } from "react";

import LinesChart, { type Line } from "./LinesChart";
import Segmented from "./Segmented";
import type { Estimate, Regression, RegressionDataset } from "@/lib/schema";

const nf = (v: number, d = 2, sign = false) =>
  v.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d, signDisplay: sign ? "always" : "auto" });
const ci = (e: Estimate, d = 2) => (e.ci_low !== null && e.ci_high !== null ? `[${nf(e.ci_low, d)} ; ${nf(e.ci_high, d)}]` : "");
const pv = (p: number) => (p < 0.001 ? "< 0,001" : nf(p, 3));

function Figure({ title, children, note }: { title: string; children: React.ReactNode; note?: React.ReactNode }) {
  return (
    <figure className="space-y-2">
      <figcaption className="text-sm font-semibold">{title}</figcaption>
      {children}
      {note && <p className="text-xs leading-relaxed text-[var(--muted)]">{note}</p>}
    </figure>
  );
}

function Charts({ d }: { d: RegressionDataset }) {
  const s = d.series;
  const model = useMemo(
    () => s.years.map((_, i) => s.anthropogenic[i]! + s.volcanic[i]! + s.solar[i]! + s.enso[i]!),
    [s],
  );
  const natural = useMemo(() => s.years.map((_, i) => s.volcanic[i]! + s.solar[i]!), [s]);
  const decomposition: Line[] = useMemo(
    () => [
      { name: "Observé", values: s.observed_rebased, color: "--ink", width: 1, opacity: 0.45 },
      { name: "Modèle (somme des contributions)", values: model, color: "--accent", width: 2 },
      { name: "Contribution humaine", values: s.anthropogenic, color: "--warm", width: 2 },
      { name: "Volcans + soleil", values: natural, color: "--cold", width: 1.5 },
      { name: "El Niño / La Niña", values: s.enso, color: "--muted", width: 1, dashed: true },
    ],
    [s, model, natural],
  );
  const to = d.trend_observed;
  const ta = d.trend_adjusted;
  const so = d.slope_observed;
  const sa = d.slope_adjusted;
  const adjusted: Line[] = useMemo(
    () => [
      { name: "Observé", values: s.observed, color: "--muted", width: 1.2 },
      { name: "Ajusté (sans ENSO, volcans, soleil)", values: s.adjusted, color: "--warm", width: 2 },
      {
        name: `Pente ajustée ${to.period.start}-${to.period.end} (Sen)`,
        values: [],
        color: "--accent",
        width: 2,
        dashed: true,
        sen: { start: ta.period.start, end: ta.period.end, fittedStart: ta.fitted_start, fittedEnd: ta.fitted_end },
      },
    ],
    [s, to.period.start, to.period.end, ta],
  );
  return (
    <div className="space-y-8">
      <Figure
        title="Ce que le modèle reconstruit, année par année"
        note={
          <>
            Écarts au niveau {d.attributions[0]!.baseline.start}-{d.attributions[0]!.baseline.end} estimé par le modèle. La courbe du modèle est la somme des quatre contributions ; l&apos;écart
            avec l&apos;observé est le résidu (écart type {nf(d.residual_sd, 2)} °C, autocorrélation ρ = {nf(d.rho, 2)}). Part de la
            variance expliquée : {nf(d.r2 * 100, 0)} %.
          </>
        }
      >
        <LinesChart years={s.years} lines={decomposition} unit="°C" label={`Décomposition de la température mondiale (${d.label})`} />
      </Figure>
      <Figure
        title="La température une fois les facteurs naturels retirés"
        note={
          <>
            Pente de Sen {to.period.start}-{to.period.end} : observée {nf(so.value, 3)} °C par décennie {ci(so, 3)}, ajustée{" "}
            {nf(sa.value, 3)} {ci(sa, 3)}. Intervalles de Sen non corrigés de l&apos;autocorrélation ; l&apos;incertitude des
            contributions retirées n&apos;est pas propagée. Écarts dans la référence de {d.label}.
          </>
        }
      >
        <LinesChart years={s.years} lines={adjusted} unit="°C" label={`Température observée et ajustée (${d.label})`} height="h-[280px] sm:h-[340px]" />
      </Figure>
    </div>
  );
}

function Attributions({ d }: { d: RegressionDataset }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[34rem] text-left text-sm">
        <thead className="text-xs text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-1.5 pr-3 font-medium">
              Par rapport à {d.attributions[0]!.baseline.start}-{d.attributions[0]!.baseline.end}
            </th>
            <th className="py-1.5 pr-3 font-medium">Part humaine (ce calcul)</th>
            <th className="py-1.5 pr-3 font-medium">Part humaine (IGCC 2025)</th>
            <th className="py-1.5 pr-3 font-medium">Volcans + soleil</th>
            <th className="py-1.5 font-medium">Observé</th>
          </tr>
        </thead>
        <tbody>
          {d.attributions.map((a) => {
            const r = a.reference_anthropogenic;
            const inside = r.ci_low !== null && r.ci_high !== null && a.anthropogenic.value >= r.ci_low && a.anthropogenic.value <= r.ci_high;
            return (
              <tr key={a.window.start} className="border-b border-[var(--rule)] align-top">
                <td className="py-1.5 pr-3 font-medium">
                  {a.window.start}-{a.window.end}
                </td>
                <td className="py-1.5 pr-3">
                  <b>{nf(a.anthropogenic.value)} °C</b> <span className="text-xs text-[var(--muted)]">{ci(a.anthropogenic)}</span>{" "}
                  <span className={inside ? "text-[var(--good)]" : "text-[var(--warm)]"}>{inside ? "✓" : "✗"}</span>
                </td>
                <td className="py-1.5 pr-3">
                  {nf(r.value)} °C <span className="text-xs text-[var(--muted)]">{ci(r, 1)}</span>
                </td>
                <td className="py-1.5 pr-3">
                  {nf(a.natural.value, 2, true)} °C <span className="text-xs text-[var(--muted)]">{ci(a.natural)}</span>
                </td>
                <td className="py-1.5">{a.observed === null ? <span className="text-[var(--muted)]">période non couverte</span> : `${nf(a.observed)} °C`}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <p className="mt-1 text-xs text-[var(--muted)]">{d.attributions[0]?.reference_source}</p>
    </div>
  );
}

function Coefficients({ d, tcrRef }: { d: RegressionDataset; tcrRef: Estimate }) {
  const ols = new Map(d.coefficients_ols.map((c) => [c.name, c]));
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[36rem] text-left text-sm">
        <thead className="text-xs text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-1.5 pr-3 font-medium">Terme</th>
            <th className="py-1.5 pr-3 font-medium">Coefficient [IC 95 %]</th>
            <th className="py-1.5 pr-3 font-medium">p</th>
            <th className="py-1.5 font-medium">Contrôle MCO + Newey-West</th>
          </tr>
        </thead>
        <tbody>
          {d.coefficients
            .filter((c) => c.name !== "constante")
            .map((c) => {
              const o = ols.get(c.name);
              return (
                <tr key={c.name} className="border-b border-[var(--rule)] align-top">
                  <td className="py-1.5 pr-3">
                    {c.label}
                    <div className="text-xs text-[var(--muted)]">{c.unit}</div>
                  </td>
                  <td className="py-1.5 pr-3">
                    <b>{nf(c.value, 3)}</b> <span className="text-xs text-[var(--muted)]">[{nf(c.ci_low, 3)} ; {nf(c.ci_high, 3)}]</span>
                  </td>
                  <td className="py-1.5 pr-3">{pv(c.p_value)}</td>
                  <td className="py-1.5 text-xs text-[var(--muted)]">
                    {o ? `${nf(o.value, 3)} [${nf(o.ci_low, 3)} ; ${nf(o.ci_high, 3)}], p ${pv(o.p_value)}` : "—"}
                  </td>
                </tr>
              );
            })}
        </tbody>
      </table>
      <p className="mt-1 text-xs text-[var(--muted)]">
        {d.method}, {d.period.start}-{d.period.end} (n = {d.n}). Réponse transitoire implicite : <b>{nf(d.tcr.value)} °C</b> {ci(d.tcr)}{" "}
        (GIEC AR6 : {nf(tcrRef.value, 1)} °C, très probablement {tcrRef.ci_low !== null && nf(tcrRef.ci_low, 1)} à{" "}
        {tcrRef.ci_high !== null && nf(tcrRef.ci_high, 1)}). Facteurs d&apos;inflation de la variance :{" "}
        {Object.entries(d.vif)
          .map(([k, v]) => `${k} ${nf(v)}`)
          .join(", ")}{" "}
        (proches de 1 : les termes ne se confondent pas).
      </p>
    </div>
  );
}

const GROUPS: Record<string, string> = {
  decalages: "Décalages",
  forcage: "Incertitude du forçage",
  "sous-periode": "Sous-période",
};

function Robustness({ d }: { d: RegressionDataset }) {
  const control = d.attributions[d.attributions.length - 1]!;
  const ref = control.reference_anthropogenic;
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[36rem] text-left text-sm">
        <thead className="text-xs text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-1.5 pr-3 font-medium">Variante</th>
            <th className="py-1.5 pr-3 font-medium">
              Part humaine {control.window.start}-{control.window.end}
            </th>
            <th className="py-1.5 pr-3 font-medium">Réponse transitoire</th>
            <th className="py-1.5 pr-3 font-medium">ρ</th>
            <th className="py-1.5 font-medium">R²</th>
          </tr>
        </thead>
        <tbody>
          {d.robustness.map((c) => (
            <tr key={c.label} className="border-b border-[var(--rule)] align-top">
              <td className="py-1.5 pr-3">
                <span className="text-xs text-[var(--muted)]">{GROUPS[c.group]} · </span>
                {c.label}
              </td>
              <td className="py-1.5 pr-3">
                {nf(c.attributable)} °C{" "}
                <span className={c.in_range ? "text-[var(--good)]" : "text-[var(--warm)]"}>{c.in_range ? "✓" : "✗"}</span>
              </td>
              <td className="py-1.5 pr-3">{nf(c.tcr)} °C</td>
              <td className="py-1.5 pr-3">{nf(c.rho)}</td>
              <td className="py-1.5">{nf(c.r2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-1 text-xs text-[var(--muted)]">
        ✓ : réchauffement attribué {control.window.start}-{control.window.end} dans la fourchette de l&apos;IGCC 2025 {ci(ref, 1)} °C ;
        pour la sous-période, l&apos;intervalle de βₐ doit aussi recouper celui de la période complète (critère O8). Un ρ proche de 1 et
        un R² faible signalent une variante qui n&apos;arrive plus à reproduire les observations (un R² négatif fait pire
        qu&apos;une constante).
      </p>
    </div>
  );
}

export default function RegressionView({ reg }: { reg: Regression }) {
  const [id, setId] = useState(reg.datasets[0]!.id);
  const d = reg.datasets.find((x) => x.id === id) ?? reg.datasets[0]!;
  return (
    <div className="space-y-8">
      <Segmented label="Jeu de températures" value={id} onChange={setId} options={reg.datasets.map((x) => ({ key: x.id, label: x.label }))} />
      <Charts d={d} />
      <section className="space-y-2">
        <h3 className="text-lg font-semibold">Combien de réchauffement d&apos;origine humaine ?</h3>
        <Attributions d={d} />
      </section>
      <section className="space-y-2">
        <h3 className="text-lg font-semibold">Les coefficients</h3>
        <Coefficients d={d} tcrRef={reg.tcr_reference} />
      </section>
      <section className="space-y-2">
        <h3 className="text-lg font-semibold">Le résultat tient-il si l&apos;on change les choix ?</h3>
        <Robustness d={d} />
      </section>
    </div>
  );
}
