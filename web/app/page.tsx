import Link from "next/link";

import IndicatorList from "@/components/IndicatorList";
import { getManifest, listIndicators } from "@/lib/data";
import { SCALE_LABELS } from "@/lib/format";
import { SCALES } from "@/lib/schema";

export default function Home() {
  const manifest = getManifest();
  const onlyDemo = manifest.indicators.length > 0 && manifest.indicators.every((e) => e.is_demo);

  return (
    <div className="space-y-12">
      <section className="max-w-2xl space-y-4">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Comment évolue le climat, ici et ailleurs ?</h1>
        <p className="text-[var(--muted)]">
          Chaque chiffre de ce site est calculé à partir de données ouvertes, avec sa méthode, sa source et son niveau
          de confiance. Les tendances sont testées statistiquement ; ce qui n&apos;est pas établi est présenté comme tel.
        </p>
        {onlyDemo && (
          <p className="text-sm">
            <strong>Phase 0 :</strong> seul un indicateur de démonstration est publié. Les premiers résultats réels
            (températures de Bordeaux-Mérignac) arrivent en phase 1.
          </p>
        )}
      </section>

      {SCALES.map((scale) => {
        const items = listIndicators(scale);
        const label = SCALE_LABELS[scale];
        return (
          <section key={scale} className="space-y-3">
            <div className="flex items-baseline justify-between gap-4">
              <h2 className="text-xl font-semibold">
                <Link href={`/${scale}`} className="hover:underline">
                  {label.name}
                </Link>
              </h2>
              <span className="text-xs text-[var(--muted)]">
                {items.length} indicateur{items.length > 1 ? "s" : ""}
              </span>
            </div>
            <p className="text-sm text-[var(--muted)]">{label.blurb}</p>
            {items.length > 0 ? (
              <IndicatorList items={items} />
            ) : (
              <p className="border-y border-[var(--rule)] py-3 text-sm text-[var(--muted)]">
                Aucun indicateur publié pour l&apos;instant ({label.phase}).
              </p>
            )}
          </section>
        );
      })}
    </div>
  );
}
