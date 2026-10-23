"""Validation de la phase 1 contre les références externes et les critères C1-C8.

C4 est retiré (référence invalide) et remplacé par C4bis, recoupement ERA5, le 23/10/2026.
C4 reste calculé et publié pour information.

Les critères et les seuils sont ceux de docs/phases.md, fixés avant tout calcul.
Ce module ne les interprète pas : il mesure et publie. L'analyse des écarts est
rédigée à la main dans docs/validation-p1.md.

Usage : python -m etl.validation.p1   → écrit docs/validation-p1-resultats.md
                                         et data/processed/validation-p1.json
"""

from __future__ import annotations

import json
import logging
import statistics
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import temperature as T
from etl.schema import Indicator, ValidationCheck, ValidationReport
from etl.sources import openmeteo_era5 as era5
from etl.stats.trend import annual_trend, ols_slope_per_decade

log = logging.getLogger("etl.validation")

# Références publiées (docs/phases.md). Intervalles = fourchettes publiées, arrondies au dixième.
R1 = {"TN": (0.15, 0.35), "TX": (0.25, 0.35)}                       # ClimatHD Nouvelle-Aquitaine, 1959-2009
R2 = {"hiver": 0.13, "printemps": 0.25, "été": 0.23, "automne": 0.12}  # ORACLE 2020, Villenave, TM 1959-2019
R2_PERIOD = (1959, 2019)
R2_TOLERANCE = 0.05
C5_TOLERANCE = 0.10
VILLENAVE = "33550001"
SEASONS = {"hiver": (12, 1, 2), "printemps": (3, 4, 5), "été": (6, 7, 8), "automne": (9, 10, 11)}

# C4bis (docs/phases.md, décision du 23/10/2026, fixé avant calcul)
C4BIS_POINT = (44.790, -0.577)          # Villenave-d'Ornon
C4BIS_PERIOD = (1979, 2022)
C4BIS_MAX_SLOPE = 0.10                  # °C/déc., sur la série des différences LSH − ERA5
ERA5_START, ERA5_END = "1958-12-01", "2022-12-31"   # décembre 1958 : hiver 1959

# Écarts acceptés par Grég (docs/phases.md) : réputés satisfaits pour l'application de C7.
ACCEPTED = {"C3 TX composite 1959-2009": "écart accepté le 23/10/2026"}

OUT = ROOT / "docs" / "validation-p1-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p1.json"   # lu par le site (encart « Résultats validés »)


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str
    kind: str = "critère"     # "critère" (compte pour la clôture), "info" ou "retiré" (publiés, sans effet)
    slope: float | None = None
    p_value: float | None = None

    @property
    def status(self) -> str:
        if self.kind == "retiré":
            return "↩ retiré, pour information"
        if self.kind == "info":
            return "ℹ information"
        if self.passed:
            return "✅ conforme"
        if self.name in ACCEPTED:
            return f"☑ {ACCEPTED[self.name]}"
        return "❌ écart"

    @property
    def satisfied(self) -> bool:
        return self.passed or self.name in ACCEPTED


# ---------------------------------------------------------------- C3, C4 (références externes)


@lru_cache(maxsize=1)
def c3(raw_dir: str = str(RAW_DIR)) -> list[Check]:
    out = []
    for var, (lo, hi) in R1.items():
        series, members, _ = T.composite_anomaly(var, Path(raw_dir))
        years = [y for y in series.hom_years() if T.CLIMATHD_WINDOW.start <= y <= T.CLIMATHD_WINDOW.end]
        t = annual_trend(years, [series.values[y] for y in years])
        ok = lo <= t.slope_per_decade <= hi
        out.append(Check(
            f"C3 {var} composite 1959-2009",
            ok,
            f"pente de Sen {t.slope_per_decade:+.3f} °C/déc. (IC 95 % {t.slope_ci_low:+.3f} à {t.slope_ci_high:+.3f}), "
            f"attendu [{lo:.2f} ; {hi:.2f}], {len(members)} stations",
        ))
    return out


def seasonal(values: dict, hom: dict | None, years: range) -> dict[str, dict[int, float]]:
    """Moyennes saisonnières. L'hiver N regroupe décembre N-1, janvier et février N."""
    out: dict[str, dict[int, float]] = {}
    for season, months in SEASONS.items():
        out[season] = {}
        for y in years:
            keys = [((y - 1) if (season == "hiver" and m == 12) else y, m) for m in months]
            if all(k in values and (hom is None or hom[k]) for k in keys):
                out[season][y] = sum(values[k] for k in keys) / 3
    return out


