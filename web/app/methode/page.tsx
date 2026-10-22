import type { Metadata } from "next";

import { CONFIDENCE_LABELS } from "@/lib/format";

export const metadata: Metadata = { title: "Méthode" };

const CONFIDENCE_RULES: Record<keyof typeof CONFIDENCE_LABELS, string> = {
  elevee: "Tendance significative, série homogénéisée, résultat cohérent avec une référence publiée.",
  moyenne: "Tendance significative, mais série non homogénéisée ou validation externe partielle.",
  faible: "Signal suggéré, non significatif ou sensible à la période retenue.",
  non_etabli: "Données insuffisantes, exploratoires ou de démonstration. Aucune conclusion.",
};

export default function MethodePage() {
  return (
    <article className="max-w-3xl space-y-8">
      <h1 className="text-3xl font-semibold tracking-tight">Méthode et limites</h1>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Chaîne de traitement</h2>
        <p>
          Un programme Python (l&apos;ETL), exécuté chaque mois par GitHub Actions, télécharge les données ouvertes,
          contrôle leur qualité, calcule les indicateurs et les tendances, puis publie des fichiers JSON. Chaque fichier
          est validé contre un schéma strict, d&apos;abord par l&apos;ETL, puis par le site au moment de sa
          construction. Un fichier non conforme bloque la publication.
        </p>
        <p>
          Le site ne fait aucun calcul scientifique. Il affiche les résultats produits par l&apos;ETL, avec leur
          source, leur licence, la version du script qui les a produits et leur date d&apos;extraction.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Tendances</h2>
        <p>
          La tendance est estimée par la pente de Sen (médiane des pentes entre toutes les paires de points), robuste
          aux valeurs extrêmes. Sa significativité est testée par le test de Mann-Kendall au seuil de 5 %.
        </p>
        <p className="rounded-md border border-[var(--rule)] p-3 text-sm">
          <strong>État actuel (phase 0) :</strong> test de Mann-Kendall classique, sans correction de
          l&apos;autocorrélation. Il surestime la significativité des séries autocorrélées. Il sera remplacé en phase 1
          par la variante de Hamed et Rao, et les deux versions seront comparées.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Niveaux de confiance</h2>
        <dl className="space-y-2">
          {(Object.keys(CONFIDENCE_RULES) as (keyof typeof CONFIDENCE_RULES)[]).map((k) => (
            <div key={k}>
              <dt className="font-medium">{CONFIDENCE_LABELS[k]}</dt>
              <dd className="text-sm text-[var(--muted)]">{CONFIDENCE_RULES[k]}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Validation</h2>
        <p>
          Chaque phase compare ses résultats à des valeurs publiées (ClimatHD de Météo-France, rapports Copernicus,
          séries NOAA). Une phase n&apos;est close que lorsque les écarts sont expliqués.
        </p>
      </section>
    </article>
  );
}
