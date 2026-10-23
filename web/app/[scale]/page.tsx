import type { Metadata } from "next";
import { notFound } from "next/navigation";

import CompositeCards from "@/components/CompositeCards";
import IndicatorList from "@/components/IndicatorList";
import StationsMap from "@/components/StationsMap";
import StationsOverlay from "@/components/StationsOverlay";
import TrendMatrix from "@/components/TrendMatrix";
import ValidationBox from "@/components/ValidationBox";
import { getValidation, listIndicators } from "@/lib/data";
import { composites, familyMatrix, mapPoints, nonMembers, overlays, VARIABLES, type VarKey } from "@/lib/family";
import { fmt, fmtSigned, SCALE_LABELS } from "@/lib/format";
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

  const comps = composites(scale);
  const matrix = familyMatrix(scale);
  const over = overlays(scale);
  const points = mapPoints(scale);
  const others = nonMembers(scale);
  const reports = label.validations.flatMap((p) => getValidation(p) ?? []);
  const initial: VarKey = matrix.variables.includes("tm") ? "tm" : (matrix.variables[0] ?? "tm");
  const period = matrix.period ? `${matrix.period.start}-${matrix.period.end}` : "";
  const spreads = Object.values(matrix.spread);
  const maxSpread = spreads.length ? Math.max(...spreads.map((s) => s.max - s.min)) : null;
  const nStations = matrix.rows.filter((r) => !r.isComposite).length;
  const allSignificant = comps.every((c) => c.ind.trend?.significant);
  const p0 = comps[0]?.ind.trend?.period;
  const ref0 = comps[0]?.ind.reference_period;

  return (
    <div className="space-y-12">
      <header className="max-w-3xl space-y-3">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{label.name}</h1>
        {comps.length > 0 && p0 && (
          // Constat entièrement calculé à partir des JSON publiés : aucune conclusion rédigée à la main ici.
          <p className="text-lg leading-relaxed">
            Composite {label.name} {p0.start}-{p0.end} :{" "}
            {comps.map((c, i) => (
              <span key={c.variable}>
                {i > 0 && (i === comps.length - 1 ? " et " : ", ")}
                {VARIABLES[c.variable].code} <b className="font-mono">{c.ind.trend ? fmtSigned(c.ind.trend.slope_per_decade) : "—"}</b>
              </span>
            ))}{" "}
            °C par décennie{allSignificant ? ", tendances toutes significatives après correction de l'autocorrélation" : ""}.
            {maxSpread !== null && nStations > 1 && (
              <>
                {" "}
                Sur la période commune {period}, les pentes des {nStations} stations diffèrent au plus de{" "}
                <b className="font-mono">{fmt(maxSpread)} °C/déc.</b>, quelle que soit la variable.
              </>
            )}
          </p>
        )}
        <p className="text-sm text-[var(--muted)]">{label.blurb}</p>
      </header>

      {comps.length > 0 && (
        <section className="space-y-2" aria-label="Chiffres-clés">
          <CompositeCards scale={scale} />
          <p className="text-xs text-[var(--muted)]">
            Barres : écart annuel{ref0 ? ` à la moyenne ${ref0.start}-${ref0.end}` : ""} ; pointillés : droite de Sen ; gris : années non homogénéisées, hors
            tendance. Une carte ouvre la page détaillée.
          </p>
        </section>
      )}

      {matrix.rows.length > 1 && (
        <div className="grid gap-10 lg:grid-cols-[1.15fr_1fr]">
          <section className="space-y-2 border-t border-[var(--rule)] pt-4">
            <h2 className="text-xl font-semibold">Les stations comparées</h2>
            <StationsOverlay data={over} variables={matrix.variables} initial={initial} />
          </section>
          <section className="space-y-2 border-t border-[var(--rule)] pt-4">
            <h2 className="text-xl font-semibold">Tendance par station</h2>
            <TrendMatrix matrix={matrix} />
          </section>
        </div>
      )}

      {Object.values(points).some((p) => p.length > 1) && (
        <section className="space-y-2 border-t border-[var(--rule)] pt-4">
          <h2 className="text-xl font-semibold">Carte des stations</h2>
          <StationsMap points={points} variables={matrix.variables} initial={initial} period={period} />
        </section>
      )}

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