def seasonal_tm(station_id: str, raw_dir: Path) -> dict[str, dict[int, float]]:
    values, hom, _ = T.monthly("TM", station_id, raw_dir)
    return seasonal(values, hom, range(R2_PERIOD[0], R2_PERIOD[1] + 1))


@lru_cache(maxsize=1)
def c4(raw_dir: str = str(RAW_DIR)) -> list[Check]:
    seasons = seasonal_tm(VILLENAVE, Path(raw_dir))
    out = []
    for season, ref in R2.items():
        data = seasons[season]
        years = sorted(data)
        complete = len(years) == R2_PERIOD[1] - R2_PERIOD[0] + 1
        ols = ols_slope_per_decade(years, [data[y] for y in years])
        sen = annual_trend(years, [data[y] for y in years]).slope_per_decade
        ok = complete and abs(ols - ref) <= R2_TOLERANCE
        out.append(Check(
            f"C4 Villenave TM {season} 1959-2019",
            ok,
            f"régression linéaire {ols:+.3f}, Sen {sen:+.3f}, publié {ref:+.2f} °C/déc., "
            f"écart {ols - ref:+.3f} (tolérance ±{R2_TOLERANCE}) — référence jugée invalide"
            + ("" if complete else " — SÉRIE INCOMPLÈTE"),
            kind="retiré",
        ))
    return out


@lru_cache(maxsize=2)
def era5_villenave(raw_dir: str) -> tuple[dict, era5.Era5Daily]:
    data = era5.fetch_daily(*C4BIS_POINT, ERA5_START, ERA5_END, Path(raw_dir), download=not T._offline())
    return era5.monthly_means(data), data


def difference_check(name: str, lsh: dict[int, float], rea: dict[int, float], period: tuple[int, int],
                     kind: str) -> Check:
    years = list(range(period[0], period[1] + 1))
    missing = [y for y in years if y not in lsh or y not in rea]
    if missing:
        return Check(name, False, f"non évalué : années manquantes {missing[:5]}…", kind)
    d = [lsh[y] - rea[y] for y in years]
    t = annual_trend(years, d)
    ok = abs(t.slope_per_decade) <= C4BIS_MAX_SLOPE and not t.significant
    offset = sum(d) / len(d)
    return Check(
        name, ok,
        f"dérive LSH − ERA5 : pente {t.slope_per_decade:+.3f} °C/déc. (IC 95 % {t.slope_ci_low:+.3f} à "
        f"{t.slope_ci_high:+.3f}), Hamed-Rao p = {t.p_value:.3f} ; seuil |pente| ≤ {C4BIS_MAX_SLOPE} et p ≥ 0,05 ; "
        f"décalage moyen {offset:+.2f} °C",
        kind,
        slope=t.slope_per_decade,
        p_value=t.p_value,
    )


def _annual_hom(values: dict, hom: dict) -> dict[int, float]:
    v, h = T.to_annual(values, hom)
    return {y: x for y, x in v.items() if h[y]}


@lru_cache(maxsize=2)
def c4bis(raw_dir: str = str(RAW_DIR)) -> list[Check]:
    primary = f"C4bis Villenave TM annuelle {C4BIS_PERIOD[0]}-{C4BIS_PERIOD[1]}"
    try:
        rea_monthly, meta = era5_villenave(raw_dir)
    except Exception as exc:  # noqa: BLE001 — une validation absente ne doit jamais relever la confiance
        log.error("C4bis non évalué : %s", exc)
        return [Check(primary, False, f"non évalué : ERA5 indisponible ({exc})")]

    rea_annual = {v: T.to_annual(m, {k: True for k in m})[0] for v, m in rea_monthly.items()}
    lsh = {}
    for var in ("TN", "TX", "TM"):
        values, hom, _ = T.monthly(var, VILLENAVE, Path(raw_dir))
        lsh[var] = (values, hom)
    cell = (f"maille ERA5 {meta.cell_lat:.3f} N ; {meta.cell_lon:.3f} E, altitude {meta.elevation:.0f} m "
            f"(demandé {C4BIS_POINT[0]:.3f} ; {C4BIS_POINT[1]:.3f})")

    first = difference_check(primary, _annual_hom(*lsh["TM"]), rea_annual["TM"], C4BIS_PERIOD, "critère")
    out = [Check(first.name, first.passed, f"{first.detail} ; {cell}", first.kind, first.slope, first.p_value)]
    for var in ("TN", "TX"):
        out.append(difference_check(f"C4bis (info) Villenave {var} annuelle {C4BIS_PERIOD[0]}-{C4BIS_PERIOD[1]}",
                                    _annual_hom(*lsh[var]), rea_annual[var], C4BIS_PERIOD, "info"))
    out.append(difference_check("C4bis (info) Villenave TM annuelle 1959-2019",
                                _annual_hom(*lsh["TM"]), rea_annual["TM"], (1959, 2019), "info"))
    years = range(C4BIS_PERIOD[0], C4BIS_PERIOD[1] + 1)
    s_lsh = seasonal(*lsh["TM"], years)
    s_rea = seasonal(rea_monthly["TM"], None, years)
    for season in SEASONS:
        out.append(difference_check(f"C4bis (info) Villenave TM {season} {C4BIS_PERIOD[0]}-{C4BIS_PERIOD[1]}",
                                    s_lsh[season], s_rea[season], C4BIS_PERIOD, "info"))
    return out


