// Série annuelle d'un indicateur en CSV, générée au build (aucun calcul : recopie du JSON publié).
import { indicatorFrom, indicatorParams } from "@/lib/static-params";

export const dynamic = "force-static";
export const dynamicParams = false;
export const generateStaticParams = indicatorParams;

export async function GET(_req: Request, { params }: { params: Promise<{ scale: string; indicator: string }> }) {
  const ind = await indicatorFrom(params);
  if (!ind) return new Response("Indicateur inconnu", { status: 404 });
  const head = [
    `# ${ind.title}`,
    `# ${ind.description}`,
    `# Unité : ${ind.unit}${ind.reference_period ? ` ; écart à la moyenne ${ind.reference_period.start}-${ind.reference_period.end}` : ""}`,
    `# Source : ${ind.provenance.source_name} (${ind.provenance.license}) ; ETL ${ind.provenance.etl_version}`,
    "periode,valeur,qualite",
  ];
  const rows = ind.series.time.map((t, i) => `${t},${ind.series.value[i] ?? ""},${ind.series.quality?.[i] ?? ""}`);
  return new Response([...head, ...rows].join("\n") + "\n", {
    headers: { "content-type": "text/csv; charset=utf-8" },
  });
}
