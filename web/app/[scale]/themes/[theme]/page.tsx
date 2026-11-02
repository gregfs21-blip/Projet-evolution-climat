// Page d'un thème d'une échelle : générée pour chaque thème publié.
import type { Metadata } from "next";
import { notFound } from "next/navigation";

import ScaleView from "@/components/ScaleView";
import { scaleSections } from "@/lib/family";
import { SCALE_LABELS } from "@/lib/format";
import { SCALES, scaleSchema } from "@/lib/schema";

export const dynamicParams = false;

// Comme pour les indicateurs : si Next transmet l'échelle du segment parent, on filtre dessus.
export async function generateStaticParams(props?: { params?: { scale?: string } | Promise<{ scale?: string }> }) {
  const parent = props?.params ? await props.params : undefined;
  return SCALES.filter((s) => !parent?.scale || s === parent.scale).flatMap((scale) => scaleSections(scale).map((s) => ({ scale, theme: s.id })));
}

type Params = Promise<{ scale: string; theme: string }>;

async function load(params: Params) {
  const { scale, theme } = await params;
  const parsed = scaleSchema.safeParse(scale);
  if (!parsed.success) return undefined;
  const section = scaleSections(parsed.data).find((s) => s.id === theme);
  return section ? { scale: parsed.data, section } : undefined;
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const found = await load(params);
  return { title: found ? `${found.section.label}, ${SCALE_LABELS[found.scale].name}` : "Thème inconnu" };
}

export default async function ThemePage({ params }: { params: Params }) {
  const found = await load(params);
  if (!found) notFound();
  return <ScaleView scale={found.scale} active={found.section.id} />;
}
