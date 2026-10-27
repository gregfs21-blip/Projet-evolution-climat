"""Validation de la phase 3 (atmosphère et littoral Gironde) : critères H1-H8 de docs/phases.md.

Critères, référence R8 et règle H5 validés par Grég le 27/10/2026, avant tout calcul. Ce module mesure et publie.
Usage : python -m etl.validation.p3   → docs/validation-p3-resultats.md et data/processed/validation-p3.json
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import atmosphere as AT
from etl.schema import Indicator, ValidationCheck, ValidationReport

SCOPE = {"pression-bordeaux-era5", "humidite-bordeaux-era5", "sst-gascogne-large-gironde", "sst-golfe-gascogne",
         "niveau-mer-large-gironde", "jours-vent-fort-bordeaux-era5", "rafale-max-bordeaux-era5"}
OUT = ROOT / "docs" / "validation-p3-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p3.json"
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
    for path in (out_dir / "gironde").glob("*.json"):
        if path.stem in SCOPE:
            out[path.stem] = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
    return out


def checks(inds: dict[str, Indicator], raw_dir: Path) -> list[Check]:
    cs = []
    missing = sorted(SCOPE - set(inds))
    cs.append(Check("H1 exhaustivité", "critère", not missing,
                    f"{len(inds)} indicateurs sur {len(SCOPE)}" + (f" ; manquants : {', '.join(missing)}" if missing else "")))
    cs.append(Check("H2 complétude", "info", True, "Appliquée par le code : mois ETCCDI et années de 12 mois (stations), "
                                                  "années complètes (ERA5, altimétrie)."))
    cs.append(Check("H3 brut ≠ homogénéisé", "critère", True,
                    "Les mesures de station ne portent aucune tendance publiée ; elles servent au seul contrôle H5."))
    g = inds.get("sst-golfe-gascogne")
    r = g.reference_check if g else None
    cs.append(Check("H4 validation externe (R8, SST du golfe)", "critère", bool(r and r.satisfied),
                    f"attendu [+0,21 ; +0,31] °C/déc. sur 1982-2014 ; mesuré : {r.measured if r else '—'}"))
    h6 = []
    for var, iid in (("pression", "pression-bordeaux-era5"), ("humidite", "humidite-bordeaux-era5")):
        ind = inds.get(iid)
        if ind is None:
            cs.append(Check(f"H5 contrôle croisé ({var})", "critère", False, "indicateur absent"))
            continue
        res = AT.h5(var, {int(t): v for t, v in zip(ind.series.time, ind.series.value)}, str(raw_dir))
        cs.append(Check(f"H5 contrôle croisé ({var})", "critère", all(c["ok"] for c in res),
                        " ; ".join(f"{c['poste']} : {c['detail']}" for c in res)))
        signs = {np.sign(c["trend"].slope_per_decade) for c in res if "trend" in c}
        same = len({c["ok"] for c in res}) == 1 and len(signs) <= 1
        h6.append(f"{var} : {'même comportement' if same else 'comportements différents'}")
        if not same:
            h6.append("à expliquer")
    cs.append(Check("H6 cohérence entre stations", "critère", "à expliquer" not in h6, " ; ".join(h6)))
    cs.append(Check("H7 plausibilité", "critère", not missing, "Bornes contrôlées à la construction (un dépassement "
                                                               "empêche la publication)."))
    # Vent : information seulement (décision du 27/10/2026).
    try:
        era = inds["jours-vent-fort-bordeaux-era5"]
        e = {int(t): v for t, v in zip(era.series.time, era.series.value)}
        daily, _ = AT._fxi(str(raw_dir))
        st = AT.fxi_counts(daily["33281001"], 16.0)
        ys = sorted(set(e) & set(st))
        r_ = float(np.corrcoef([e[y] for y in ys], [st[y] for y in ys])[0, 1]) if len(ys) > 10 else float("nan")
        cs.append(Check("Vent : ERA5 et mesure (information)", "info", True,
                        f"corrélation interannuelle des jours de vent fort, ERA5 contre rafales mesurées à Mérignac "
                        f"(≥ 16 m/s, brutes) : r = {r_:.2f} sur {len(ys)} ans"))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("Vent : ERA5 et mesure (information)", "info", True, f"non calculée : {exc}"))
    cs.append(Check("H8 technique", "info", True, "Tests, CI et contrat vérifiés par les workflows."))
    return cs


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load(out_dir)
    if not inds:
        print("Aucun indicateur P3 publié : validation P3 non exécutée.")
        return 0
    cs = checks(inds, raw_dir)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P3 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p3` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P3).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    rep = ValidationReport(phase="p3", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=sorted(inds),
                           checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied,
                                                   detail=c.detail) for c in cs])
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
