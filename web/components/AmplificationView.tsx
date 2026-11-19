"use client";

// Résultats de l'amplification régionale (P10.3). Tous les chiffres viennent de data/processed/demonstration.json ;
// la page ne fait que les mettre en forme.
import { Fragment, useState } from "react";

import LinesChart from "./LinesChart";
import ScatterFitChart from "./ScatterFitChart";
import Segmented from "./Segmented";
import type { Amplification, AmplificationFit, AmplificationScale, Estimate } from "@/lib/schema";

const nf = (v: number, d = 2, sign = false) =>
  v.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d, signDisplay: sign ? "always" : "auto" });
const ci = (e: Estimate, d = 2) => (e.ci_low !== null && e.ci_high !== null ? `[${nf(e.ci_low, d)} ; ${nf(e.ci_high, d)}]` : "");
const per = (f: AmplificationFit) => `${f.period.start}-${f.period.end}`;

function K({ e }: { e: Estimate }) {
  return (
    <>
      <b>{nf(e.value)}</b> <span className="text-xs text-[var(--muted)]">{ci(e)}</span>
    </>
  );
}

function Figure({ title, children, note }: { title: string; children: React.ReactNode; note?: React.ReactNode }) {
  return (
    <figure className="space-y-2">
      <figcaption className="text-sm font-semibold">{title}</figcaption>
      {children}
      {note && <p className="text-xs leading-relaxed text-[var(--muted)]">{note}</p>}
    </figure>
  );
}

function Charts({ s, a }: { s: AmplificationScale; a: Amplification }) {
  const f = s.fit;
  return (
    <div className="grid gap-8 lg:grid-cols-2">
      <Figure
        title={`${s.label} contre le monde, une année par point (${per(f)})`}
        note={
          <>
            Pente de la droite : k = {nf(f.k.value)} {ci(f.k)}. Une pente de 1 voudrait dire que la région se réchauffe comme
            la moyenne mondiale. Abscisse : {a.covariate}.
          </>
        }
      >
        <ScatterFitChart
          years={s.series.years}
          x={s.series.covariate}
          y={s.series.values}
          fitted={s.series.fitted}
          rawYears={s.series.raw_years}
          xLabel="Monde"
          yLabel={s.label}
          fitLabel={`c + k·G, k = ${nf(f.k.value)}`}
          label={`Anomalie annuelle de ${s.label} en fonction de la température mondiale`}
        />
      </Figure>
      <Figure
        title={`${s.label} : observé et c + k·G, année par année`}
        note={
          <>
            Anomalies par rapport à 1961-1990. L&apos;écart entre les deux courbes est la variabilité propre de la région
            (autocorrélation ρ = {nf(f.rho)}, part de la variance expliquée {nf(f.r2 * 100, 0)} %).
          </>
        }
      >
        <LinesChart
          years={s.series.years}
          unit="°C"
          label={`Anomalie annuelle de ${s.label}, observée et reconstruite`}
          height="h-[300px] sm:h-[360px]"
          lines={[
            { name: "Observé", values: s.series.values, color: "--ink", width: 1.2, opacity: 0.6 },
            { name: "c + k·G", values: s.series.fitted, color: "--accent", width: 2 },
          ]}
        />
      </Figure>
    </div>
  );
}

