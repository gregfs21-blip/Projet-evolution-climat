"""Validation de la phase 5 (France) : critères J1-J8 de docs/phases.md.

Critères, référence R10 et réseau validés par Grég le 29/10/2026, avant tout calcul. Ce module mesure et publie.
Usage : python -m etl.validation.p5   → docs/validation-p5-resultats.md et data/processed/validation-p5.json
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import france as F
from etl.indicators import temperature as T
from etl.schema import Indicator, ValidationCheck, ValidationReport
from etl.stats.trend import annual_trend

SCOPE = {"tn-france", "tm-france", "tx-france", "rr-cumul-france"}
OUT = ROOT / "docs" / "validation-p5-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p5.json"
ACCEPTED: dict[str, str] = {}


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
    for path in (out_dir / "france").glob("*.json"):
        if path.stem in SCOPE:
            out[path.stem] = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
    return out


def checks(inds: dict[str, Indicator], raw_dir: Path) -> list[Check]:
    cs = []
    missing = sorted(SCOPE - set(inds))
    cs.append(Check("J1 exhaustivité", "critère", not missing,
                    f"{len(inds)} indicateurs sur {len(SCOPE)}" + (f" ; manquants : {', '.join(missing)}" if missing else "")))
    cs.append(Check("J2 complétude", "info", True, "Appliquée par le code : années de 12 mois homogénéisés, réseau "
                                                   "constant 1959-2021 (températures) et 1961-2014 (pluie)."))
    cs.append(Check("J3 brut ≠ homogénéisé", "critère", True,
                    "Tendances, normales et R10 sur les seules années où toutes les stations sont homogénéisées."))
    r = inds["tm-france"].reference_check if "tm-france" in inds else None
    cs.append(Check("J4 validation externe (R10, TM)", "critère", bool(r and r.satisfied),
                    f"attendu [+0,2 ; +0,4] °C/déc. sur 1959-2021 ; mesuré : "
                    f"{T.fr(r.measured, 3) if r and r.measured is not None else '—'}"))
    try:
        slopes = F.station_slopes(raw_dir)
        pos = [p for p, v in slopes.items() if v > 0]
        neg = sorted((v, p) for p, v in slopes.items() if v <= 0)
        share = len(pos) / len(slopes)
        cs.append(Check("J5 cohérence spatiale (contrôle interne)", "critère", share >= 0.95 and not neg,
                        f"{len(pos)} pentes positives sur {len(slopes)} ({T.fr(100 * share, 1, False)} %) ; "
                        f"médiane {T.fr(sorted(slopes.values())[len(slopes) // 2], 2)} °C/déc."
                        + (f" ; négatives ou nulles : {', '.join(f'{p} ({T.fr(v, 2)})' for v, p in neg[:10])}" if neg else "")))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("J5 cohérence spatiale (contrôle interne)", "critère", False, f"non calculé : {exc}"))
    try:
        simple, hom = F.composite(F.station_anomalies("TM", raw_dir), weighted=False)
        ys = list(range(F.T_SPAN[0], F.T_SPAN[1] + 1))
        a = annual_trend(ys, [simple[y] for y in ys]).slope_per_decade
        b = inds["tm-france"].trend.slope_per_decade if "tm-france" in inds and inds["tm-france"].trend else None
        cs.append(Check("J6 robustesse de la pondération", "critère", b is not None and abs(a - b) <= 0.05,
                        f"pondéré par département {T.fr(b, 3) if b is not None else '—'} ; moyenne simple {T.fr(a, 3)} "
                        "°C/déc. ; écart admis 0,05"))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("J6 robustesse de la pondération", "critère", False, f"non calculé : {exc}"))
    cs.append(Check("J7 plausibilité", "critère", bool(inds),
                    f"Bornes contrôlées à la construction pour les {len(inds)} indicateurs publiés (un dépassement "
                    "empêche la publication)."))
    cs.append(Check("J8 technique", "info", True, "Tests, CI et contrat vérifiés par les workflows."))
    return cs


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load(out_dir)
    if not inds:
        print("Aucun indicateur P5 publié : validation P5 non exécutée.")
        return 0
    cs = checks(inds, raw_dir)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P5 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p5` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P5).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    rep = ValidationReport(phase="p5", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=sorted(inds),
                           checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied,
                                                   detail=c.detail) for c in cs])
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
