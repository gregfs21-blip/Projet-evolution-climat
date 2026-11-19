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

/** Règle unique des périodes de retour et rapports de probabilité (identique au constat, etl/demo_extremes.py `_n`) :
 *  une décimale sous 100, entier au-delà. */
const num = (v: number) => nf(v, Math.round(v * 10) / 10 < 100 ? 1 : 0); // arrondir d'abord : 99,96 → « 100 »
/** Pourcentage, une décimale au plus (2,5 %, 95 %). */
const pct = (l: number) => `${(l * 100).toLocaleString("fr-FR", { maximumFractionDigits: 1 })} %`;
/** Durée en années : singulier sous 2 (« 1,2 an »). */
const yrs = (v: number) => `${num(v)} ${v < 2 ? "an" : "ans"}`;
const inf = (v: number | null) => (v === null ? "∞" : num(v));

function Unb({ u, years = false, draws }: { u: Unbounded; years?: boolean; draws: number }) {
  const fixed = u.value !== null && u.ci_low === u.value && u.ci_high === u.value;
  return (
    <>
      <b>
        {fixed && Number.isInteger(u.value) ? `${u.value} ans` : u.value !== null && years ? yrs(u.value) : inf(u.value)}
      </b>
      {!fixed && (
        <span className="text-xs text-[var(--muted)]">
          {" "}
          [{inf(u.ci_low)} ; {inf(u.ci_high)}]
        </span>
      )}
      {fixed && <span className="text-xs text-[var(--muted)]"> (par construction)</span>}
      {u.infinite_draws > 0 && (
        <span className="block text-xs text-[var(--muted)]">
          ∞ dans {u.infinite_draws.toLocaleString("fr-FR")} tirage{u.infinite_draws > 1 ? "s" : ""} sur {(draws - u.undefined_draws).toLocaleString("fr-FR")}
          {u.undefined_draws > 0 && ` (${u.undefined_draws} indéfini${u.undefined_draws > 1 ? "s" : ""}, écarté${u.undefined_draws > 1 ? "s" : ""})`}
        </span>
      )}
    </>
  );
}

function Figure({ title, children, note }: { title: string; children: React.ReactNode; note?: React.ReactNode }) {
  return (
    <figure className="space-y-2">
      <figcaption className="text-sm font-semibold">{title}</figcaption>
      {children}
      {note && <div className="text-xs leading-relaxed text-[var(--muted)]">{note}</div>}
    </figure>
  );
}

function Events({ x }: { x: Extremes }) {
  const d = x.n_boot - x.n_failed;
  const pre = `${x.preindustrial_period.start}-${x.preindustrial_period.end}`;
  const rows: { label: string; cell: (e: ExtremeEvent) => React.ReactNode }[] = [
    { label: "Intensité", cell: (e) => <><b>{nf(e.value.value)} °C</b> <span className="text-xs text-[var(--muted)]">{ci(e.value)}</span></> },
    { label: `Période de retour en ${x.today_year}`, cell: (e) => <Unb u={e.return_period_today} years draws={d} /> },
    { label: `Période de retour en ${x.past_year}`, cell: (e) => <Unb u={e.return_period_past} years draws={d} /> },
    { label: `Probabilité ${x.today_year} / ${x.past_year}`, cell: (e) => <Unb u={e.probability_ratio} draws={d} /> },
    {
      label: `À rareté égale, écart ${x.today_year} − ${x.past_year}`,
      cell: (e) => <><b>{nf(e.intensity_change.value, 1, true)} °C</b> <span className="text-xs text-[var(--muted)]">{ci(e.intensity_change)}</span></>,
    },
    { label: `Période de retour en ${pre} (information)`, cell: (e) => <Unb u={e.return_period_preindustrial} years draws={d} /> },
    { label: `Probabilité ${x.today_year} / ${pre} (information)`, cell: (e) => <Unb u={e.probability_ratio_preindustrial} draws={d} /> },
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
        Intervalles à {pct(x.ci_level)} par rééchantillonnage des années ({d.toLocaleString("fr-FR")} tirages retenus sur{" "}
        {x.n_boot.toLocaleString("fr-FR")}). « ∞ » en valeur centrale : l&apos;événement dépasse la borne supérieure de la loi ajustée
        pour ce climat, il y est impossible selon le modèle, d&apos;où un rapport de probabilité infini. « ∞ » en borne
        d&apos;intervalle : au moins {pct((1 - x.ci_level) / 2)} des tirages placent l&apos;événement au-delà de cette borne. Un tirage
        « indéfini » donne 0/0 (événement au-delà de la borne dans les deux climats) ; il est écarté de l&apos;intervalle. Les
        périodes de retour longues sont des extrapolations (voir les limites).
      </p>
    </div>
  );
}

