import type { Metadata } from "next";
import { notFound } from "next/navigation";

import IndicatorList from "@/components/IndicatorList";
import ThemeSection from "@/components/ThemeSection";
import ValidationBox from "@/components/ValidationBox";
import { getValidation, listIndicators } from "@/lib/data";
import { nonMembers, themes } from "@/lib/family";
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

  if (listIndicators(scale).length === 0) {
    return (
      <div className="space-y-4">
        <h1 className="text-3xl font-semibold tracking-tight">{label.name}</h1>
        <p className="max-w-2xl text-[var(--muted)]">{label.blurb}</p>
        <p className="border-y border-[var(--rule)] py-3 text-sm text-[var(--muted)]">
          Aucun indicateur publié pour l&apos;instant. Prévu en {label.phase}.
        </p>
      </div>
    );
  }

  const ths = themes(scale);
  const others = nonMembers(scale);
  const reports = label.validations.flatMap((p) => getValidation(p) ?? []);

  return (
    <div className="space-y-12">
      <header className="max-w-3xl space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{label.name}</h1>
        <p className="text-sm text-[var(--muted)]">{label.blurb}</p>
      </header>

      {ths.map((t) => (
        <ThemeSection key={t.id} scale={scale} scaleName={label.name} theme={t} heading={ths.length > 1} />
      ))}

      <ValidationBox reports={reports} />

      {others.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-xl font-semibold">Autres indicateurs</h2>
          <IndicatorList items={others} />
        </section>
      )}
    </div>
  );
}
