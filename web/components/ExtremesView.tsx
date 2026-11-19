// Résultats de l'analyse des valeurs extrêmes (P10.2). Tous les chiffres viennent de data/processed/demonstration.json ;
// la page ne fait que les mettre en forme (∞ = valeur au-delà de la borne supérieure de la loi ajustée).
import { Fragment } from "react";

import LinesChart from "./LinesChart";
import ReturnLevelChart from "./ReturnLevelChart";
import type { Estimate, ExtremeEvent, Extremes, Unbounded } from "@/lib/schema";

const nf = (v: number, d = 1, sign = false) =>
  v.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d, signDisplay: sign ? "always" : "auto" });
const ci = (e: Estimate, d = 1) => (e.ci_low !== null && e.ci_high !== null ? `[${nf(e.ci_low, d)} ; ${nf(e.ci_high, d)}]` : "");
const pv = (p: number) => (p < 0.001 ? "< 0,001" : nf(p, 3));

/** Nombre sans infini : 1 décimale sous 10, entier au-delà. */
const num = (v: number) => nf(v, v < 10 ? 1 : 0);
const inf = (v: number | null) => (v === null ? "∞" : num(v));

function Unb({ u, unit = "" }: { u: Unbounded; unit?: string }) {
  const fixed = u.value !== null && u.ci_low === u.value && u.ci_high === u.value;
  return (
    <>
      <b>
        {inf(u.value)}
        {u.value !== null && unit}
      </b>
      {!fixed && (u.ci_low !== null || u.ci_high !== null || u.value === null) && (
        <span className="text-xs text-[var(--muted)]">
          {" "}
          [{inf(u.ci_low)} ; {inf(u.ci_high)}]
        </span>
      )}
      {fixed && <span className="text-xs text-[var(--muted)]"> (par construction)</span>}
      {u.undefined_draws > 0 && <span className="text-xs text-[var(--muted)]"> · {u.undefined_draws} tirage(s) indéfini(s)</span>}
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

function Events({ x }: { x: Extremes }) {
  const rows: { label: string; cell: (e: ExtremeEvent) => React.ReactNode }[] = [
    { label: "Intensité", cell: (e) => <><b>{nf(e.value.value)} °C</b> <span className="text-xs text-[var(--muted)]">{ci(e.value)}</span></> },
    { label: `Période de retour en ${x.today_year}`, cell: (e) => <Unb u={e.return_period_today} unit=" ans" /> },
    { label: `Période de retour en ${x.past_year}`, cell: (e) => <Unb u={e.return_period_past} unit=" ans" /> },
    { label: `Probabilité ${x.today_year} / ${x.past_year}`, cell: (e) => <Unb u={e.probability_ratio} /> },
    {
      label: `À rareté égale, écart ${x.today_year} − ${x.past_year}`,
      cell: (e) => <><b>{nf(e.intensity_change.value, 1, true)} °C</b> <span className="text-xs text-[var(--muted)]">{ci(e.intensity_change)}</span></>,
    },
    { label: "Période de retour en 1880-1900 (information)", cell: (e) => <Unb u={e.return_period_preindustrial} unit=" ans" /> },
    { label: `Probabilité ${x.today_year} / 1880-1900 (information)`, cell: (e) => <Unb u={e.probability_ratio_preindustrial} /> },
  ];
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[34rem] text-left text-sm">
        <thead className="text-xs text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-1.5 pr-3 font-medium" />
            {x.events.map((e) => (
              <th key={e.id} className="py-1.5 pr-3 font-medium">
                {e.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.label} className="border-b border-[var(--rule)] align-top">
              <td className="py-1.5 pr-3 text-[var(--muted)]">{r.label}</td>
              {x.events.map((e) => (
                <td key={e.id} className="py-1.5 pr-3">
                  {r.cell(e)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-1 text-xs leading-relaxed text-[var(--muted)]">
        Intervalles à 95 % par rééchantillonnage des années ({x.n_boot.toLocaleString("fr-FR")} tirages). « ∞ » : la valeur dépasse la
        borne supérieure de la loi ajustée pour ce climat, elle y est impossible selon le modèle ; un rapport de probabilité infini en
        découle. Les périodes de retour longues sont des extrapolations (voir les limites).
      </p>
    </div>
  );
}

function Variants({ x }: { x: Extremes }) {
  const record = x.events.find((e) => e.date !== null) ?? x.events[0]!;
  const groups = [
    { id: "robustesse" as const, title: "Variantes de calcul (critère X5)" },
    { id: "station" as const, title: "Autres postes de Gironde (critère X6)" },
  ];
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[36rem] text-left text-sm">
        <thead className="text-xs text-[var(--muted)]">
          <tr className="border-b border-[var(--rule)]">
            <th className="py-1.5 pr-3 font-medium">Cas</th>
            <th className="py-1.5 pr-3 font-medium">Années</th>
            <th className="py-1.5 pr-3 font-medium">α (°C par °C)</th>
            <th className="py-1.5 pr-3 font-medium">ξ</th>
            <th className="py-1.5 pr-3 font-medium">Rapport de probabilité du record</th>
            <th className="py-1.5 font-medium" />
          </tr>
        </thead>
        <tbody>
          <tr className="border-b border-[var(--rule)] align-top">
            <td className="py-1.5 pr-3 font-medium">Référence : {x.station}</td>
            <td className="py-1.5 pr-3">
              {x.period.start}-{x.period.end}
            </td>
            <td className="py-1.5 pr-3">
              <b>{nf(x.alpha.value, 2)}</b> <span className="text-xs text-[var(--muted)]">{ci(x.alpha, 2)}</span>
            </td>
            <td className="py-1.5 pr-3">{nf(x.xi.value, 2)}</td>
            <td className="py-1.5 pr-3">
              <Unb u={record.probability_ratio} />
            </td>
            <td />
          </tr>
          {groups.map((g) => (
            <Fragment key={g.id}>
              <tr>
                <td colSpan={6} className="pt-3 pb-1 text-xs font-semibold text-[var(--muted)]">
                  {g.title}
                </td>
              </tr>
              {x.variants
                .filter((v) => v.group === g.id)
                .map((v) => (
                  <tr key={`${g.id}-${v.label}`} className="border-b border-[var(--rule)] align-top">
                    <td className="py-1.5 pr-3">{v.label}</td>
                    <td className="py-1.5 pr-3">
                      {v.period.start}-{v.period.end} <span className="text-xs text-[var(--muted)]">({v.n})</span>
                    </td>
                    <td className="py-1.5 pr-3">
                      {nf(v.alpha.value, 2)} <span className="text-xs text-[var(--muted)]">{ci(v.alpha, 2)}</span>
                    </td>
                    <td className="py-1.5 pr-3">{nf(v.xi, 2)}</td>
                    <td className="py-1.5 pr-3">
                      {v.probability_ratio_status === "fini" ? (
                        num(v.probability_ratio!)
                      ) : v.probability_ratio_status === "infini" ? (
                        "∞"
                      ) : v.probability_ratio_status === "indefini" ? (
                        "indéfini (0/0)"
                      ) : (
                        <span className="text-[var(--muted)]">—</span>
                      )}
                    </td>
                    <td className={`py-1.5 ${v.ok ? "text-[var(--good)]" : "text-[var(--warm)]"}`}>{v.ok ? "✓" : "✗"}</td>
                  </tr>
                ))}
            </Fragment>
          ))}
        </tbody>
      </table>
      <p className="mt-1 text-xs leading-relaxed text-[var(--muted)]">
        Variantes : estimations centrales, sans rééchantillonnage ; conformes si α &gt; 0 et rapport de probabilité du record &gt; 1
        (pour TX3x, le record est la valeur TX3x de {x.today_year}). Autres postes : α &gt; 0 et intervalle recouvrant celui de
        la station de référence. Référence publiée pour α : {x.reference_source}.
      </p>
    </div>
  );
}

export default function ExtremesView({ x }: { x: Extremes }) {
  const s = x.series;
  const record = x.events.find((e) => e.date !== null);
  const rawNote =
    s.raw_years.length > 0
      ? `Années ${s.raw_years[0]}-${s.raw_years[s.raw_years.length - 1]} prises brutes (pas encore homogénéisées), autorisé par le critère X1.`
      : "";
  return (
    <div className="space-y-8">
      <dl className="grid max-w-3xl grid-cols-2 gap-x-6 gap-y-2 text-sm sm:grid-cols-4">
        <div>
          <dt className="text-xs text-[var(--muted)]">α, °C par °C mondial</dt>
          <dd>
            <b>{nf(x.alpha.value, 2)}</b> <span className="text-xs text-[var(--muted)]">{ci(x.alpha, 2)}</span>
          </dd>
        </div>
        <div>
          <dt className="text-xs text-[var(--muted)]">Réchauffement mondial {x.past_year} → {x.today_year}</dt>
          <dd>
            <b>{nf(x.g_today - x.g_past, 2, true)} °C</b>
          </dd>
        </div>
        <div>
          <dt className="text-xs text-[var(--muted)]">Test du décalage (rapport de vraisemblance)</dt>
          <dd>p {pv(x.lrt_p)}</dd>
        </div>
        <div>
          <dt className="text-xs text-[var(--muted)]">Forme ξ · ajustement (KS)</dt>
          <dd>
            {nf(x.xi.value, 2)} · p = {nf(x.ks_p, 2)}
          </dd>
        </div>
      </dl>

      <Figure
        title={`Niveaux de retour de ${x.index_label.split(",")[0]} à ${x.station}, climat de ${x.past_year} et climat de ${x.today_year}`}
        note={
          <>
            Lecture : pour une période de retour donnée (axe horizontal, logarithmique), la courbe donne la chaleur atteinte en moyenne une
            fois par période. L&apos;écart vertical entre les deux courbes est le gain d&apos;intensité à rareté égale ; l&apos;écart
            horizontal, le changement de fréquence. Les courbes plafonnent parce que la loi ajustée a une borne supérieure (ξ &lt; 0).
          </>
        }
      >
        <ReturnLevelChart
          curve={x.curve}
          pastLabel={`Climat de ${x.past_year}`}
          todayLabel={`Climat de ${x.today_year}`}
          marker={record ? { value: record.value.value, label: `record ${nf(record.value.value)} °C` } : undefined}
          label={`Niveaux de retour de la température maximale annuelle à ${x.station}`}
        />
      </Figure>

      <Figure
        title={`${x.index_label} à ${x.station}, ${x.period.start}-${x.period.end}`}
        note={
          <>
            La position de la loi suit la température mondiale lissée ({x.covariate}) : elle monte avec le réchauffement, sans hypothèse de
            tendance linéaire. {rawNote}
          </>
        }
      >
        <LinesChart
          years={s.years}
          signed={false}
          unit="°C"
          label={`${x.index_label} à ${x.station}`}
          height="h-[280px] sm:h-[340px]"
          lines={[
            { name: "Maximum observé de l'année", values: s.values, color: "--ink", width: 1.2, opacity: 0.7 },
            { name: "Valeur la plus probable (position μ de la loi)", values: s.mu, color: "--accent", width: 2 },
            { name: "Niveau de retour 20 ans de l'année", values: s.level20, color: "--warm", width: 2, dashed: true },
          ]}
        />
      </Figure>

      <Figure title="Deux événements, deux climats">
        <Events x={x} />
      </Figure>

      <Figure title="Robustesse et cohérence régionale">
        <Variants x={x} />
      </Figure>
    </div>
  );
}
