// Synthèse (P8) : affirmations par échelle, générées par l'ETL (etl/synthese.py) à partir des indicateurs publiés.
// Le site n'écrit aucun chiffre : il affiche le texte rendu par l'ETL, sa confiance (règle S1) et ses indicateurs.
import type { Metadata } from "next";
import Link from "next/link";

import ConfidenceBadge from "@/components/ConfidenceBadge";
import ValidationBox from "@/components/ValidationBox";
import { getSynthesis, getValidation } from "@/lib/data";
import { fmtDateTime } from "@/lib/format";
import type { Claim, Synthesis } from "@/lib/schema";

export const metadata: Metadata = { title: "Synthèse" };

const KIND: Record<Claim["kind"], { label: string; tone: string } | null> = {
  signal: null,
  absence: null,
  comparaison: { label: "Comparaison", tone: "border-[var(--rule)] text-[var(--muted)]" },
  acceleration: { label: "Accélération", tone: "border-[var(--rule)] text-[var(--muted)]" },
  information: { label: "Information", tone: "border-dashed border-[var(--accent)] text-[var(--accent)]" },
  contexte: { label: "Contexte externe", tone: "border-dashed border-[var(--muted)] text-[var(--muted)]" },
  lacune: { label: "Lacune", tone: "border-[var(--warm)] text-[var(--warm)]" },
};

function ClaimItem({ c }: { c: Claim }) {
  const k = KIND[c.kind];
  return (
    <li className="space-y-1.5 border-t border-[var(--rule)] py-3 first:border-t-0">
      <div className="flex flex-wrap items-center gap-2">
        {c.confidence && <ConfidenceBadge level={c.confidence} />}
        {k && (
          <span className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-medium ${k.tone}`}>{k.label}</span>
        )}
      </div>
      <p className="leading-relaxed">{c.text}</p>
      {c.problem && (
        <p className="rounded border border-[var(--warm)]/40 bg-[var(--warm-soft)] px-2 py-1 text-xs text-[var(--warm)]">
          ⚠ Affirmation à revoir : {c.problem}
        </p>
      )}
      {(c.indicators.length > 0 || c.source) && (
        <p className="text-xs text-[var(--muted)]">
          {c.indicators.length > 0 && (
            <>
              Fondée sur :{" "}
              {c.indicators.map((i, n) => (
                <span key={i.id}>
                  {n > 0 && " · "}
                  <Link href={`/${i.scale}/${i.id}`} className="underline underline-offset-2 hover:text-[var(--ink)]">
                    {i.title}
                  </Link>
                </span>
              ))}
            </>
          )}
          {c.source && (
            <>
              {c.indicators.length > 0 && " — "}Source :{" "}
              <a href={c.source.url} className="underline underline-offset-2 hover:text-[var(--ink)]" rel="noreferrer">
                {c.source.label}
              </a>
            </>
          )}
        </p>
      )}
    </li>
  );
}

function Section({ s }: { s: Synthesis["sections"][number] }) {
  return (
    <section id={s.id} className="scroll-mt-20 space-y-4">
      <h2 className="text-2xl font-semibold tracking-tight">{s.title}</h2>
      {s.intro && <p className="max-w-3xl text-sm text-[var(--muted)]">{s.intro}</p>}
      {s.pending && (
        <p className="max-w-3xl border-y border-[var(--rule)] py-3 text-sm text-[var(--muted)]">{s.pending}</p>
      )}
      {s.groups.map((g) => (
        <div key={g.title} className="max-w-3xl">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">{g.title}</h3>
          <ul>
            {g.claims.map((c) => (
              <ClaimItem key={c.id} c={c} />
            ))}
          </ul>
        </div>
      ))}
      {s.conclusion && (
        <div className="max-w-3xl rounded-lg border border-[var(--rule)] px-4 py-3">
          <h3 className="mb-1 text-sm font-semibold">En résumé</h3>
          <p className="leading-relaxed">{s.conclusion}</p>
        </div>
      )}
    </section>
  );
}

export default function SynthesePage() {
  const syn = getSynthesis();
  const report = getValidation("p8");
  if (!syn) {
    return (
      <article className="max-w-3xl space-y-4">
        <h1 className="text-3xl font-semibold tracking-tight">Synthèse</h1>
        <p className="text-[var(--muted)]">La synthèse n&apos;est pas encore générée.</p>
      </article>
    );
  }
  return (
    <div className="space-y-12">
      <header className="max-w-3xl space-y-3">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Synthèse</h1>
        <p className="text-sm leading-relaxed text-[var(--muted)]">
          Chaque affirmation est générée à partir des indicateurs publiés : aucun chiffre n&apos;est écrit à la main, et
          la synthèse suit les mises à jour. Sa confiance est celle du plus faible des indicateurs qui la fondent ; un
          accord entre jeux de données qui partagent leurs mesures ne la relève pas. Une tendance « non détectée » ne veut
          pas dire « stable ». L&apos;étude décrit le climat observé et n&apos;attribue pas de cause.
        </p>
        <nav aria-label="Sections" className="flex flex-wrap gap-x-4 gap-y-1 text-sm">
          {syn.sections.map((s) => (
            <a key={s.id} href={`#${s.id}`} className="text-[var(--muted)] underline-offset-2 hover:text-[var(--ink)] hover:underline">
              {s.title}
            </a>
          ))}
        </nav>
        <p className="text-xs text-[var(--muted)]">Générée le {fmtDateTime(syn.generated_at)}.</p>
      </header>
      {syn.sections.map((s) => (
        <Section key={s.id} s={s} />
      ))}
      {report && <ValidationBox reports={[report]} />}
    </div>
  );
}
