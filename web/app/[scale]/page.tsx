import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import ScaleView from "@/components/ScaleView";
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

  if (scale === "monde") {
    return (
      <>
        <p className="mb-6 text-sm text-[var(--muted)]">
          Les aérodromes les plus chauds et les plus froids en ce moment :{" "}
          <Link href="/instantane" className="underline underline-offset-2">
            Instantané
          </Link>
          .
        </p>
        <ScaleView scale={scale} />
      </>
    );
  }
  return <ScaleView scale={scale} />;
}
