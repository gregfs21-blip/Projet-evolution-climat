// « Ce qui fonde ce niveau de confiance » : la justification du badge, calculée depuis le JSON publié
// et le rapport de validation de l'échelle. Rien n'est rédigé à la main ; un point défavorable s'affiche tel quel.
import ConfidenceBadge from "./ConfidenceBadge";
import { establishedBreaks } from "./Breakpoints";
import { fmtPValue } from "@/lib/format";
import type { Indicator, ValidationReport } from "@/lib/schema";

type Point = { ok: boolean; title: string; text: string };

function points(ind: Indicator, reports: ValidationReport[]): Point[] {
  const out: Point[] = [];
  const t = ind.trend;
  if (t) {
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
  if (ind.alt_trends.length > 0 && t) {
    const agree = ind.alt_trends.filter((a) => Math.sign(a.slope_per_decade) === Math.sign(t.slope_per_decade) && a.significant === t.significant);
    out.push({
      ok: agree.length === ind.alt_trends.length,
      title: "Autres périodes",
      text:
        agree.length === ind.alt_trends.length
          ? `Même signe et même conclusion sur ${ind.alt_trends.length === 1 ? "l'autre période calculée" : `les ${ind.alt_trends.length} autres périodes calculées`} (${ind.alt_trends.map((a) => `${a.period.start}-${a.period.end}`).join(", ")}).`
          : `${ind.alt_trends.length - agree.length} période${ind.alt_trends.length - agree.length > 1 ? "s" : ""} sur ${ind.alt_trends.length} ${ind.alt_trends.length - agree.length > 1 ? "aboutissent" : "aboutit"} à une conclusion différente (voir les détails statistiques).`,
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
