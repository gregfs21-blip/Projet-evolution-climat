"""Validation de la phase 1 contre les références externes et les critères C1-C8.

Les critères et les seuils sont ceux de docs/phases.md, fixés avant tout calcul.
Ce module ne les interprète pas : il mesure et publie. L'analyse des écarts est
rédigée à la main dans docs/validation-p1.md.

Usage : python -m etl.validation.p1   → écrit docs/validation-p1-resultats.md
"""

from __future__ import annotations

import json
import statistics
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import temperature as T
from etl.schema import Indicator
from etl.stats.trend import annual_trend, ols_slope_per_decade

# Références publiées (docs/phases.md). Intervalles = fourchettes publiées, arrondies au dixième.
R1 = {"TN": (0.15, 0.35), "TX": (0.25, 0.35)}                       # ClimatHD Nouvelle-Aquitaine, 1959-2009
R2 = {"hiver": 0.13, "printemps": 0.25, "été": 0.23, "automne": 0.12}  # ORACLE 2020, Villenave, TM 1959-2019
R2_PERIOD = (1959, 2019)
R2_TOLERANCE = 0.05
C5_TOLERANCE = 0.10
VILLENAVE = "33550001"
SEASONS = {"hiver": (12, 1, 2), "printemps": (3, 4, 5), "été": (6, 7, 8), "automne": (9, 10, 11)}

OUT = ROOT / "docs" / "validation-p1-resultats.md"


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


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


def seasonal_tm(station_id: str, raw_dir: Path) -> dict[str, dict[int, float]]:
    """TM saisonnière homogénéisée. L'hiver N regroupe décembre N-1, janvier et février N."""
    values, hom, _ = T.monthly("TM", station_id, raw_dir)
    out: dict[str, dict[int, float]] = {}
    for season, months in SEASONS.items():
        out[season] = {}
        for y in range(R2_PERIOD[0], R2_PERIOD[1] + 1):
            keys = [((y - 1) if (season == "hiver" and m == 12) else y, m) for m in months]
            if all(k in values and hom[k] for k in keys):
                out[season][y] = sum(values[k] for k in keys) / 3
    return out


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
            f"écart {ols - ref:+.3f} (tolérance ±{R2_TOLERANCE})" + ("" if complete else " — SÉRIE INCOMPLÈTE"),
        ))
    return out


def external_validation_passed(raw_dir: Path = RAW_DIR) -> bool:
    return all(c.passed for c in c3(str(raw_dir)) + c4(str(raw_dir)))


# ---------------------------------------------------------------- C1, C5-C8 (sur les JSON publiés)


def load_indicators(out_dir: Path = PROCESSED_DIR) -> list[Indicator]:
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    return [Indicator.model_validate_json((out_dir / e["path"]).read_text(encoding="utf-8")) for e in manifest["indicators"]]


def internal_checks(inds: list[Indicator], raw_dir: Path) -> tuple[list[Check], list[str]]:
    checks: list[Check] = []
    lines: list[str] = []
    stations = [i for i in inds if not i.id.endswith("-gironde")]

    # C1 — exhaustivité
    for var in ("TN", "TX"):
        expected = set(T.stations_with(var, raw_dir))
        got = {i.stations[0].id for i in stations if i.id.startswith(var.lower() + "-")}
        checks.append(Check(f"C1 {var}", expected == got,
                            f"{len(got)}/{len(expected)} séries LSH traitées" + (f", manquantes : {sorted(expected - got)}" if expected - got else "")))

    # C5 — cohérence inter-stations sur la période commune
    lines += ["", "### C5 — Pentes 1962-2022 par station (°C/déc.)", "", "| Variable | Station | Pente | Écart à la médiane | À expliquer |", "|---|---|---|---|---|"]
    for var in ("tn", "tx", "tm"):
        rows = []
        for i in stations:
            if not i.id.startswith(var + "-"):
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


def main() -> int:
    inds = load_indicators()
    ext = c3() + c4()
    internal, tables = internal_checks(inds, RAW_DIR)
    checks = internal[:2] + ext + internal[2:]
    md = [
        "# Validation P1 — résultats automatiques",
        "",
        "Fichier généré par `python -m etl.validation.p1` à chaque exécution de l'ETL. Ne pas éditer à la main :",
        "l'analyse des écarts est dans `docs/validation-p1.md`. Critères et seuils : `docs/phases.md`.",
        "",
        "| Critère | Résultat | Mesure |",
        "|---|---|---|",
        *[f"| {c.name} | {'✅ conforme' if c.passed else '❌ écart'} | {c.detail} |" for c in checks],
        *tables,
        "",
    ]
    OUT.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(f"{'OK ' if c.passed else 'ÉCART'} {c.name} : {c.detail}" for c in checks))
    # Code de sortie 0 même en cas d'écart : un écart se documente, il ne bloque pas la publication.
    return 0


if __name__ == "__main__":
    sys.exit(main())
