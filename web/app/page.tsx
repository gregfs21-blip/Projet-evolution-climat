import Link from "next/link";

import CompositeCards from "@/components/CompositeCards";
import IndicatorList from "@/components/IndicatorList";
import { groupedIndicators, listIndicators } from "@/lib/data";
import { composites, themes } from "@/lib/family";
import { SCALE_LABELS } from "@/lib/format";
import { SCALES } from "@/lib/schema";

export default function Home() {
  const published = SCALES.filter((s) => listIndicators(s).length > 0);
  const upcoming = SCALES.filter((s) => listIndicators(s).length === 0);

  return (
    <div className="space-y-12">
      <section className="max-w-2xl space-y-3">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Comment évolue le climat, ici et ailleurs ?</h1>
        <p className="text-[var(--muted)]">
          Chaque chiffre est calculé à partir de données ouvertes, avec sa méthode, sa source et son niveau de
          confiance. Les tendances sont testées statistiquement ; ce qui n&apos;est pas établi est présenté comme tel.
        </p>
      </section>

      {published.map((scale) => {
        const label = SCALE_LABELS[scale];
        const n = listIndicators(scale).length;
        const ths = themes(scale);
        const synth = groupedIndicators(scale).find(([g]) => g.startsWith("Synthèse"));
        return (
          <section key={scale} className="space-y-3">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <h2 className="text-xl font-semibold">
                <Link href={`/${scale}`} className="hover:underline">
                  {label.name}
                </Link>
              </h2>
              <Link href={`/${scale}`} className="text-sm text-[var(--muted)] hover:underline">
                {n} indicateur{n > 1 ? "s" : ""}, stations comparées →
              </Link>
            </div>
            {ths.length > 0 ? (
              ths.filter((t) => composites(scale, t.id).length > 0).map((t) => (
                <div key={t.id} className="space-y-2">
                  {ths.length > 1 && <h3 className="text-sm font-medium text-[var(--muted)]">{t.label}</h3>}
                  <CompositeCards scale={scale} theme={t.id} />
                </div>
              ))
            ) : (
              <IndicatorList items={synth ? synth[1] : listIndicators(scale)} />
            )}
          </section>
        );
      })}

      {upcoming.length > 0 && (
        <section className="space-y-2 border-t border-[var(--rule)] pt-4">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--muted)]">À venir</h2>
          <ul className="space-y-1 text-sm">
            {upcoming.map((scale) => (
              <li key={scale}>
                <span className="font-medium">{SCALE_LABELS[scale].name}</span>{" "}
                <span className="text-[var(--muted)]">
                  ({SCALE_LABELS[scale].phase}) : {SCALE_LABELS[scale].blurb}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
