// Encart « résultats validés » : affiche le rapport de validation publié par l'ETL, sans le réinterpréter.
import { fmtDateTime, REPO_URL } from "@/lib/format";
import type { ValidationReport } from "@/lib/schema";

export default function ValidationBox({ reports }: { reports: ValidationReport[] }) {
  if (reports.length === 0) return null;
  return (
    <section className="space-y-4" aria-label="Validation">
      {reports.map((r) => {
        const counted = r.checks.filter((c) => c.kind === "critère");
        const ok = counted.filter((c) => c.satisfied);
        const other = r.checks.filter((c) => c.kind !== "critère");
        const tone = r.closure_ok
          ? "border-[var(--good)]/40 bg-[var(--good-soft)]"
          : "border-[var(--warm)]/40 bg-[var(--warm-soft)]";
        return (
          <div key={r.phase} className={`rounded-lg border px-4 py-3 text-sm ${tone}`}>
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <h2 className={`font-semibold ${r.closure_ok ? "text-[var(--good)]" : "text-[var(--warm)]"}`}>
                {r.closure_ok ? "✓" : "⚠"} Validation de la phase {r.phase.toUpperCase()} : {ok.length}/{counted.length}{" "}
                critères satisfaits
              </h2>
              <span className="text-xs text-[var(--muted)]">contrôlé le {fmtDateTime(r.generated_at)}</span>
            </div>
            <p className="mt-1">{r.verdict}</p>
            <details className="mt-2">
              <summary className="cursor-pointer text-xs font-medium">
                <span className="chevron">▸</span> Voir les critères et les mesures
              </summary>
              <ul className="mt-2 space-y-1.5">
                {counted.map((c) => (
                  <li key={c.name} className="text-xs">
                    <span className="font-medium">{c.name}</span> · {c.status}
                    <div className="font-mono text-[11px] break-words text-[var(--muted)]">{c.detail}</div>
                  </li>
                ))}
              </ul>
              {other.length > 0 && (
                <p className="mt-2 text-xs text-[var(--muted)]">
                  {other.length} contrôle{other.length > 1 ? "s" : ""} complémentaire{other.length > 1 ? "s" : ""} publié
                  {other.length > 1 ? "s" : ""} pour information, sans effet sur la clôture.
                </p>
              )}
              <p className="mt-2 text-xs">
                Analyse des écarts :{" "}
                <a
                  className="underline underline-offset-2"
                  href={`${REPO_URL}/blob/main/docs/validation-${r.phase}.md`}
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  docs/validation-{r.phase}.md
                </a>
              </p>
            </details>
          </div>
        );
      })}
    </section>
  );
}
