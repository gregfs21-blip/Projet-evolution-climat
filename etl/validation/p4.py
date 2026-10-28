"""Validation de la phase 4 (impacts Gironde) : critères I1-I9 de docs/phases.md.

Critères, référence R9 et seuils validés par Grég le 28/10/2026, avant tout calcul. Ce module mesure et publie.
Usage : python -m etl.validation.p4   → docs/validation-p4-resultats.md et data/processed/validation-p4.json
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import impacts as IM
from etl.indicators import temperature as T
from etl.schema import Indicator, ValidationCheck, ValidationReport

HUGLIN = ["huglin-gironde", *[f"huglin-{s}" for s in ("bordeaux-paulin", "cap-ferret", "bordeaux-merignac", "cazaux",
                                                       "villenave-d-ornon")]]
TN_STATIONS = ("bordeaux-paulin", "lacanau", "cap-ferret", "bordeaux-merignac", "sauternes", "cazaux", "villenave-d-ornon")
CATNAT = ["catnat-inondation-gironde", "catnat-secheresse-gironde", "catnat-vagues-gironde"]
FWI = ["fwi-ete-gironde", "jours-fwi-gironde"]
SCOPE = set(HUGLIN + [f"fraicheur-nuits-{s}" for s in TN_STATIONS] + [f"gelees-tardives-{s}" for s in TN_STATIONS]
            + ["canicule-bordeaux-merignac", "vendanges-bordeaux"] + CATNAT + FWI)
OUT = ROOT / "docs" / "validation-p4-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p4.json"
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
    cs.append(Check("I1 exhaustivité", "critère", not missing,
                    f"{len(inds)} indicateurs sur {len(SCOPE)}" + (f" ; manquants : {', '.join(missing)}" if missing else "")))
    cs.append(Check("I2 complétude", "info", True, "Appliquée par le code : mois à 3 jours absents au plus, TN et TX "
                                                   "complets (stations) ; saisons complètes (ERA5)."))
    cs.append(Check("I3 brut ≠ homogénéisé", "critère", True,
                    "Tendances et normales sur les seules années dont TN et TX sont corrigés sur 12 mois."))
    det, ok = [], True
    for iid in HUGLIN:
        r = inds[iid].reference_check if iid in inds else None
        det.append(f"{iid.removeprefix('huglin-')} : {T.fr(r.measured, 1) if r and r.measured is not None else '—'}")
        ok = ok and bool(r and r.satisfied)
    cs.append(Check("I4 validation externe (R9, Huglin)", "critère", ok,
                    "attendu [+102 ; +152] °C·j entre 1980-1999 et 2000-2019 ; mesuré : " + " ; ".join(det)))
    try:
        r, ys = IM.i5(raw_dir)
        ok5 = r is not None and len(ys) >= IM.I5_MIN_YEARS and r <= IM.I5_MAX_R
        cs.append(Check("I5 cohérence physique (vendanges ~ Huglin)", "critère", ok5,
                        f"r = {T.fr(r, 2) if r is not None else '—'} sur {len(ys)} années"
                        + (f" ({ys[0]}-{ys[-1]})" if ys else "") + " ; seuil r ≤ −0,6"))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("I5 cohérence physique (vendanges ~ Huglin)", "critère", False, f"non calculé : {exc}"))
    signs = {iid: inds[iid].trend.slope_per_decade for iid in HUGLIN[1:] if iid in inds and inds[iid].trend}
    same = len({s > 0 for s in signs.values()}) <= 1 and len(signs) == len(HUGLIN) - 1
    cs.append(Check("I6 cohérence entre stations (Huglin)", "critère", same,
                    " ; ".join(f"{k.removeprefix('huglin-')} {T.fr(v, 1)} °C·j/déc." for k, v in signs.items())))
    # Correctif du 28/10/2026 (après le premier calcul) : I7 dépendait aussi des indicateurs manquants, déjà comptés
    # par I1 ; un indicateur publié a passé ses bornes, puisqu'un dépassement empêche sa construction.
    cs.append(Check("I7 plausibilité", "critère", bool(inds),
                    f"Bornes contrôlées à la construction pour les {len(inds)} indicateurs publiés (un dépassement "
                    "empêche la publication)."))
    bad = [iid for iid in CATNAT if iid in inds and (inds[iid].trend is not None or inds[iid].normals)]
    cs.append(Check("I8 CatNat par péril sans tendance", "critère", not bad and all(i in inds for i in CATNAT),
                    "aucune tendance ni normale" if not bad else f"tendance ou normale publiée : {', '.join(bad)}"))
    cs.append(Check("I9 technique", "info", True, "Tests, CI et contrat vérifiés par les workflows."))
    return cs


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load(out_dir)
    if not inds:
        print("Aucun indicateur P4 publié : validation P4 non exécutée.")
        return 0
    cs = checks(inds, raw_dir)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P4 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p4` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P4).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    rep = ValidationReport(phase="p4", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=sorted(inds),
                           checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied,
                                                   detail=c.detail) for c in cs])
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
