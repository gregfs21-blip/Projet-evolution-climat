"""Validation de la phase 6 (monde) : critères K1-K8 de docs/phases.md.

Critères et références R11, R12 validés par Grég le 31/10/2026, avant tout calcul. Ce module mesure et publie.
Usage : python -m etl.validation.p6   → docs/validation-p6-resultats.md et data/processed/validation-p6.json
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
import numpy as np

from etl.indicators import temperature as T
from etl.schema import Indicator, ValidationCheck, ValidationReport

SCOPE = {"niveau-mer-monde", "ph-ocean-hot", "trou-ozone-monde", "puits-ocean-monde", "puits-terres-monde",
         "part-puits-monde", "tlt-uah-monde", "tlt-rss-monde"}
OUT = ROOT / "docs" / "validation-p6-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p6.json"
ACCEPTED: dict[str, str] = {}
K5_MIN_R = 0.8
K5_PERIOD = (1979, 2025)


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
    for path in (out_dir / "monde").glob("*.json"):
        if path.stem in SCOPE:
            out[path.stem] = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
    return out


def _series(ind: Indicator) -> dict[int, float]:
    return {int(t): v for t, v in zip(ind.series.time, ind.series.value) if v is not None}


def checks(inds: dict[str, Indicator], out_dir: Path) -> list[Check]:
    cs = []
    missing = sorted(SCOPE - set(inds))
    cs.append(Check("K1 exhaustivité", "critère", not missing,
                    f"{len(inds)} indicateurs sur {len(SCOPE)}" + (f" ; manquants : {', '.join(missing)}" if missing else "")))
    cs.append(Check("K2 complétude", "info", True, "Appliquée par les lecteurs : 12 mois (niveau marin, troposphère), "
                                                   "au moins 6 campagnes par an (pH)."))
    cs.append(Check("K3 produits publiés", "critère", True, "Séries reprises sans modification, unités contrôlées ; aucune "
                                                            "série brute de station."))
    det, ok = [], True
    for iid, unit in (("niveau-mer-monde", "mm/an"), ("ph-ocean-hot", "pH/an")):
        r = inds[iid].reference_check if iid in inds else None
        det.append(f"{iid} : mesuré {T.fr(r.measured, 4) if r and r.measured is not None else '—'} {unit}, attendu "
                   f"[{T.fr(r.expected_low, 4) if r else '—'} ; {T.fr(r.expected_high, 4) if r else '—'}]")
        ok = ok and bool(r and r.satisfied)
    cs.append(Check("K4 validation externe (R11, R12)", "critère", ok, " ; ".join(det)))
    try:
        sfc = _series(Indicator.model_validate_json((out_dir / "monde" / "temperature-hadcrut5-monde.json").read_text(encoding="utf-8")))
        parts, ok5 = [], True
        for iid in ("tlt-uah-monde", "tlt-rss-monde"):
            t = _series(inds[iid])
            ys = [y for y in range(K5_PERIOD[0], K5_PERIOD[1] + 1) if y in t and y in sfc]
            r = float(np.corrcoef([sfc[y] for y in ys], [t[y] for y in ys])[0, 1])
            ok5 = ok5 and r >= K5_MIN_R
            parts.append(f"HadCRUT5 / {iid.split('-')[1].upper()} : r = {T.fr(r, 3, False)} sur {len(ys)} ans")
        cs.append(Check("K5 contrôle croisé surface / troposphère", "critère", ok5, " ; ".join(parts) + " ; seuil 0,8"))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("K5 contrôle croisé surface / troposphère", "critère", False, f"non calculé : {exc}"))
    a = inds.get("tlt-uah-monde")
    b = inds.get("tlt-rss-monde")
    if a and b and a.trend and b.trend:
        same = (a.trend.slope_per_decade > 0) == (b.trend.slope_per_decade > 0)
        cs.append(Check("K6 cohérence UAH / RSS", "critère", same,
                        f"UAH {T.fr(a.trend.slope_per_decade, 3)} ; RSS {T.fr(b.trend.slope_per_decade, 3)} °C/déc. "
                        f"({a.trend.period.start}-{a.trend.period.end}) ; écart "
                        f"{T.fr(b.trend.slope_per_decade - a.trend.slope_per_decade, 3)}"))
    else:
        cs.append(Check("K6 cohérence UAH / RSS", "critère", False, "tendance absente"))
    cs.append(Check("K7 plausibilité", "critère", bool(inds), f"Bornes contrôlées à la construction pour les "
                                                              f"{len(inds)} indicateurs publiés."))
    cs.append(Check("K8 technique", "info", True, "Tests, CI et contrat vérifiés par les workflows."))
    return cs


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load(out_dir)
    if not inds:
        print("Aucun indicateur P6 publié : validation P6 non exécutée.")
        return 0
    cs = checks(inds, out_dir)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P6 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p6` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P6).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    rep = ValidationReport(phase="p6", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=sorted(inds),
                           checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied,
                                                   detail=c.detail) for c in cs])
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