def variable_caveat(variable: str, raw_dir: Path = RAW_DIR) -> str | None:
    """Mise en garde quand le recoupement informatif ERA5 d'une variable dépasse le seuil de C4bis.

    N'influe pas sur la confiance (règle C7 inchangée) : c'est une information, affichée telle quelle.
    """
    check = next((c for c in c4bis(str(raw_dir)) if c.name.startswith(f"C4bis (info) Villenave {variable} annuelle 1979")), None)
    if check is None or check.passed or check.slope is None:
        return None
    fr = lambda x, f: format(x, f).replace(".", ",")  # noqa: E731
    sense = "plus vite" if check.slope > 0 else "moins vite"
    over = abs(check.slope) > C4BIS_MAX_SLOPE
    significant = check.p_value < 0.05
    reason = (
        "écart supérieur au seuil de 0,10 °C par décennie" + (" et significatif" if significant else "")
        if over else "écart inférieur au seuil de 0,10 °C par décennie, mais statistiquement significatif"
    )
    return (
        f"Recoupement avec la réanalyse ERA5 à Villenave-d'Ornon (1979-2022) : pour cette variable, la station se "
        f"réchauffe {sense} que la réanalyse, de {fr(abs(check.slope), '.3f')} °C par décennie "
        f"(p = {fr(check.p_value, '.3f')}) ; {reason}. La hausse est confirmée par les deux sources, sa valeur "
        "exacte est moins assurée que pour la température moyenne."
    )


def external_validation_passed(raw_dir: Path = RAW_DIR) -> bool:
    """C7 : C3 (écarts acceptés compris) et C4bis. C4, retiré, n'entre plus en compte."""
    checks = [c for c in c3(str(raw_dir)) + c4bis(str(raw_dir)) if c.kind == "critère"]
    return all(c.satisfied for c in checks)


# ---------------------------------------------------------------- C1, C5-C8 (sur les JSON publiés)


# Périmètre de P1 : les températures annuelles. Les indicateurs des phases suivantes n'en relèvent pas
# et ne doivent ni entrer dans les contrôles C5-C8 ni figurer dans le rapport.
P1_VARIABLES = ("tn", "tm", "tx")


def in_scope(ind: Indicator) -> bool:
    return ind.variable is not None and ind.variable.id in P1_VARIABLES


def load_indicators(out_dir: Path = PROCESSED_DIR) -> list[Indicator]:
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    inds = [Indicator.model_validate_json((out_dir / e["path"]).read_text(encoding="utf-8")) for e in manifest["indicators"]]
    return [i for i in inds if in_scope(i)]


