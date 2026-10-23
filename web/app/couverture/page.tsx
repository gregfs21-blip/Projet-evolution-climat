// Couverture : chaque paramètre des instructions du projet, à chaque échelle, avec son état réel.
// Les trous restent visibles : un paramètre sans donnée ouverte est dit tel quel, pas masqué.
import type { Metadata } from "next";
import Link from "next/link";

import { getCoverage } from "@/lib/data";
import { CONFIDENCE_LABELS, SCALE_LABELS } from "@/lib/format";
import { SCALES, type CoverageCell } from "@/lib/schema";

export const metadata: Metadata = { title: "Couverture" };

const STATUS: Record<CoverageCell["status"], { label: string; tone: string }> = {
  publie: { label: "Publié", tone: "border-[var(--good)] bg-[var(--good-soft)] text-[var(--good)]" },
  prevu: { label: "Prévu", tone: "border-[var(--rule)] text-[var(--muted)]" },
  "sans-donnee": { label: "Sans donnée ouverte", tone: "border-[var(--warm)] bg-[var(--warm-soft)] text-[var(--warm)]" },
  instantane: { label: "Instantané, hors tendance", tone: "border-dashed border-[var(--accent)] text-[var(--accent)]" },
};

function Cell({ c }: { c: CoverageCell | undefined }) {
  if (!c) return <td className="px-2 py-2 text-center text-xs text-[var(--muted)]">—</td>;
  const s = STATUS[c.status];
  return (
    <td className="px-2 py-2 align-top">
      <span className={`inline-block rounded-full border px-2 py-0.5 text-xs font-medium ${s.tone}`}>{s.label}</span>
      {c.indicators.length > 0 && (
        <ul className="mt-1 space-y-0.5 text-xs">
          {c.indicators.slice(0, 4).map((i) => (
            <li key={i.id}>
              <Link href={`/${c.scale}/${i.id}`} className="underline underline-offset-2">
                {i.title}
              </Link>{" "}
              <span className="text-[var(--muted)]">· {CONFIDENCE_LABELS[i.confidence].toLowerCase()}</span>
            </li>
          ))}
          {c.indicators.length > 4 && <li className="text-[var(--muted)]">et {c.indicators.length - 4} autres</li>}
        </ul>
      )}
      {c.indicators.length === 0 && c.source && <div className="mt-1 text-xs text-[var(--muted)]">{c.source}</div>}
      {c.note && <div className="mt-1 text-xs italic text-[var(--muted)]">{c.note}</div>}
    </td>
  );
}

export default function CouverturePage() {
  const cov = getCoverage();
  if (!cov) return <p className="text-sm text-[var(--muted)]">Couverture non publiée.</p>;
  const cells = cov.parameters.flatMap((p) => p.cells);
  const count = (s: CoverageCell["status"]) => cells.filter((c) => c.status === s).length;
  return (
    <article className="space-y-6">
      <header className="max-w-3xl space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">Couverture</h1>
        <p className="text-[var(--muted)]">
          Chaque paramètre du projet, à chaque échelle. « Publié » est calculé à partir des indicateurs effectivement en
          ligne, jamais déclaré à la main.
        </p>
        <p className="text-lg">
          <b className="font-mono">{count("publie")}</b> case{count("publie") > 1 ? "s" : ""} publiée{count("publie") > 1 ? "s" : ""} sur{" "}
          <b className="font-mono">{cells.length}</b> · {count("prevu")} prévue{count("prevu") > 1 ? "s" : ""} ·{" "}
          {count("sans-donnee")} sans donnée ouverte · {count("instantane")} instantanée{count("instantane") > 1 ? "s" : ""}
        </p>
      </header>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[44rem] border-collapse text-left text-sm">
          <thead className="text-xs uppercase tracking-wide text-[var(--muted)]">
            <tr className="border-b border-[var(--rule)]">
              <th className="py-2 pr-3 font-medium">Paramètre</th>
              {SCALES.map((s) => (
                <th key={s} className="px-2 py-2 font-medium">
                  {SCALE_LABELS[s].name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {cov.parameters.map((p) => (
              <tr key={p.id} className="border-b border-[var(--rule)]">
                <th scope="row" className="py-2 pr-3 align-top font-medium">
                  {p.label}
                </th>
                {SCALES.map((s) => (
                  <Cell key={s} c={p.cells.find((c) => c.scale === s)} />
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  );
}
