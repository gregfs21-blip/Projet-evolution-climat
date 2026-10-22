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
      {ind.method_note && <p className="mb-4 text-xs">{ind.method_note}</p>}
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
      {ind.stations.length > 0 && (
        <div className="mt-4 overflow-x-auto">
          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">
            Séries Météo-France utilisées
          </h3>
          <table className="w-full min-w-[36rem] text-left text-xs">
            <thead className="text-[var(--muted)]">
              <tr className="border-b border-[var(--rule)]">
                <th className="py-1 pr-3 font-medium">Station</th>
                <th className="py-1 pr-3 font-medium">Série</th>
                <th className="py-1 pr-3 font-medium">Homogénéisée</th>
                <th className="py-1 pr-3 font-medium">Ampl. min. détectable</th>
                <th className="py-1 pr-3 font-medium">Ruptures corrigées</th>
                <th className="py-1 font-medium">Fichier du</th>
              </tr>
            </thead>
            <tbody className="font-mono">
              {ind.stations.map((st) => (
                <tr key={st.series_id ?? st.id} className="border-b border-[var(--rule)] align-top">
                  <td className="py-1 pr-3 font-sans">{st.name}</td>
                  <td className="py-1 pr-3">{st.series_id ?? "—"}</td>
                  <td className="py-1 pr-3">
                    {st.homogenized_period ? `${st.homogenized_period.start}–${st.homogenized_period.end}` : "—"}
                  </td>
                  <td className="py-1 pr-3">
                    {st.min_detectable_amplitude !== null ? `${st.min_detectable_amplitude.toLocaleString("fr-FR")} °C` : "—"}
                  </td>
                  <td className="py-1 pr-3">{st.homogenization_breaks.join(", ") || "aucune"}</td>
                  <td className="py-1">{st.file_produced ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </aside>
  );
}
