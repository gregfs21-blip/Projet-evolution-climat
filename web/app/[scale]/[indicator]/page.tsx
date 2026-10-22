// Modèle unique de page d'indicateur, pour toutes les échelles.
// Une page est générée par entrée du manifeste : ajouter un indicateur côté ETL
// suffit à faire apparaître sa page, sans code côté site.
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import Breakpoints, { establishedBreaks } from "@/components/Breakpoints";
import ConfidenceBadge from "@/components/ConfidenceBadge";
import DemoBanner from "@/components/DemoBanner";
import KeyFigure from "@/components/KeyFigure";
import LimitsBox from "@/components/LimitsBox";
import Normals from "@/components/Normals";
import TrendChart from "@/components/TrendChart";
import TrendTable from "@/components/TrendTable";
import { getIndicator, getManifest } from "@/lib/data";
import { SCALE_LABELS } from "@/lib/format";
import { scaleSchema } from "@/lib/schema";

export const dynamicParams = false;

// Génère les couples complets (échelle, indicateur) depuis le manifeste.
// Si Next transmet l'échelle du segment parent, on filtre dessus ; sinon on
// renvoie tout. Les deux modes de génération (descendant et ascendant) sont couverts.
export async function generateStaticParams(props?: {
  params?: { scale?: string } | Promise<{ scale?: string }>;
}) {
  const parent = props?.params ? await props.params : undefined;
  const scale = parent?.scale;
  const params = getManifest()
    .indicators.filter((e) => !scale || e.scale === scale)
    .map((e) => ({ scale: e.scale, indicator: e.id }));
  console.log(`[generateStaticParams] parent=${JSON.stringify(parent ?? null)} → ${params.length} page(s)`);
  return params;
}

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

export default async function IndicatorPage({ params }: { params: Params }) {
  const ind = await load(params);
  if (!ind) notFound();

  return (
    <article className="space-y-8">
      <nav className="text-sm text-[var(--muted)]">
        <Link href={`/${ind.scale}`} className="hover:underline">
          {SCALE_LABELS[ind.scale].name}
        </Link>{" "}
        / {ind.id}
      </nav>

      {ind.is_demo && <DemoBanner />}

      <header className="max-w-3xl space-y-3">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{ind.title}</h1>
        {/* 1. Le constat en une phrase, avec son niveau de confiance */}
        <p className="text-lg">{ind.finding}</p>
        <ConfidenceBadge level={ind.confidence} />
        <p className="text-sm text-[var(--muted)]">{ind.description}</p>
      </header>

      {/* 2. La courbe */}
      <section aria-label="Série">
        <TrendChart
          time={ind.series.time}
          value={ind.series.value}
          unit={ind.unit}
          isAnomaly={ind.is_anomaly}
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
          quality={ind.series.quality}
        />
        {ind.is_anomaly && ind.reference_period && (
          <p className="mt-1 text-xs text-[var(--muted)]">
            Écart à la moyenne {ind.reference_period.start}–{ind.reference_period.end}. Pointillés : droite de Sen.
            {ind.series.quality?.includes("raw") && " Barres grises : années non homogénéisées, exclues de la tendance."}
          </p>
        )}
      </section>

      {/* 3. Les chiffres de tendance */}
      <section aria-label="Tendance" className="space-y-5 border-y border-[var(--rule)] py-5">
        <KeyFigure trend={ind.trend} unit={ind.unit} />
        <Normals normals={ind.normals} unit={ind.unit} />
        <TrendTable trends={[...(ind.trend ? [ind.trend] : []), ...ind.alt_trends]} unit={ind.unit} />
        <Breakpoints ind={ind} />
      </section>

      {/* 4. L'encart limites */}
      <LimitsBox ind={ind} />
    </article>
  );
}
