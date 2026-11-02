// Page d'une échelle : ses boutons de thème et un seul thème à la fois.
// Tout vient du manifeste : un nouveau thème publié par l'ETL ajoute son bouton et sa page, sans code ici.
import DepartmentsMap from "./DepartmentsMap";
import IndicatorList from "./IndicatorList";
import ThemeSection from "./ThemeSection";
import ThemeTabs from "./ThemeTabs";
import ValidationBox from "./ValidationBox";
import { getDepartmentMap, getValidation } from "@/lib/data";
import { nonMembers, orderedThemes, scaleSections, themeEntries, VALIDATION_SECTION } from "@/lib/family";
import { SCALE_LABELS } from "@/lib/format";
import type { Scale } from "@/lib/schema";

// Cartes départementales : rattachées au thème qu'elles illustrent (par échelle puis par thème).
const THEME_MAPS: Partial<Record<Scale, Record<string, string>>> = {
  france: { temperature: "carte-departements", precipitations: "carte-departements-pluie" },
};

/** `active` absent : page d'accueil de l'échelle, qui ouvre le premier thème. */
export default function ScaleView({ scale, active }: { scale: Scale; active?: string }) {
  const label = SCALE_LABELS[scale];
  const sections = scaleSections(scale);
  const current = active ?? sections[0]?.id ?? "";
  const theme = orderedThemes(scale).find((t) => t.id === current);
  const mapName = THEME_MAPS[scale]?.[current];
  const depMap = mapName ? getDepartmentMap(mapName) : undefined;
  const others = nonMembers(scale);
  const entries = theme ? themeEntries(scale, theme.id) : [];

  return (
    <div className="space-y-6">
      <header className="max-w-3xl space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{label.name}</h1>
        <p className="text-sm text-[var(--muted)]">{label.blurb}</p>
      </header>

      <ThemeTabs active={current} tabs={sections.map((s) => ({ ...s, href: `/${scale}/themes/${s.id}` }))} />

      <div className="space-y-12 pt-4">
        {theme && <ThemeSection scale={scale} scaleName={label.name} theme={theme} heading />}

        {depMap && (
          <section className="space-y-3">
            <h2 className="text-xl font-semibold">{depMap.title}</h2>
            <DepartmentsMap data={depMap} />
            <ul className="list-disc space-y-1 pl-5 text-sm text-[var(--muted)]">
              {depMap.limitations.map((l) => (
                <li key={l}>{l}</li>
              ))}
            </ul>
          </section>
        )}

        {entries.length > 1 && (
          <details className="border-t border-[var(--rule)] pt-4">
            <summary className="cursor-pointer select-none font-medium">
              <span className="chevron mr-1 text-[var(--muted)]">▸</span>
              Toutes les séries de ce thème ({entries.length})
            </summary>
            <div className="mt-3">
              <IndicatorList items={entries} />
            </div>
          </details>
        )}

        {current === VALIDATION_SECTION && <ValidationBox reports={label.validations.flatMap((p) => getValidation(p) ?? [])} />}

        {!active && others.length > 0 && (
          <section className="space-y-3">
            <h2 className="text-xl font-semibold">Autres indicateurs</h2>
            <IndicatorList items={others} />
          </section>
        )}
      </div>
    </div>
  );
}
