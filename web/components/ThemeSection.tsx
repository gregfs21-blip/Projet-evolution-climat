// Un thème d'une échelle (ex. « Températures annuelles ») : constat calculé, chiffres-clés des composites,
// stations superposées, matrice et carte. Générique : tout vient du manifeste et des JSON.
import CompositeCards from "./CompositeCards";
import StationsMap from "./StationsMap";
import StationsOverlay from "./StationsOverlay";
import TrendMatrix from "./TrendMatrix";
import { composites, familyMatrix, mapPoints, overlays, type Theme } from "@/lib/family";
import { fmt, fmt1, fmtSigned } from "@/lib/format";
import type { Scale } from "@/lib/schema";

export default function ThemeSection({ scale, scaleName, theme, heading }: { scale: Scale; scaleName: string; theme: Theme; heading: boolean }) {
  const comps = composites(scale, theme.id);
  const matrix = familyMatrix(scale, theme);
  const over = overlays(scale, theme.id);
  const points = mapPoints(scale, theme.id);
  const vars = theme.variables.map((v) => ({ id: v.id, code: v.code, label: v.label }));
  // Variable affichée par défaut : celle du milieu du thème (TM pour TN/TM/TX).
  const initial = theme.variables[Math.floor((theme.variables.length - 1) / 2)]?.id ?? "";
  const period = matrix.period ? `${matrix.period.start}-${matrix.period.end}` : "";
  const spreads = Object.values(matrix.spread);
  const maxSpread = spreads.length ? Math.max(...spreads.map((s) => s.max - s.min)) : null;
  // Stations ayant au moins une pente sur la période commune (une série incomplète n'entre pas dans la comparaison).
  const nStations = matrix.rows.filter((r) => !r.isComposite && Object.values(r.cells).some((c) => c.slope !== null)).length;
  const trended = comps.filter((c) => c.ind.headline !== "normals");
  const allSignificant = trended.length > 0 && trended.every((c) => c.ind.trend?.significant);
  const p0 = comps[0]?.ind.trend?.period;
  // Périodes différentes selon les variables (ex. CO₂ depuis 1979, CH₄ depuis 1984) : période donnée pour chacune.
  const samePeriod = trended.every((c) => c.ind.trend?.period.start === p0?.start && c.ind.trend?.period.end === p0?.end);
  const ref0 = comps[0]?.ind.reference_period;
  const u = theme.unit;

  return (
    <section className="space-y-10" aria-label={theme.label}>
      <div className="max-w-3xl space-y-2">
        {heading && <h2 className="text-2xl font-semibold tracking-tight">{theme.label}</h2>}
        {comps.length > 0 && p0 && (
          // Constat entièrement calculé à partir des JSON publiés : aucune conclusion rédigée à la main ici.
          <p className="text-lg leading-relaxed">
            {comps[0]?.ind.stations.length ? `Composite ${scaleName}` : scaleName}
            {samePeriod ? ` ${p0.start}-${p0.end}` : ""} :{" "}
            {trended.map((c, i) => (
              <span key={c.variable.id}>
                {i > 0 && (i === trended.length - 1 ? " et " : ", ")}
                {c.variable.code} <b className="font-mono">{c.ind.trend ? fmtSigned(c.ind.trend.slope_per_decade) : "—"}</b>
                {u === null && ` ${c.ind.unit}`}
                {!samePeriod && c.ind.trend && ` (${c.ind.trend.period.start}-${c.ind.trend.period.end})`}
              </span>
            ))}{" "}
            {u ?? ""} par décennie{allSignificant ? (trended.length > 1 ? ", tendances toutes significatives" : ", tendance significative") + " après correction de l'autocorrélation" : ""}.
            {comps
              .filter((c) => c.ind.headline === "normals" && c.ind.normals_comparison)
              .map((c) => {
                const n = c.ind.normals_comparison!;
                return (
                  <span key={c.variable.id}>
                    {" "}
                    {c.variable.code} (indice rare) : <b className="font-mono">{fmt1(n.first_value)} → {fmt1(n.second_value)}</b>{" "}
                    {c.ind.unit} par an entre {n.first.start}-{n.first.end} et {n.second.start}-{n.second.end}
                    {n.significant ? "" : ", écart non significatif"}.
                  </span>
                );
              })}
            {u !== null && maxSpread !== null && nStations > 1 && (
              <>
                {" "}
                Sur la période commune {period}, les pentes des {nStations} stations diffèrent au plus de{" "}
                <b className="font-mono">
                  {fmt(maxSpread)} {u}/déc.
                </b>
                {spreads.length > 1 ? ", quelle que soit la variable" : ""}.
              </>
            )}
          </p>
        )}
      </div>

      {(comps.length > 0 || matrix.rows.length > 0) && (
        <div className="space-y-2">
          <CompositeCards scale={scale} theme={theme.id} />
          <p className="text-xs text-[var(--muted)]">
            {ref0 ? `Barres : écart annuel à la moyenne ${ref0.start}-${ref0.end}` : `Barres : valeur annuelle, en ${u}`} ; pointillés :
            droite de Sen (absente pour un indice rare) ; gris : années non homogénéisées, hors tendance. Une carte ouvre la
            page détaillée.
          </p>
        </div>
      )}

      {u !== null && matrix.rows.length > 1 && (
        <div className="grid gap-10 lg:grid-cols-[1.15fr_1fr]">
          <div className="space-y-2 border-t border-[var(--rule)] pt-4">
            <h3 className="text-xl font-semibold">Les stations comparées</h3>
            <StationsOverlay data={over} variables={vars} initial={initial} unit={u} />
          </div>
          <div className="space-y-2 border-t border-[var(--rule)] pt-4">
            <h3 className="text-xl font-semibold">Tendance par station</h3>
            <TrendMatrix matrix={matrix} />
          </div>
        </div>
      )}

      {u !== null && Object.values(points).some((p) => p.length > 1) && (
        <div className="space-y-2 border-t border-[var(--rule)] pt-4">
          <h3 className="text-xl font-semibold">Carte des stations</h3>
          <StationsMap points={points} variables={vars} initial={initial} period={period} unit={u} />
        </div>
      )}
    </section>
  );
}
