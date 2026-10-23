// Bandeau de trois chiffres en tête de page : tendance, réchauffement cumulé, normales.
// Remplace KeyFigure + Normals dans le flux principal ; le détail statistique est replié plus bas.
import { fmt1, fmtPValue, fmtSigned, fmtSigned1 } from "@/lib/format";
import type { Indicator } from "@/lib/schema";

function Cell({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="border-[var(--rule)] px-4 py-3 not-last:border-b sm:not-last:border-r sm:not-last:border-b-0">
      <div className="text-xs uppercase tracking-wide text-[var(--muted)]">{label}</div>
      {children}
    </div>
  );
}

export default function KpiBand({ ind }: { ind: Indicator }) {
  const t = ind.trend;
  const u = ind.unit;
  const c = ind.headline === "normals" ? ind.normals_comparison : null;
  if (c) {
    // Indice rare (critère E9) : la pente de Sen est peu informative, l'écart entre normales est mis en avant.
    return (
      <div className="grid rounded-lg border border-[var(--rule)] bg-[var(--card)] sm:grid-cols-[1.25fr_1fr_1fr]">
        <Cell label="Écart entre normales">
          <div className="font-mono text-3xl tabular-nums">
            {fmtSigned1(c.difference)} <span className="text-sm text-[var(--muted)]">{u} / an</span>
          </div>
          <div className="font-mono text-xs text-[var(--muted)]">
            {c.significant ? "significatif" : "non significatif"} ({fmtPValue(c.p_value)}, Mann-Whitney)
          </div>
        </Cell>
        <Cell label="Normales">
          <div className="font-mono text-3xl tabular-nums">
            {fmt1(c.first_value)} → {fmt1(c.second_value)} <span className="text-sm text-[var(--muted)]">{u} / an</span>
          </div>
          <div className="font-mono text-xs text-[var(--muted)]">
            {c.first.start}-{c.first.end} → {c.second.start}-{c.second.end}
          </div>
        </Cell>
        <Cell label="Pourquoi pas une pente ?">
          <div className="mt-1 text-sm text-[var(--muted)]">
            Indice rare (moins de 5 jours par an en médiane sur 1961-1990) : beaucoup d&apos;années comptent peu ou pas
            de jours, une pente annuelle serait instable. Elle reste dans les détails statistiques.
          </div>
        </Cell>
      </div>
    );
  }
  if (!t) return <p className="text-sm text-[var(--muted)]">Pas de tendance calculée pour cet indicateur.</p>;
  const first = ind.normals[0];
  const last = ind.normals[ind.normals.length - 1];
  const years = t.period.end - t.period.start + 1;

  return (
    <div className="grid rounded-lg border border-[var(--rule)] bg-[var(--card)] sm:grid-cols-[1.25fr_1fr_1fr]">
      <Cell label={`Tendance ${t.period.start}-${t.period.end}`}>
        <div className="font-mono text-3xl tabular-nums">
          {fmtSigned(t.slope_per_decade)} <span className="text-sm text-[var(--muted)]">{u} / décennie</span>
        </div>
        <div className="font-mono text-xs text-[var(--muted)]">
          {t.slope_ci_low !== null && t.slope_ci_high !== null
            ? `IC ${Math.round((1 - t.alpha) * 100)} % ${fmtSigned(t.slope_ci_low)} à ${fmtSigned(t.slope_ci_high)} · `
            : ""}
          {t.significant ? "significative" : "non significative"} ({fmtPValue(t.p_value)})
        </div>
      </Cell>
      <Cell label="Évolution cumulée">
        <div className="font-mono text-3xl tabular-nums">
          {fmtSigned1(t.fitted_end - t.fitted_start)} <span className="text-sm text-[var(--muted)]">{u}</span>
        </div>
        <div className="text-xs text-[var(--muted)]">
          en {years} ans, le long de la droite de Sen
        </div>
      </Cell>
      <Cell label="Normales">
        {first && last && first !== last ? (
          <>
            <div className="font-mono text-3xl tabular-nums">
              {fmt1(first.value)} → {fmt1(last.value)} <span className="text-sm text-[var(--muted)]">{u}</span>
            </div>
            <div className="font-mono text-xs text-[var(--muted)]">
              {first.period.start}-{first.period.end} → {last.period.start}-{last.period.end} · {fmtSigned1(last.value - first.value)} {u}
            </div>
          </>
        ) : first ? (
          <>
            <div className="font-mono text-3xl tabular-nums">
              {fmt1(first.value)} <span className="text-sm text-[var(--muted)]">{u}</span>
            </div>
            <div className="font-mono text-xs text-[var(--muted)]">
              normale {first.period.start}-{first.period.end} (une seule publiée)
            </div>
          </>
        ) : (
          <div className="mt-2 text-sm text-[var(--muted)]">Aucune normale publiée pour cette série.</div>
        )}
      </Cell>
    </div>
  );
}
