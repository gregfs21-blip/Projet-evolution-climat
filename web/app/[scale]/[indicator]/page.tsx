// Modèle unique de page d'indicateur, pour toutes les échelles.
// Une page est générée par entrée du manifeste : ajouter un indicateur côté ETL
// suffit à faire apparaître sa page, sans code côté site.
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import ConfidenceBadge from "@/components/ConfidenceBadge";
import DemoBanner from "@/components/DemoBanner";
import KeyFigure from "@/components/KeyFigure";
import LimitsBox from "@/components/LimitsBox";
import TrendChart from "@/components/TrendChart";
import { getIndicator, getManifest } from "@/lib/data";
import { SCALE_LABELS } from "@/lib/format";
import { scaleSchema } from "@/lib/schema";

export const dynamicParams = false;

// `params` contient l'échelle générée par le segment parent. `await` couvre les deux
// conventions de Next (objet ou promesse) sans dépendre de la version.
export async function generateStaticParams({
  params,
}: {
  params: { scale: string } | Promise<{ scale: string }>;
}) {
  const { scale } = await params;
  return getManifest()
    .indicators.filter((e) => e.scale === scale)
    .map((e) => ({ indicator: e.id }));
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
          breakpoints={ind.breakpoints.map((b) => b.time)}
        />
        {ind.is_anomaly && ind.reference_period && (
          <p className="mt-1 text-xs text-[var(--muted)]">
            Écart à la moyenne {ind.reference_period.start}–{ind.reference_period.end}. Pointillés : droite de Sen.
          </p>
        )}
      </section>

      {/* 3. Les chiffres de tendance */}
      <section aria-label="Tendance" className="border-y border-[var(--rule)] py-5">
        <KeyFigure trend={ind.trend} unit={ind.unit} />
        <p className="mt-4 text-xs text-[var(--muted)]">
          Ruptures détectées :{" "}
          {ind.breakpoints.length > 0
            ? ind.breakpoints.map((b) => `${b.time} (${b.method})`).join(", ")
            : "aucune analyse de rupture pour l'instant"}
          .
        </p>
      </section>

      {/* 4. L'encart limites */}
      <LimitsBox ind={ind} />
    </article>
  );
}
