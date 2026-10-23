// Modèle unique de page d'indicateur, pour toutes les échelles.
// Une page est générée par entrée du manifeste : ajouter un indicateur côté ETL
// suffit à faire apparaître sa page, sans code côté site.
//
// Ordre : où l'on est (fil d'Ariane, séries voisines) → les trois chiffres → la courbe →
// pourquoi on peut s'y fier → le détail technique, replié.
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import Breakpoints, { establishedBreaks } from "@/components/Breakpoints";
import DemoBanner from "@/components/DemoBanner";
import IndicatorChart from "@/components/IndicatorChart";
import KpiBand from "@/components/KpiBand";
import LimitsBox from "@/components/LimitsBox";
import SiblingPills from "@/components/SiblingPills";
import TrendTable from "@/components/TrendTable";
import WhyConfidence from "@/components/WhyConfidence";
import { getIndicator, getValidation } from "@/lib/data";
import { members, placeName, siblings } from "@/lib/family";
import { SCALE_LABELS } from "@/lib/format";
import { scaleSchema } from "@/lib/schema";
import { indicatorParams } from "@/lib/static-params";

export const dynamicParams = false;

// Génère les couples complets (échelle, indicateur) depuis le manifeste.
export const generateStaticParams = indicatorParams;

type Params = Promise<{ scale: string; indicator: string }>;

async function load(params: Params) {
  const { scale, indicator } = await params;
  const parsed = scaleSchema.safeParse(scale);
  if (!parsed.success) return undefined;
  return getIndicator(parsed.data, indicator);
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const ind = await load(params);
  return { title: ind?.title ?? "Indicateur inconnu", description: ind?.finding };
}

function Fold({ title, hint, children }: { title: string; hint: string; children: React.ReactNode }) {
  return (
    <details className="group border-t border-[var(--rule)] py-3">
      <summary className="cursor-pointer select-none">
        <span className="chevron mr-1 text-[var(--muted)]">▸</span>
        <span className="font-medium">{title}</span>
        <span className="ml-2 text-sm text-[var(--muted)]">{hint}</span>
      </summary>
      <div className="mt-4 space-y-5">{children}</div>
    </details>
  );
}

export default async function IndicatorPage({ params }: { params: Params }) {
  const ind = await load(params);
  if (!ind) notFound();

  const label = SCALE_LABELS[ind.scale];
  const self = members(ind.scale).find((m) => m.entry.id === ind.id);
  const sib = siblings(ind);
  const reports = label.validations.flatMap((p) => getValidation(p) ?? []);
  const ref = ind.reference_period;
  const refNormal = ref ? ind.normals.find((n) => n.period.start === ref.start && n.period.end === ref.end) : undefined;
  const base = `/${ind.scale}/${ind.id}`;

  return (
    <article className="space-y-8">
      <div className="space-y-3">
        <nav aria-label="Fil d'Ariane" className="text-sm text-[var(--muted)]">
          <Link href={`/${ind.scale}`} className="hover:underline">
            {label.name}
          </Link>
          {ind.group && <> › {ind.group}</>}
          {self && (
            <>
              {" "}
              › <span className="text-[var(--ink)]">{placeName(self, ind)}</span>
            </>
          )}
        </nav>
        {sib && <SiblingPills variables={sib.variables} places={sib.places} />}
      </div>

      {ind.is_demo && <DemoBanner />}

      <header className="max-w-3xl space-y-2">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{ind.title}</h1>
        <p className="text-sm text-[var(--muted)]">{ind.description}</p>
      </header>

      <KpiBand ind={ind} />

      <IndicatorChart
        time={ind.series.time}
        value={ind.series.value}
        quality={ind.series.quality}
        unit={ind.unit}
        isAnomaly={ind.is_anomaly}
        reference={ref ? `${ref.start}-${ref.end}` : null}
        offset={refNormal?.value ?? null}
        trend={
          ind.trend
            ? {
                start: ind.trend.period.start,
                end: ind.trend.period.end,
                fittedStart: ind.trend.fitted_start,
                fittedEnd: ind.trend.fitted_end,
              }
            : null
        }
        breakpoints={establishedBreaks(ind)}
        composite={
          sib?.composite
            ? { name: SCALE_LABELS[ind.scale].name + " (composite)", time: sib.composite.series.time, value: sib.composite.series.value }
            : null
        }
      />

      <WhyConfidence ind={ind} reports={reports} />

      <div className="border-b border-[var(--rule)]">
        <Fold title="Détails statistiques" hint="toutes les périodes, test classique vs Hamed-Rao, ruptures">
          <TrendTable trends={[...(ind.trend ? [ind.trend] : []), ...ind.alt_trends]} unit={ind.unit} />
          {ind.trend && <p className="text-xs text-[var(--muted)]">Méthode : {ind.trend.method}.</p>}
          <Breakpoints ind={ind} />
        </Fold>
        <Fold title="Limites et traçabilité" hint="source, licence, séries Météo-France, date d'extraction">
          <LimitsBox ind={ind} />
        </Fold>
        <Fold title="Télécharger les données" hint="série annuelle en CSV, fichier JSON complet">
          <ul className="space-y-1 text-sm">
            <li>
              <a className="underline underline-offset-2" href={`${base}/donnees.csv`} download={`${ind.id}.csv`}>
                {ind.id}.csv
              </a>{" "}
              <span className="text-[var(--muted)]">année, valeur, qualité (homogénéisée ou brute)</span>
            </li>
            <li>
              <a className="underline underline-offset-2" href={`${base}/donnees.json`} download={`${ind.id}.json`}>
                {ind.id}.json
              </a>{" "}
              <span className="text-[var(--muted)]">fichier publié par l&apos;ETL, tendances et métadonnées comprises</span>
            </li>
          </ul>
        </Fold>
      </div>
    </article>
  );
}
