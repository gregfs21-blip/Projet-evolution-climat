// P11 — localités la plus chaude et la plus froide à l'instant t (décisions D-AJ à D-AL, docs/phases.md).
// Seule page du site rendue côté serveur hors déploiement (exception D-AJ) : Vercel la régénère au plus toutes les
// 10 minutes à partir du fichier METAR mondial de la NOAA. Rien n'est stocké, aucune tendance n'est calculée.
// Si la source ne répond pas pendant une régénération, l'erreur est levée : Vercel garde la dernière page réussie,
// dont l'heure de lecture est affichée, et le bandeau signale qu'elle n'a pas été rafraîchie (critère Q5).
import type { Metadata } from "next";
import Link from "next/link";
import { gunzipSync } from "node:zlib";

import StaleBanner from "@/components/StaleBanner";
import { fmtDateTime } from "@/lib/format";
import {
  EXCLUSIONS,
  MAX_AGE_MIN,
  REFERENCE_ID,
  snapshot,
  stationIndex,
  T_MAX,
  T_MIN,
  TOP,
  type Observation,
  type Snapshot,
} from "@/lib/metar";

export const revalidate = 600;
export const metadata: Metadata = { title: "Instantané" };

const METAR_URL = "https://aviationweather.gov/data/cache/metars.cache.csv.gz";
const STATIONS_URL = "https://aviationweather.gov/data/cache/stations.cache.json.gz";
const SOURCE_PAGE = "https://aviationweather.gov/data/api/";

function text(buf: ArrayBuffer): string {
  const b = Buffer.from(buf);
  // Fichiers gzip ; si un intermédiaire les a déjà décompressés, ils sont lus tels quels.
  return (b[0] === 0x1f && b[1] === 0x8b ? gunzipSync(b) : b).toString("utf8");
}

async function load(): Promise<Snapshot> {
  const [m, s] = await Promise.all([
    fetch(METAR_URL, { next: { revalidate: 600 } }),
    fetch(STATIONS_URL, { next: { revalidate: 86400 } }),
  ]);
  if (!m.ok) throw new Error(`METAR : HTTP ${m.status}`);
  if (!s.ok) throw new Error(`stations : HTTP ${s.status}`);
  const stations = stationIndex(JSON.parse(text(await s.arrayBuffer())));
  return snapshot(text(await m.arrayBuffer()), stations, new Date(), m.headers.get("last-modified"));
}

const region = new Intl.DisplayNames(["fr"], { type: "region" });
function country(code: string | null): string {
  if (!code) return "pays non renseigné";
  try {
    return region.of(code) ?? code;
  } catch {
    return code;
  }
}

const nf = (v: number, d = 1) =>
  v.toLocaleString("fr-FR", { minimumFractionDigits: v % 1 === 0 ? 0 : d, maximumFractionDigits: d });
const utc = (iso: string) =>
  new Intl.DateTimeFormat("fr-FR", { hour: "2-digit", minute: "2-digit", timeZone: "UTC" }).format(new Date(iso));

function Station({ o, rank, tone }: { o: Observation; rank?: number; tone: string }) {
  return (
    <li className="border-b border-[var(--rule)] py-3">
      <div className="flex items-baseline justify-between gap-3">
        <div className="min-w-0">
          <div className="font-medium">
            {rank !== undefined && <span className="mr-2 text-xs text-[var(--muted)]">{rank}.</span>}
            {o.name}
          </div>
          <div className="text-xs text-[var(--muted)]">
            {country(o.country)} · {o.id}
            {o.elev !== null ? ` · ${o.elev.toLocaleString("fr-FR")} m` : ""} · mesure de {utc(o.time)} UTC (il y a {o.ageMin} min)
          </div>
        </div>
        <div className={`shrink-0 text-2xl font-semibold tabular-nums ${tone}`}>{nf(o.temp)} °C</div>
      </div>
      <p className="mt-1 font-mono text-[11px] break-words text-[var(--muted)]">{o.raw}</p>
    </li>
  );
}

function Unavailable({ error }: { error: string }) {
  return (
    <p className="rounded-lg border border-[var(--warm)] px-4 py-3 text-sm">
      La source METAR de la NOAA n&apos;a pas répondu lors de la construction de cette page ({error}). Aucune valeur
      n&apos;est affichée plutôt qu&apos;une valeur ancienne ; la page sera régénérée à la prochaine visite après 10 minutes.
    </p>
  );
}

