// Démonstration de l'évolution du climat (P10) : analyses qui croisent plusieurs séries pour établir ce qui change
// et pourquoi. Tout est produit par l'ETL (etl/demonstration.py) ; la page n'écrit aucun chiffre.
import type { Metadata } from "next";
import Link from "next/link";

import ConfidenceBadge from "@/components/ConfidenceBadge";
import RegressionView from "@/components/RegressionView";
import ValidationBox from "@/components/ValidationBox";
import { getDemonstration, getValidation } from "@/lib/data";
import { fmtDateTime, REPO_URL } from "@/lib/format";
import ExtremesView from "@/components/ExtremesView";
import type { Extremes, Regression } from "@/lib/schema";

type Result = Regression | Extremes;

export const metadata: Metadata = { title: "Démonstration" };

function Criteria({ reg }: { reg: Result }) {
  const ids = reg.criteria.map((c) => c.id);
  return (
    <details className="rounded-lg border border-[var(--rule)] px-4 py-3 text-sm">
      <summary className="cursor-pointer font-medium">
        <span className="chevron">▸</span> Critères fixés avant le calcul ({ids[0]}-{ids[ids.length - 1]}) : {reg.criteria.filter((c) => c.satisfied).length}/
        {reg.criteria.length} conformes
      </summary>
      <ul className="mt-3 space-y-2">
        {reg.criteria.map((c) => (
          <li key={c.id}>
            <span className={c.satisfied ? "text-[var(--good)]" : "text-[var(--warm)]"}>{c.satisfied ? "✓" : "✗"}</span>{" "}
            <span className="font-medium">
              {c.id} {c.label}
            </span>
            <div className="text-xs break-words text-[var(--muted)]">{c.detail}</div>
          </li>
        ))}
      </ul>
    </details>
  );
}

