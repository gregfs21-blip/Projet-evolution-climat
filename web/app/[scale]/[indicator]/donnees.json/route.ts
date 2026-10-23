// Fichier JSON publié par l'ETL pour cet indicateur, tel quel (déjà validé par zod au build).
import { indicatorFrom, indicatorParams } from "@/lib/static-params";

export const dynamic = "force-static";
export const dynamicParams = false;
export const generateStaticParams = indicatorParams;

export async function GET(_req: Request, { params }: { params: Promise<{ scale: string; indicator: string }> }) {
  const ind = await indicatorFrom(params);
  if (!ind) return new Response("Indicateur inconnu", { status: 404 });
  return Response.json(ind);
}