def internal_checks(inds: list[Indicator], raw_dir: Path) -> tuple[list[Check], list[str]]:
    checks: list[Check] = []
    lines: list[str] = []
    stations = [i for i in inds if i.place and i.place.kind == "station"]

    # C1 — exhaustivité
    for var in ("TN", "TX"):
        expected = set(T.stations_with(var, raw_dir))
        got = {i.stations[0].id for i in stations if i.variable.id == var.lower()}
        checks.append(Check(f"C1 {var}", expected == got,
                            f"{len(got)}/{len(expected)} séries LSH traitées" + (f", manquantes : {sorted(expected - got)}" if expected - got else "")))

    # C5 — cohérence inter-stations sur la période commune
    lines += ["", "### C5 — Pentes 1962-2022 par station (°C/déc.)", "", "| Variable | Station | Pente | Écart à la médiane | À expliquer |", "|---|---|---|---|---|"]
    for var in ("tn", "tx", "tm"):
        rows = []
        for i in stations:
            if i.variable.id != var:
                continue
            t = next((a for a in i.alt_trends if a.label.startswith("1962-2022")), None)
            if t:
                rows.append((i.stations[0].name, t.slope_per_decade))
        if not rows:
            continue
        med = statistics.median(v for _, v in rows)
        flagged = 0
        for name, v in sorted(rows, key=lambda r: -r[1]):
            out = abs(v - med) > C5_TOLERANCE
            flagged += out
            lines.append(f"| {var.upper()} | {name} | {v:+.3f} | {v - med:+.3f} | {'**oui**' if out else 'non'} |")
        checks.append(Check(f"C5 {var.upper()}", flagged == 0,
                            f"médiane {med:+.3f} ; {flagged} station(s) à plus de {C5_TOLERANCE} de la médiane"))

    # C6 — ruptures
    lines += ["", "### C6 — Ruptures de Pettitt (p < 0,05) sur séries homogénéisées", "",
              "| Indicateur | Nouveau régime | p | p après retrait de tendance | Artefact possible | Détail |", "|---|---|---|---|---|---|"]
    for i in inds:
        for b in i.breakpoints:
            lines.append(f"| {i.id} | {b.time} | {b.p_value:.4f} | {b.detrended_p_value:.3f} | {'**oui**' if b.possible_artifact else 'non'} | {b.note} |")
    bps = [b for i in inds for b in i.breakpoints]
    checks.append(Check("C6", True, f"{len(bps)} rupture(s) détectée(s), {sum(b.possible_artifact for b in bps)} marquée(s) "
                                    f"artefact possible, {sum((b.detrended_p_value or 1) < 0.05 for b in bps)} encore significative(s) "
                                    "après retrait de la tendance"))

    # C7 — effet de la correction de l'autocorrélation
    lines += ["", "### C7 — Significativité : Mann-Kendall classique vs Hamed-Rao (période homogénéisée)", "",
              "| Indicateur | Pente | p classique | p Hamed-Rao | Conclusion modifiée | Confiance |", "|---|---|---|---|---|---|"]
    changed = 0
    for i in inds:
        t = i.trend
        flip = (t.p_value_classical < t.alpha) != t.significant
        changed += flip
        lines.append(f"| {i.id} | {t.slope_per_decade:+.3f} | {t.p_value_classical:.2e} | {t.p_value:.2e} | {'**oui**' if flip else 'non'} | {i.confidence} |")
    checks.append(Check("C7", True, f"{changed} série(s) dont la conclusion change avec la correction"))

    # C8 — traçabilité
    missing = [i.id for i in inds for st in i.stations
               if not (st.series_id and st.homogenized_period and st.min_detectable_amplitude is not None and st.file_produced)]
    checks.append(Check("C8", not missing, "métadonnées Météo-France complètes" if not missing else f"incomplètes : {missing}"))
    return checks, lines


def build_report(checks: list[Check], verdict: str, indicators: list[str]) -> ValidationReport:
    """Version structurée du tableau publié, pour le site. Même contenu, aucune réinterprétation."""
    from datetime import datetime, timezone

    counted = [c for c in checks if c.kind == "critère"]
    return ValidationReport(
        phase="p1",
        generated_at=datetime.now(timezone.utc).replace(microsecond=0),
        closure_ok=all(c.satisfied for c in counted),
        verdict=verdict,
        indicators=indicators,
        checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied, detail=c.detail)
                for c in checks],
    )


def main() -> int:
    inds = load_indicators()
    ext = c3() + c4bis() + c4()
    internal, tables = internal_checks(inds, RAW_DIR)
    checks = internal[:2] + ext + internal[2:]
    counted = [c for c in checks if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits (écarts acceptés compris)."
               if all(c.satisfied for c in counted) else
               "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = [
        "# Validation P1 — résultats automatiques",
        "",
        "Fichier généré par `python -m etl.validation.p1` à chaque exécution de l'ETL. Ne pas éditer à la main :",
        "l'analyse des écarts est dans `docs/validation-p1.md`. Critères et seuils : `docs/phases.md`.",
        "",
        f"**{verdict}**",
        "",
        "| Critère | Résultat | Mesure |",
        "|---|---|---|",
        *[f"| {c.name} | {c.status} | {c.detail} |" for c in checks],
        *tables,
        "",
    ]
    OUT.write_text("\n".join(md), encoding="utf-8")
    scope = [i.id for i in inds]   # déjà restreint au périmètre P1 par load_indicators
    OUT_JSON.write_text(build_report(checks, verdict, scope).model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in checks))
    print(verdict)
    # Code de sortie 0 même en cas d'écart : un écart se documente, il ne bloque pas la publication.
    return 0


if __name__ == "__main__":
    sys.exit(main())