function MethodAndLimits({ reg }: { reg: Result }) {
  return (
    <details className="rounded-lg border border-[var(--rule)] px-4 py-3 text-sm">
      <summary className="cursor-pointer font-medium">
        <span className="chevron">▸</span> Méthode, limites et sources
      </summary>
      <div className="mt-3 space-y-4">
        <p className="font-mono text-xs">{reg.model}</p>
        <p className="leading-relaxed">{reg.method_note}</p>
        <div>
          <h4 className="mb-1 text-xs font-semibold text-[var(--muted)]">Limites</h4>
          <ul className="list-disc space-y-1 pl-5">
            {reg.limitations.map((l) => (
              <li key={l}>{l}</li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="mb-1 text-xs font-semibold text-[var(--muted)]">Données</h4>
          <ul className="space-y-1">
            {reg.inputs.map((i) => (
              <li key={i.name}>
                <a className="underline underline-offset-2" href={i.url} rel="noopener noreferrer" target="_blank">
                  {i.name}
                </a>{" "}
                <span className="text-xs text-[var(--muted)]">
                  — {i.license}
                  {i.note ? ` ; ${i.note}` : ""}
                </span>
              </li>
            ))}
          </ul>
          {"enso_oni_correlation" in reg && (
            <p className="mt-2 text-xs text-[var(--muted)]">
              Corrélation entre l&apos;indice ENSO utilisé et l&apos;ONI de la NOAA : r ={" "}
              {reg.enso_oni_correlation.toLocaleString("fr-FR", { maximumFractionDigits: 3 })}.
            </p>
          )}
        </div>
        <p className="font-mono text-xs text-[var(--muted)]">
          {reg.script} · ETL {reg.etl_version} · {fmtDateTime(reg.extracted_at)} ·{" "}
          <a className="underline underline-offset-2" href={`${REPO_URL}/blob/main/docs/phases.md`} rel="noopener noreferrer" target="_blank">
            cadrage P10
          </a>
        </p>
      </div>
    </details>
  );
}

export default function DemonstrationPage() {
  const demo = getDemonstration();
  const report = getValidation("p10");
  if (!demo) {
    return (
      <article className="max-w-3xl space-y-4">
        <h1 className="text-3xl font-semibold tracking-tight">Démonstration de l&apos;évolution du climat</h1>
        <p className="text-[var(--muted)]">Les analyses ne sont pas encore calculées.</p>
      </article>
    );
  }
  return (
    <div className="space-y-12">
      <header className="max-w-3xl space-y-3">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Démonstration de l&apos;évolution du climat</h1>
        <p className="leading-relaxed">
          Les pages Gironde, France et Monde décrivent ce qui change, série par série. Cet onglet croise les séries pour
          répondre à deux questions de plus : ce changement est-il réel, et d&apos;où vient-il ? Deux courbes qui montent
          ensemble ne prouvent rien, puisque n&apos;importe quelle grandeur qui augmente avec le temps leur est
          « corrélée ». Chaque analyse repose donc sur un modèle explicite, des critères fixés avant le calcul et
          une comparaison avec des estimations publiées.
        </p>
        <ol className="space-y-1 text-sm">
          {demo.analyses.map((a) => (
            <li key={a.id} className="flex flex-wrap items-baseline gap-2">
              <span className="rounded-full border border-[var(--rule)] px-1.5 text-[11px] leading-4">{a.phase.toUpperCase()}</span>
              {a.status === "publie" ? (
                <a href={`#${a.id}`} className="underline underline-offset-2">
                  {a.title}
                </a>
              ) : (
                <span className="text-[var(--muted)]">
                  {a.title} <span className="text-xs">(à venir)</span>
                </span>
              )}
            </li>
          ))}
        </ol>
        <p className="text-xs text-[var(--muted)]">Calculée le {fmtDateTime(demo.generated_at)}.</p>
      </header>

      {demo.analyses
        .filter((a) => a.status === "publie" && a.regression)
        .map((a) => {
          const reg = a.regression!;
          return (
            <section key={a.id} id={a.id} className="scroll-mt-20 space-y-6">
              <div className="max-w-3xl space-y-3">
                <p className="text-xs font-semibold tracking-wider text-[var(--muted)] uppercase">{a.phase.toUpperCase()} · régression multiple</p>
                <h2 className="text-2xl font-semibold tracking-tight">{a.title}</h2>
                <p className="text-[var(--muted)] italic">{a.question}</p>
                <div className="flex flex-wrap items-center gap-2">
                  <ConfidenceBadge level={reg.confidence} />
                </div>
                <p className="leading-relaxed">{reg.finding}</p>
                <p className="text-sm text-[var(--muted)]">{reg.confidence_reason}</p>
                <p className="text-sm leading-relaxed">
                  Principe : la température mondiale est décrite comme la somme de quatre influences, chacune multipliée par un
                  coefficient que les données estiment. Le forçage d&apos;origine humaine (surtout les gaz à effet de serre, moins
                  l&apos;effet des aérosols),
                  les éruptions volcaniques, l&apos;activité du soleil, et El Niño / La Niña, qui déplace de la chaleur entre
                  l&apos;océan et l&apos;atmosphère sans en créer. Si le forçage humain n&apos;expliquait rien, son coefficient
                  serait nul : c&apos;est ce que teste le critère O3. Le réchauffement que le modèle lui attribue est ensuite comparé à
                  l&apos;estimation de l&apos;IGCC, obtenue par d&apos;autres méthodes mais à partir des mêmes forçages : un
                  recoupement, pas une preuve indépendante (critère O4).
                </p>
              </div>
              <RegressionView reg={reg} />
              <div className="max-w-3xl space-y-3">
                <Criteria reg={reg} />
                <MethodAndLimits reg={reg} />
              </div>
            </section>
          );
        })}

      {demo.analyses
        .filter((a) => a.status === "publie" && a.extremes)
        .map((a) => {
          const x = a.extremes!;
          return (
            <section key={a.id} id={a.id} className="scroll-mt-20 space-y-6">
              <div className="max-w-3xl space-y-3">
                <p className="text-xs font-semibold tracking-wider text-[var(--muted)] uppercase">{a.phase.toUpperCase()} · valeurs extrêmes</p>
                <h2 className="text-2xl font-semibold tracking-tight">{a.title}</h2>
                <p className="text-[var(--muted)] italic">{a.question}</p>
                <div className="flex flex-wrap items-center gap-2">
                  <ConfidenceBadge level={x.confidence} />
                </div>
                <p className="leading-relaxed">{x.finding}</p>
                <p className="text-sm text-[var(--muted)]">{x.confidence_reason}</p>
                <p className="text-sm leading-relaxed">
                  Principe : une moyenne qui monte ne dit pas comment évoluent les extrêmes, qui comptent pour la santé, les
                  cultures et les réseaux. On prend la journée la plus chaude de chaque année et on décrit sa loi de probabilité
                  par une loi des valeurs extrêmes dont la position suit la température mondiale. Si la chaleur extrême de
                  Bordeaux n&apos;avait pas évolué avec le réchauffement mondial, le coefficient α serait nul : c&apos;est ce que
                  teste le critère X3. Un α positif établit une évolution commune ; il ne dit pas quelle part revient à des
                  facteurs qui ont changé en même temps (urbanisation, aérosols, circulation atmosphérique). La loi ajustée permet
                  ensuite de comparer, pour un même événement, sa fréquence dans le climat de {x.past_year} et dans celui de{" "}
                  {x.today_year}. La régression ci-dessus porte sur la seule moyenne mondiale : ses conclusions sur la part
                  humaine ne se transposent pas aux maxima de Bordeaux.
                </p>
              </div>
              <ExtremesView x={x} />
              <div className="max-w-3xl space-y-3">
                <Criteria reg={x} />
                <MethodAndLimits reg={x} />
              </div>
            </section>
          );
        })}

      {report && (
        <div className="max-w-3xl">
          <ValidationBox reports={[report]} />
        </div>
      )}
      <p className="max-w-3xl text-xs text-[var(--muted)]">
        Les séries utilisées sont publiées sur la page{" "}
        <Link href="/monde" className="underline underline-offset-2">
          Monde
        </Link>
        .
      </p>
    </div>
  );
}
