// Accueil : les trois échelles côte à côte, sur la même référence.
// Le constat d'en-tête est composé à partir des JSON publiés : aucune conclusion n'est écrite à la main ici
// (la synthèse rédigée, avec son niveau de confiance par affirmation, relève de la phase P8).
import Image from "next/image";
import Link from "next/link";

import ClimateStripes from "@/components/ClimateStripes";
import ConfidenceBadge from "@/components/ConfidenceBadge";
import ConfidenceBars from "@/components/ConfidenceBars";
import FeaturedCard from "@/components/FeaturedCard";
import ScalesChart from "@/components/ScalesChart";
import { fmtSigned } from "@/lib/format";
import { featuredIndicators, publishedFindings, temperatureByScale } from "@/lib/home";

// Hébergée par le site socio-vote du même compte (photo Unsplash), tant qu'elle n'est pas versée dans web/public.
const PHOTO = "https://correlation-socio-vote.vercel.app/accueil/bourg.jpg";

const WHERE: Record<string, string> = { gironde: "en Gironde", france: "en France", monde: "à l'échelle du globe" };

export default function Home() {
  const t = temperatureByScale();
  const featured = featuredIndicators();
  const findings = publishedFindings();

  return (
    <div className="space-y-6">
      <section className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.05fr)] lg:gap-10">
        <figure className="relative -mx-4 -mt-5 h-[170px] overflow-hidden sm:-mx-6 sm:h-[240px] lg:order-last lg:mx-0 lg:mt-0 lg:h-auto lg:min-h-[380px] lg:rounded-2xl">
          <Image src={PHOTO} alt="Bourg de Saint-Émilion et ses vignes" fill priority sizes="(min-width: 1152px) 560px, (min-width: 1024px) 50vw, 100vw" className="object-cover" />
          <figcaption className="absolute inset-x-0 bottom-0 bg-linear-to-t from-[rgb(8_38_22/0.82)] to-transparent px-3 pt-7 pb-2.5 text-sm font-semibold text-white">
            Saint-Émilion, Gironde
          </figcaption>
        </figure>
        <div className="self-center">
          <p className="text-xs font-semibold tracking-[0.08em] text-[var(--muted)] uppercase">Gironde, France, monde · données ouvertes</p>
          <h1 className="mt-2 mb-3 text-[27px] leading-[1.1] font-bold tracking-tight sm:text-4xl lg:mb-4 lg:text-[44px]">
            Comment évolue le <span className="text-[var(--highlight)]">climat</span>, ici et ailleurs&nbsp;?
          </h1>
          <p className="mb-5 max-w-xl text-[15px] leading-relaxed lg:mb-6 lg:text-base">
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
          <div className="flex flex-col gap-3 sm:flex-row">
            <Link href="/gironde" className="inline-flex h-[50px] items-center justify-center rounded-full bg-[var(--primary)] px-6 font-semibold text-[var(--primary-ink)] transition-opacity hover:opacity-90">
              Explorer la Gironde
            </Link>
            <Link href="/methode" className="hidden h-[50px] items-center justify-center rounded-full border-[1.5px] border-[var(--rule)] bg-[var(--card)] px-6 font-semibold text-[var(--primary)] transition-colors hover:border-[var(--primary)] sm:inline-flex">
              Voir la méthode
            </Link>
          </div>
        </div>
      </section>

      <section aria-labelledby="titre-chiffres" className="space-y-2.5">
        <h2 id="titre-chiffres" className="text-xs font-semibold tracking-[0.08em] text-[var(--muted)] uppercase">
          Chiffres-clés
        </h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4 lg:gap-4">
          {featured.map((f) => (
            <FeaturedCard key={f.href} {...f} />
          ))}
        </div>
      </section>

      <section aria-label="Bandes climatiques" className="rounded-2xl bg-[var(--forest)] p-4 text-white sm:p-6">
        <ClimateStripes series={t.series} first={t.first} last={t.last} unit={t.unit} reference={t.reference} />
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