/** Mode d'emploi du graphe des niveaux de retour. Chiffres repris du JSON (aucun calcul nouveau, sauf la borne
 *  supérieure de la loi μ − σ/ξ, déduite des paramètres publiés, et des maxima de courbes déjà fournies). */
function ReturnLevelGuide({ x }: { x: Extremes }) {
  const c = x.curve;
  const past = `${x.past_year}`;
  const today = `${x.today_year}`;
  const T = nf(x.past_return_period, 0);
  const ref = x.events.find((e) => e.date === null);
  const record = x.events.find((e) => e.date !== null);
  const shift = ref?.intensity_change.value ?? record?.intensity_change.value ?? x.alpha.value * (x.g_today - x.g_past);
  const nObs = c.obs_periods.length;
  const maxObsT = Math.max(...c.obs_periods);
  const bounded = x.xi.value < 0;
  const bound = (g: number) => x.mu0 + x.alpha.value * g - x.sigma.value / x.xi.value;
  const d = x.n_boot - x.n_failed;
  const recPast = record?.return_period_past;
  const recFiniteDraws = recPast ? d - recPast.undefined_draws - recPast.infinite_draws : 0;
  const recDate = record?.date
    ? new Date(record.date).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" })
    : null;

  return (
    <div className="space-y-2 text-sm">
      <p>
        <b className="text-[var(--ink)]">Ce que montre le graphe.</b> Chaque été fournit une valeur : la journée la plus chaude de
        l&apos;année. Le graphe répond à la question « jusqu&apos;où peut monter cette journée, selon sa rareté ? ». L&apos;axe
        horizontal, logarithmique, est la période de retour T : un niveau de T ans a une chance sur T d&apos;être dépassé chaque
        année (T = 1 : un pic d&apos;été banal ; T = 10 : 10 % par an ; T = 100 : 1 % par an). L&apos;axe vertical donne la
        température correspondante. La courbe bleue est la loi ajustée pour le climat de {past}, la rouge la même loi pour le climat
        de {today} ; les bandes sont les intervalles à {pct(x.ci_level)}.
      </p>
      <p>
        <b className="text-[var(--ink)]">Les points.</b> Ce sont les {nObs} étés observés, chacun corrigé du réchauffement mondial
        de son année pour être exprimé dans le climat de {today} (points pleins) ou de {past} (cercles), puis placé à sa période de
        retour empirique (le plus chaud à environ {nf(maxObsT, 0)} ans). Rouges et bleus sont donc les mêmes données, décalées de{" "}
        {nf(shift)} °C. Qu&apos;ils suivent les courbes montre que la loi décrit bien les observations (Kolmogorov-Smirnov, p ={" "}
        {nf(x.ks_p, 2)}) ; ce n&apos;est pas une validation indépendante, puisque la correction utilise le α estimé par le même
        ajustement.
      </p>
      {ref && (
        <p>
          <b className="text-[var(--ink)]">Deux lectures.</b> Verticalement, à rareté égale : la chaleur de période de retour {T} ans
          passe de {nf(ref.value.value)} °C en {past} à {nf(ref.value.value + shift)} °C en {today}, soit {nf(shift, 1, true)} °C.
          Horizontalement, à intensité égale : partir de {nf(ref.value.value)} °C sur la courbe bleue (T = {T} ans) et suivre
          l&apos;horizontale jusqu&apos;à la courbe rouge, qu&apos;on croise à T ≈ {yrs(ref.return_period_today.value ?? NaN)}. Ce qui
          arrivait une fois tous les {T} ans arrive aujourd&apos;hui environ{" "}
          {Math.round(100 / (ref.return_period_today.value ?? Infinity))} % des étés.
        </p>
      )}
      {record && recPast && (
        <p>
          <b className="text-[var(--ink)]">Le record.</b> La ligne pointillée ({nf(record.value.value)} °C
          {recDate ? `, ${recDate}` : ""}) croise la courbe rouge vers{" "}
          {record.return_period_today.value !== null ? yrs(record.return_period_today.value) : "l'infini"}.{" "}
          {recPast.value === null && bounded
            ? `La courbe bleue plafonne vers ${nf(bound(x.g_past))} °C et ne l'atteint jamais : dans le climat de ${past}, le modèle le juge impossible, d'où les « ∞ » du tableau « Deux événements, deux climats ».`
            : recPast.value !== null
              ? `Sur la courbe bleue, il correspond à une période de retour d'environ ${yrs(recPast.value)}.`
              : ""}
        </p>
      )}
      {bounded && (
        <p>
          <b className="text-[var(--ink)]">Pourquoi les courbes plafonnent.</b> La forme estimée est négative (ξ ={" "}
          {nf(x.xi.value, 2)}) : la loi a une borne supérieure, environ {nf(bound(x.g_past))} °C dans le climat de {past} et{" "}
          {nf(bound(x.g_today))} °C dans celui de {today}. C&apos;est physiquement plausible (l&apos;assèchement des sols et
          l&apos;advection d&apos;air chaud ont des limites), mais cette borne est estimée sur {nObs} valeurs et reste mal connue.
        </p>
      )}
      <p>
        <b className="text-[var(--ink)]">Précautions.</b> L&apos;écart vertical est le même partout par construction : le modèle
        décale la loi sans la déformer (échelle σ et forme ξ fixes), il ne peut donc pas montrer que les extrêmes s&apos;écartent
        plus vite que les étés ordinaires.
        {record && recPast && recPast.value === null && recFiniteDraws > 0 && (
          <>
            {" "}
            « Impossible en {past} » se lit « au-delà de ce que les données permettent de quantifier » :{" "}
            {recFiniteDraws.toLocaleString("fr-FR")} tirages sur {d.toLocaleString("fr-FR")} ne placent pas le record au-delà de la
            borne, et la bande bleue monte jusqu&apos;à {nf(Math.max(...c.past_high))} °C.
          </>
        )}{" "}
        Enfin, au-delà d&apos;environ {nf(maxObsT, 0)} ans il n&apos;y a plus d&apos;observation : les courbes sont des
        extrapolations, d&apos;où les bandes qui s&apos;élargissent.
      </p>
    </div>
  );
}