export default async function InstantanePage() {
  let snap: Snapshot | null = null;
  let error: string | null = null;
  try {
    snap = await load();
  } catch (e) {
    // Pendant le déploiement, une panne de la source ne doit pas bloquer la construction du site : page d'attente.
    // Pendant une régénération, l'erreur est relancée pour que Vercel garde la dernière page réussie.
    if (process.env.NEXT_PHASE !== "phase-production-build") throw e;
    error = e instanceof Error ? e.message : String(e);
  }

  return (
    <article className="max-w-3xl space-y-8">
      <header className="space-y-3">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Instantané : les extrêmes du moment</h1>
        <p className="leading-relaxed">
          Les aérodromes où il fait le plus chaud et le plus froid en ce moment, d&apos;après les observations METAR de
          plusieurs milliers d&apos;aérodromes dans le monde. C&apos;est une photographie de l&apos;instant, pas une
          tendance climatique : rien n&apos;est conservé, et cette page n&apos;entre pas dans la synthèse.
        </p>
        {snap && (
          <p className="text-sm text-[var(--muted)]">
            Lu le {fmtDateTime(snap.readAt)} (heure de Paris), parmi les <b>{snap.kept.toLocaleString("fr-FR")}</b> stations
            retenues sur {snap.total.toLocaleString("fr-FR")}. Page régénérée au plus toutes les 10 minutes.
          </p>
        )}
        {snap && <StaleBanner readAt={snap.readAt} />}
      </header>

      {error && <Unavailable error={error} />}

      {snap && (
        <>
          <div className="grid gap-8 sm:grid-cols-2">
            <section>
              <h2 className="mb-1 text-lg font-semibold">Les {TOP} plus chaudes</h2>
              <ol>
                {snap.hottest.map((o, i) => (
                  <Station key={o.id} o={o} rank={i + 1} tone="text-[var(--warm)]" />
                ))}
              </ol>
            </section>
            <section>
              <h2 className="mb-1 text-lg font-semibold">Les {TOP} plus froides</h2>
              <ol>
                {snap.coldest.map((o, i) => (
                  <Station key={o.id} o={o} rank={i + 1} tone="text-[var(--cold)]" />
                ))}
              </ol>
            </section>
          </div>

          <section>
            <h2 className="mb-1 text-lg font-semibold">Repère : Bordeaux-Mérignac</h2>
            {snap.reference ? (
              <ul>
                <Station o={snap.reference} tone="" />
              </ul>
            ) : (
              <p className="text-sm text-[var(--muted)]">
                {REFERENCE_ID} non affiché : {snap.referenceExclusion}.
              </p>
            )}
          </section>
        </>
      )}

      <details className="rounded-lg border border-[var(--rule)] px-4 py-3 text-sm">
        <summary className="cursor-pointer font-medium">
          <span className="chevron">▸</span> Contrôle qualité, limites et source
        </summary>
        <div className="mt-3 space-y-3 leading-relaxed">
          <p>
            Une observation est écartée, jamais corrigée, si elle date de plus de {MAX_AGE_MIN / 60} heures, si sa
            température sort de {T_MIN} à +{T_MAX} °C, si son point de rosée dépasse sa température, si la station signale
            une maintenance, si la température du fichier diffère de celle du message METAR brut, ou si la station est
            inconnue. Une station n&apos;est comptée qu&apos;une fois, avec sa mesure la plus récente.
          </p>
          {snap && (
            <ul className="space-y-0.5 text-xs text-[var(--muted)]">
              {EXCLUSIONS.map((e) => (
                <li key={e}>
                  {e} : {snap.excluded[e].toLocaleString("fr-FR")} station{snap.excluded[e] > 1 ? "s" : ""} écartée
                  {snap.excluded[e] > 1 ? "s" : ""}
                </li>
              ))}
            </ul>
          )}
          <p>
            Ce sont les extrêmes <b>du réseau METAR</b>, pas ceux de la Terre. Le réseau couvre les aérodromes : il est
            dense en Europe et en Amérique du Nord, clairsemé dans les déserts, et ne contient ni l&apos;intérieur de
            l&apos;Antarctique (Vostok, plateau), où l&apos;on mesure les froids les plus intenses ; le pôle Sud y
            figure seulement quand son dernier message a moins d&apos;une heure et demie. Les mesures sont celles des
            stations, à leur altitude : un aérodrome d&apos;altitude paraît plus froid sans que la masse d&apos;air le
            soit.
          </p>
          <p className="text-xs text-[var(--muted)]">
            Source :{" "}
            <a className="underline underline-offset-2" href={SOURCE_PAGE} rel="noopener noreferrer" target="_blank">
              NOAA Aviation Weather Center
            </a>{" "}
            (fichiers METAR et stations, domaine public)
            {snap?.fileModified ? `, fichier METAR du ${fmtDateTime(snap.fileModified)}` : ""}. Code :{" "}
            <code>web/lib/metar.ts</code>. Cadrage : phase P11 (
            <Link href="/methode" className="underline underline-offset-2">
              méthode
            </Link>
            ).
          </p>
        </div>
      </details>
    </article>
  );
}
