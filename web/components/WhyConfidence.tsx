// « Ce qui fonde ce niveau de confiance » : la justification du badge, calculée depuis le JSON publié
// et le rapport de validation de l'échelle. Rien n'est rédigé à la main ; un point défavorable s'affiche tel quel.
import ConfidenceBadge from "./ConfidenceBadge";
import { establishedBreaks } from "./Breakpoints";
import { fmtPValue } from "@/lib/format";
import type { Indicator, ValidationReport } from "@/lib/schema";

type Point = { ok: boolean; title: string; text: string };

const CONTROL_A = "Contrôle A";
const B_ON_A = "Série corrigée sur la période du contrôle A";

function points(ind: Indicator, reports: ValidationReport[]): Point[] {
  const out: Point[] = [];
  const t = ind.trend;
  const c = ind.headline === "normals" ? ind.normals_comparison : null;
  if (c) {
    out.push({
      ok: c.significant,
      title: c.significant ? "Écart entre normales significatif" : "Écart entre normales non significatif",
      text: `${c.method} (${fmtPValue(c.p_value)}). Indice rare : confiance au plus « moyenne » (critère E9).`,
    });
  } else if (t) {
    out.push({
      ok: t.significant,
      title: t.significant ? "Tendance significative" : "Tendance non significative",
      text: `Au seuil de ${Math.round(t.alpha * 100)} %, après correction de l'autocorrélation (${fmtPValue(t.p_value)}).`,
    });
    if (t.p_value_classical !== null) {
      const same = t.p_value_classical < t.alpha === t.significant;
      out.push({
        ok: same,
        title: same ? "Conclusion stable" : "Conclusion sensible au test",
        text: same
          ? "Le test classique, sans correction, aboutit à la même conclusion."
          : "Le test classique, sans correction, conclut différemment : la correction compte ici.",
      });
    }
  }
  // Contrôle sur données brutes (P2a, critère E7) : même signe et intervalles de confiance qui se recouvrent.
  const a = ind.alt_trends.find((x) => x.label.startsWith(CONTROL_A));
  const b = ind.alt_trends.find((x) => x.label.startsWith(B_ON_A));
  if (a && b && a.slope_ci_low !== null && a.slope_ci_high !== null && b.slope_ci_low !== null && b.slope_ci_high !== null) {
    const ok =
      Math.sign(a.slope_per_decade) === Math.sign(b.slope_per_decade) &&
      a.slope_ci_low <= b.slope_ci_high &&
      b.slope_ci_low <= a.slope_ci_high;
    out.push({
      ok,
      title: ok ? "Contrôle brut concordant" : "Contrôle brut discordant",
      text: `Sur ${a.period.start}-${a.period.end}, après la dernière rupture connue, la série brute donne ${a.slope_per_decade.toLocaleString("fr-FR", { signDisplay: "always", maximumFractionDigits: 2 })} contre ${b.slope_per_decade.toLocaleString("fr-FR", { signDisplay: "always", maximumFractionDigits: 2 })} ${ind.unit}/déc. pour la série corrigée.`,
    });
  }
  const periods = ind.alt_trends.filter((x) => !x.label.startsWith(CONTROL_A) && !x.label.startsWith(B_ON_A));
  if (periods.length > 0 && t && !c) {
    const agree = periods.filter((x) => Math.sign(x.slope_per_decade) === Math.sign(t.slope_per_decade) && x.significant === t.significant);
    const n = periods.length;
    const bad = n - agree.length;
    out.push({
      ok: bad === 0,
      title: "Autres périodes",
      text:
        bad === 0
          ? `Même signe et même conclusion sur ${n === 1 ? "l'autre période calculée" : `les ${n} autres périodes calculées`} (${periods.map((x) => `${x.period.start}-${x.period.end}`).join(", ")}).`
          : `${bad} période${bad > 1 ? "s" : ""} sur ${n} ${bad > 1 ? "aboutissent" : "aboutit"} à une conclusion différente (voir les détails statistiques).`,
    });
  }
  const est = establishedBreaks(ind);
  out.push({
    ok: est.length === 0,
    title: est.length === 0 ? "Pas de saut brusque" : "Rupture établie",
    text:
      ind.breakpoints.length === 0
        ? "Aucune rupture détectée (test de Pettitt)."
        : est.length === 0
          ? `${ind.breakpoints.length === 1 ? "1 rupture détectée, non établie : elle disparaît" : `${ind.breakpoints.length} ruptures détectées, aucune établie : chacune disparaît`} après retrait de la tendance ou coïncide avec une correction d'homogénéité.`
          : `${est.length > 1 ? "Ruptures" : "Rupture"} en ${est.join(", ")} : à interpréter avant toute conclusion sur la tendance.`,
  });
  // Seuls les rapports qui couvrent explicitement cet indicateur comptent.
  for (const r of reports.filter((x) => x.indicators.includes(ind.id))) {
    const counted = r.checks.filter((c) => c.kind === "critère");
    out.push({
      ok: r.closure_ok,
      title: `Validation ${r.phase.toUpperCase()}`,
      text: `${counted.filter((c) => c.satisfied).length}/${counted.length} critères de validation de la phase satisfaits, écarts acceptés compris (détail sur la page de l'échelle).`,
    });
  }
  return out;
}

export default function WhyConfidence({ ind, reports }: { ind: Indicator; reports: ValidationReport[] }) {
  const pts = points(ind, reports);
  return (
    <section aria-label="Niveau de confiance" className="rounded-lg border border-[var(--rule)] bg-[var(--card)] p-4">
      <div className="mb-3 flex flex-wrap items-center gap-3">
        <ConfidenceBadge level={ind.confidence} />
        <h2 className="text-sm font-semibold">Ce qui fonde ce niveau</h2>
      </div>
      <ul className="grid gap-x-6 gap-y-3 text-sm sm:grid-cols-2">
        {pts.map((p) => (
          <li key={p.title} className="flex gap-2">
            <span aria-hidden className={p.ok ? "text-[var(--good)]" : "text-[var(--warm)]"}>
              {p.ok ? "✓" : "⚠"}
            </span>
            <span>
              <b className="font-medium">{p.title}.</b> <span className="text-[var(--muted)]">{p.text}</span>
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
}
