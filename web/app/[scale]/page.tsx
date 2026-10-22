import type { Metadata } from "next";
import { notFound } from "next/navigation";

import IndicatorList from "@/components/IndicatorList";
import { listIndicators } from "@/lib/data";
import { SCALE_LABELS } from "@/lib/format";
import { SCALES, scaleSchema } from "@/lib/schema";

export const dynamicParams = false;

export function generateStaticParams() {
  return SCALES.map((scale) => ({ scale }));
}

type Params = Promise<{ scale: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const parsed = scaleSchema.safeParse((await params).scale);
  return { title: parsed.success ? SCALE_LABELS[parsed.data].name : "Échelle inconnue" };
}

export default async function ScalePage({ params }: { params: Params }) {
  const parsed = scaleSchema.safeParse((await params).scale);
  if (!parsed.success) notFound();
  const scale = parsed.data;
  const label = SCALE_LABELS[scale];
  const items = listIndicators(scale);

  return (
    <div className="space-y-6">
      <header className="max-w-2xl space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">{label.name}</h1>
        <p className="text-[var(--muted)]">{label.blurb}</p>
      </header>
      {items.length > 0 ? (
        <IndicatorList items={items} />
      ) : (
        <p className="border-y border-[var(--rule)] py-3 text-sm text-[var(--muted)]">
          Aucun indicateur publié pour l&apos;instant. Prévu en {label.phase}.
        </p>
      )}
    </div>
  );
}
