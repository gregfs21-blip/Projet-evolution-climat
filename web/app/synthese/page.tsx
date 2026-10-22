import type { Metadata } from "next";

export const metadata: Metadata = { title: "Synthèse" };

export default function SynthesePage() {
  return (
    <article className="max-w-3xl space-y-4">
      <h1 className="text-3xl font-semibold tracking-tight">Synthèse</h1>
      <p className="text-[var(--muted)]">
        Les conclusions par échelle seront rédigées en phase 8, à partir des résultats calculés et avec un niveau de
        confiance pour chaque affirmation. Aucune conclusion n&apos;est publiée tant que les indicateurs qui la fondent
        ne sont pas validés.
      </p>
    </article>
  );
}
