// Paramètres statiques communs aux routes d'un indicateur (page et téléchargements).
import { getIndicator, getManifest } from "./data";
import { scaleSchema } from "./schema";

// Si Next transmet l'échelle du segment parent, on filtre dessus ; sinon on renvoie tous les couples.
export async function indicatorParams(props?: { params?: { scale?: string } | Promise<{ scale?: string }> }) {
  const parent = props?.params ? await props.params : undefined;
  return getManifest()
    .indicators.filter((e) => !parent?.scale || e.scale === parent.scale)
    .map((e) => ({ scale: e.scale, indicator: e.id }));
}

export async function indicatorFrom(params: Promise<{ scale: string; indicator: string }>) {
  const { scale, indicator } = await params;
  const parsed = scaleSchema.safeParse(scale);
  return parsed.success ? getIndicator(parsed.data, indicator) : undefined;
}
