"""Validation de la phase 7 (exploratoire) : critères L1-L5 de docs/phases.md.

Critères et méthode validés par Grég le 31/10/2026, avant tout calcul. Ce module mesure et publie.
Usage : python -m etl.validation.p7   → docs/validation-p7-resultats.md et data/processed/validation-p7.json
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import temperature as T
from etl.schema import Indicator, ValidationCheck, ValidationReport

SCOPE = {"jours-blocage-hiver-monde", "jours-blocage-ete-monde", "z500-europe-monde", "cape-gironde"}
OUT = ROOT / "docs" / "validation-p7-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p7.json"
ACCEPTED: dict[str, str] = {}
L3_PERIOD = (1981, 2010)


@dataclass
class Check:
    name: str
    kind: str
    satisfied: bool
    detail: str

    def __post_init__(self):
        self.passed = self.satisfied
        if self.kind == "critère" and not self.passed and self.name in ACCEPTED:
            self.satisfied = True

    @property
    def status(self) -> str:
        if self.kind != "critère":
            return "ℹ️ information"
        if self.passed:
            return "✅ conforme"
        return f"☑ {ACCEPTED[self.name]}" if self.name in ACCEPTED else "❌ non conforme"


def load(out_dir: Path) -> dict[str, Indicator]:
    out = {}
    for scale in ("monde", "gironde"):
        for path in (out_dir / scale).glob("*.json"):
            if path.stem in SCOPE:
                out[path.stem] = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
    return out


def _series(ind: Indicator) -> dict[int, float]:
    return {int(t): v for t, v in zip(ind.series.time, ind.series.value) if v is not None}


def checks(inds: dict[str, Indicator], out_dir: Path) -> list[Check]:
    from etl.indicators import exploratoire as E
    from etl.sources import era5_blocking as B
    from etl.stats.trend import annual_trend
    cs = []
    missing = sorted(SCOPE - set(inds))
    cs.append(Check("L1 exhaustivité", "critère", not missing,
                    f"{len(inds)} indicateurs sur {len(SCOPE)}" + (f" ; manquants : {', '.join(missing)}" if missing else "")))
    cs.append(Check("L2 complétude", "info", True, "Saisons retenues si tous leurs jours (blocages) ou leurs 3 mois (CAPE) "
                                                   "existent ; années complètes (Z500)."))
    try:
        frac = {}
        for season, iid in (("hiver", "jours-blocage-hiver-monde"), ("ete", "jours-blocage-ete-monde")):
            s = _series(inds[iid])
            ys = [y for y in range(L3_PERIOD[0], L3_PERIOD[1] + 1) if y in s]
            frac[season] = 100 * sum(s[y] / len(E.season_days(y, season)) for y in ys) / len(ys)
        ok = frac["hiver"] > frac["ete"] and all(5 <= v <= 40 for v in frac.values())
        cs.append(Check("L3 plausibilité climatologique", "critère", ok,
                        f"jours bloqués 1981-2010 : hiver {T.fr(frac['hiver'], 1, False)} %, été {T.fr(frac['ete'], 1, False)} % "
                        "(attendu : hiver > été, chacun entre 5 et 40 %)"))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("L3 plausibilité climatologique", "critère", False, f"non calculé : {exc}"))
    try:
        rows = B.load()
        parts = []
        for season, iid in (("hiver", "jours-blocage-hiver-monde"), ("ete", "jours-blocage-ete-monde")):
            alt = E.seasonal_counts(rows, season, E.SECTOR_ALT)
            main = inds[iid].trend
            ys = [y for y in range(main.period.start, main.period.end + 1) if y in alt]
            t = annual_trend(ys, [alt[y] for y in ys])
            same = (t.slope_per_decade > 0) == (main.slope_per_decade > 0) or (t.slope_per_decade == 0 == main.slope_per_decade)
            parts.append(f"{season} : 30° O-30° E {T.fr(main.slope_per_decade, 2)}, 20° O-40° E {T.fr(t.slope_per_decade, 2)} "
                         f"jours/déc. ({'même signe' if same else 'signes opposés'})")
        cs.append(Check("L4 robustesse au secteur (information)", "info", True, " ; ".join(parts)))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("L4 robustesse au secteur (information)", "info", True, f"non calculé : {exc}"))
    cs.append(Check("L5 technique", "info", True, "Tests, CI et contrat vérifiés par les workflows."))
    return cs


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load(out_dir)
    if not inds:
        print("Aucun indicateur P7 publié : validation P7 non exécutée.")
        return 0
    cs = checks(inds, out_dir)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P7 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p7` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P7).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    rep = ValidationReport(phase="p7", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=sorted(inds),
                           checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied,
                                                   detail=c.detail) for c in cs])
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
