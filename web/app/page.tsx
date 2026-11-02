// Accueil : les trois échelles côte à côte, sur la même référence.
// Le constat d'en-tête est composé à partir des JSON publiés : aucune conclusion n'est écrite à la main ici
// (la synthèse rédigée, avec son niveau de confiance par affirmation, relève de la phase P8).
import Link from "next/link";

import ClimateStripes from "@/components/ClimateStripes";
import ConfidenceBadge from "@/components/ConfidenceBadge";
import ConfidenceBars from "@/components/ConfidenceBars";
import FeaturedCard from "@/components/FeaturedCard";
import ScalesChart from "@/components/ScalesChart";
import { fmtSigned } from "@/lib/format";
import { featuredIndicators, publishedFindings, temperatureByScale } from "@/lib/home";

const WHERE: Record<string, string> = { gironde: "en Gironde", france: "en France", monde: "à l'échelle du globe" };

export default function Home() {
  const t = temperatureByScale();
  const featured = featuredIndicators();
  const findings = publishedFindings();

  return (
    <div className="space-y-6">
      <section className="rounded-3xl bg-[#0b2748] px-4 pt-6 pb-14 text-white sm:px-7 sm:pt-8">
        <div className="space-y-3">
          <h1 className="text-3xl leading-tight font-semibold tracking-tight sm:text-[2.6rem]">Comment évolue le climat, ici et ailleurs&nbsp;?</h1>
          <p className="max-w-3xl text-base leading-relaxed text-white/85">
            Sur la même période {t.period}, la température moyenne évolue de{" "}
            {t.series.map((s, i) => (
              <span key={s.key}>
                {i > 0 && (i === t.series.length - 1 ? " et " : ", ")}
                <b className="font-semibold whitespace-nowrap tabular-nums">
                  {fmtSigned(s.trend.slope)} {t.unit}
                </b>{" "}
                par décennie {WHERE[s.key]}
                {!s.trend.significant && " (non significatif)"}
              </span>
            ))}
            . Chaque chiffre vient de données ouvertes, avec sa méthode, sa source et son niveau de confiance.
          </p>
        </div>
        <div className="mt-6">
          <ClimateStripes series={t.series} first={t.first} last={t.last} unit={t.unit} reference={t.reference} />
        </div>
      </section>

      <section aria-label="Chiffres-clés" className="relative z-10 -mt-14 grid gap-3 px-2 sm:grid-cols-2 sm:px-5 xl:grid-cols-4">
        {featured.map((f) => (
          <FeaturedCard key={f.href} {...f} />
        ))}
      </section>

      <section className="card space-y-3 p-4 sm:p-6">
        <h2 className="text-lg font-semibold tracking-tight">Écart de température par échelle</h2>
        <ScalesChart series={t.series} first={t.first} last={t.last} unit={t.unit} reference={t.reference} period={t.period} />
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
        <section className="card space-y-3 p-4 sm:p-6">
          <h2 className="text-lg font-semibold tracking-tight">Ce qui est établi, et ce qui ne l&apos;est pas</h2>
          <ConfidenceBars />
        </section>
        <section className="card space-y-3 p-4 sm:p-6">
          <h2 className="text-lg font-semibold tracking-tight">Trois constats publiés</h2>
          <ul className="divide-y divide-[var(--rule)]">
            {findings.map(({ ind, href }) => (
              <li key={href} className="space-y-1.5 py-3 first:pt-0 last:pb-0">
                <ConfidenceBadge level={ind.confidence} />
                <p className="text-sm leading-relaxed">
                  <Link href={href} className="underline-offset-2 hover:underline">
                    {ind.finding}
                  </Link>
                </p>
              </li>
            ))}
          </ul>
          <p className="text-xs text-[var(--muted)]">
            Constats par indicateur, repris tels quels. La synthèse par échelle reste à écrire (phase P8).
          </p>
        </section>
      </div>
    </div>
  );
}