function Factors({ a }: { a: Amplification }) {
  const rows: { label: string; cell: (s: AmplificationScale) => React.ReactNode }[] = [
    { label: "Contre le monde (k principal)", cell: (s) => <K e={s.fit.k} /> },
    { label: "Contre les terres émergées (CRUTEM5)", cell: (s) => <K e={s.land.k} /> },
    { label: "Été (juin-août), contre le monde", cell: (s) => <K e={s.summer.k} /> },
    { label: "Hiver (décembre-février), contre le monde", cell: (s) => <K e={s.winter.k} /> },
    {
      label: "Rapport des pentes de Sen (régionale / mondiale)",
      cell: (s) => (
        <>
          <b>{nf(s.slope_ratio)}</b>{" "}
          <span className="text-xs text-[var(--muted)]">
            {nf(s.slope_regional, 2)} / {nf(s.slope_global, 2)} °C par décennie
          </span>
        </>
      ),
    },
  ];
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[34rem] text-left text-sm">
        <thead className="text-xs text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-1.5 pr-3 font-medium" />
            {a.scales.map((s) => (
              <th key={s.id} className="py-1.5 pr-3 font-medium">
                {s.label} ({per(s.fit)})
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.label} className="border-b border-[var(--rule)] align-top">
              <td className="py-1.5 pr-3 text-[var(--muted)]">{r.label}</td>
              {a.scales.map((s) => (
                <td key={s.id} className="py-1.5 pr-3">
                  {r.cell(s)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-1 text-xs leading-relaxed text-[var(--muted)]">
        Seul le facteur contre le monde est soumis aux critères ; les autres lignes sont des informations. Sur{" "}
        {per(a.land_global)}, les terres émergées dans leur ensemble se réchauffent de {nf(a.land_global.k.value)}{" "}
        {ci(a.land_global.k)} °C par °C mondial ({a.land_reference}). Les saisons sont mesurées contre le même G annuel.
        Intervalles à 95 %.
      </p>
    </div>
  );
}

function Variants({ a }: { a: Amplification }) {
  const label = (id: string) => a.scales.find((s) => s.id === id)?.label ?? id;
  const groups = [
    { key: "robustesse", title: "Variantes de calcul (critère A5 : k > 1)" },
    { key: "poste", title: "Postes de Gironde (critère A6 : k > 0, intervalle recoupant celui du composite)" },
  ] as const;
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[34rem] text-left text-sm">
        <thead className="text-xs text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-1.5 pr-3 font-medium">Cas</th>
            <th className="py-1.5 pr-3 font-medium">Années</th>
            <th className="py-1.5 pr-3 font-medium">k</th>
            <th className="py-1.5 font-medium" />
          </tr>
        </thead>
        <tbody>
          {groups.map((g) => (
            <Fragment key={g.key}>
              <tr>
                <td colSpan={4} className="pt-3 pb-1 text-xs font-semibold text-[var(--muted)]">
                  {g.title}
                </td>
              </tr>
              {a.variants
                .filter((v) => v.group === g.key)
                .map((v) => (
                  <tr key={`${v.scale}-${v.label}`} className="border-b border-[var(--rule)] align-top">
                    <td className="py-1.5 pr-3">
                      {g.key === "robustesse" && <span className="text-xs text-[var(--muted)]">{label(v.scale)} · </span>}
                      {v.label}
                    </td>
                    <td className="py-1.5 pr-3">
                      {v.period.start}-{v.period.end} <span className="text-xs text-[var(--muted)]">({v.n})</span>
                    </td>
                    <td className="py-1.5 pr-3">
                      <K e={v.k} />
                    </td>
                    <td className={`py-1.5 ${v.ok ? "text-[var(--good)]" : "text-[var(--warm)]"}`}>{v.ok ? "✓" : "✗"}</td>
                  </tr>
                ))}
            </Fragment>
          ))}
        </tbody>
      </table>
      <p className="mt-1 text-xs leading-relaxed text-[var(--muted)]">
        Fourchette de contrôle du facteur de la France (critère A4) : [{nf(a.reference_low, 1)} ; {nf(a.reference_high, 1)}].{" "}
        {a.reference_source}.
      </p>
    </div>
  );
}

export default function AmplificationView({ a }: { a: Amplification }) {
  const [id, setId] = useState(a.scales[0]!.id);
  const s = a.scales.find((x) => x.id === id) ?? a.scales[0]!;
  return (
    <div className="space-y-8">
      <dl className="grid max-w-3xl grid-cols-2 gap-x-6 gap-y-2 text-sm sm:grid-cols-4">
        {a.scales.map((x) => (
          <div key={x.id}>
            <dt className="text-xs text-[var(--muted)]">
              k {x.label}, {per(x.fit)}
            </dt>
            <dd>
              <K e={x.fit.k} />
            </dd>
          </div>
        ))}
        <div>
          <dt className="text-xs text-[var(--muted)]">Terres émergées contre monde, {per(a.land_global)}</dt>
          <dd>
            <K e={a.land_global.k} />
          </dd>
        </div>
      </dl>
      <Segmented label="Échelle" value={id} onChange={setId} options={a.scales.map((x) => ({ key: x.id, label: x.label }))} />
      <p className="text-xs text-[var(--muted)]">
        {s.source}
        {s.series.raw_years.length > 0 &&
          ` ; années ${s.series.raw_years[0]}-${s.series.raw_years[s.series.raw_years.length - 1]} en partie ou entièrement non homogénéisées`}
        .
      </p>
      <Charts s={s} a={a} />
      <Figure title="Les facteurs d'amplification">
        <Factors a={a} />
      </Figure>
      <Figure title="Robustesse et cohérence">
        <Variants a={a} />
      </Figure>
    </div>
  );
}