function Variants({ x }: { x: Extremes }) {
  const record = x.events.find((e) => e.date !== null) ?? x.events[0]!;
  const d = x.n_boot - x.n_failed;
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
            <th className="py-1.5 pr-3 font-medium">Période de retour du record en {x.today_year}</th>
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
            <td className="py-1.5 pr-3">{record.return_period_today.value === null ? "∞" : yrs(record.return_period_today.value)}</td>
            <td className="py-1.5 pr-3">{inf(record.probability_ratio.value)}</td>
            <td />
          </tr>
          {groups.map((g) => (
            <Fragment key={g.id}>
              <tr>
                <td colSpan={7} className="pt-3 pb-1 text-xs font-semibold text-[var(--muted)]">
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
                    <td className="py-1.5 pr-3">{v.return_period_today === null ? <span className="text-[var(--muted)]">—</span> : yrs(v.return_period_today)}</td>
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
        Toutes les lignes : estimations centrales (intervalles de la référence dans le tableau des événements). Variantes : conformes si α &gt; 0 et rapport de probabilité du record &gt; 1
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
        note={<ReturnLevelGuide x={x} />}
      >
        <ReturnLevelChart
          curve={x.curve}
          pastLabel={`Climat de ${x.past_year}`}
          todayLabel={`Climat de ${x.today_year}`}
          marker={record ? { value: record.value.value, label: `record ${nf(record.value.value)} °C` } : undefined}
          ciLabel={pct(x.ci_level)}
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
            { name: "Position μ de la loi (dépassée près de 2 années sur 3)", values: s.mu, color: "--accent", width: 2 },
            {
              name: `Niveau de retour ${nf(x.past_return_period, 0)} ans de l'année`,
              values: s.level20,
              color: "--warm",
              width: 2,
              dashed: true,
            },
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
