// Encart limites : tout ce qu'il faut pour juger de la solidité du chiffre affiché.
import { fmtDateTime } from "@/lib/format";
import type { Indicator } from "@/lib/schema";

export default function LimitsBox({ ind }: { ind: Indicator }) {
  const p = ind.provenance;
  return (
    <aside className="rounded-md border border-[var(--rule)] p-4 text-sm">
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">Limites et traçabilité</h2>
      <ul className="mb-4 list-disc space-y-1 pl-5">
        {ind.limitations.map((l) => (
          <li key={l}>{l}</li>
        ))}
      </ul>
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-xs">
        <dt className="text-[var(--muted)]">Source</dt>
        <dd>
          <a className="underline underline-offset-2" href={p.source_url} rel="noopener noreferrer" target="_blank">
            {p.source_name}
          </a>
        </dd>
        <dt className="text-[var(--muted)]">Licence</dt>
        <dd>{p.license}</dd>
        <dt className="text-[var(--muted)]">Série</dt>
        <dd>{p.homogenized ? "homogénéisée" : "brute, non homogénéisée"}</dd>
        {ind.reference_period && (
          <>
            <dt className="text-[var(--muted)]">Référence</dt>
            <dd>
              {ind.reference_period.start}–{ind.reference_period.end}
            </dd>
          </>
        )}
        <dt className="text-[var(--muted)]">Extraction</dt>
        <dd>{fmtDateTime(p.extracted_at)}</dd>
        <dt className="text-[var(--muted)]">Produit par</dt>
        <dd className="font-mono">
          {p.script} · ETL {p.etl_version}
        </dd>
      </dl>
    </aside>
  );
}
