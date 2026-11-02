"""Validation de la phase 8 (synthèse) : critères M1-M7 de docs/phases.md.

Critères validés par Grég le 02/11/2026, avant toute rédaction et tout calcul. Ce module mesure et publie.
Usage : python -m etl.validation.p8   → docs/validation-p8-resultats.md et data/processed/validation-p8.json
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from etl import synthese as S
from etl.context import PROCESSED_DIR, ROOT
from etl.schema import ValidationCheck, ValidationReport
from etl.validation.p7 import Check

OUT = ROOT / "docs" / "validation-p8-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p8.json"
RELECTURE = ROOT / "docs" / "relecture-p8.md"
M5_RANGE = (0.059, 0.109)
CLOSED_MARK = "Relecture close"


def checks(res: S.Result) -> list[Check]:
    syn = res.synthesis
    claims = [c for s in syn.sections for g in s.groups for c in g.claims]
    cs = []
    cs.append(Check("M1 chiffres produits par l'ETL", "critère", not res.m1,
                    "aucun nombre écrit en dur hors années et seuils déclarés" if not res.m1 else " ; ".join(res.m1[:5])))
    probs = [f"{c.id} : {c.problem}" for c in claims if c.problem]
    n_conf = sum(1 for c in claims if c.confidence)
    cs.append(Check("M2 confiance et type d'affirmation", "critère", not probs,
                    f"{n_conf} affirmations qualifiées selon S1, aucune règle S2 enfreinte" if not probs else " ; ".join(probs[:5])))
    cs.append(Check("M3 couverture", "critère", not res.m3_missing,
                    "chaque case publiée de la couverture a au moins une affirmation à son échelle"
                    if not res.m3_missing else "cases sans affirmation : " + ", ".join(res.m3_missing)))
    cmp_claims = [c for c in claims if c.kind == "comparaison"]
    cfg_cmp = {c["id"]: c for c in __import__("yaml").safe_load(S.CONFIG.read_text(encoding="utf-8"))["comparisons"]}
    bad = [k for k, c in cfg_cmp.items() if c["a"] == c["b"]]
    detail = "; ".join(f"{k} {c.start}-{c.end} : {c.verdict.replace(' que', '')}" for k, c in res.comparisons.items())
    cs.append(Check("M4 comparaisons sur période commune (S3)", "critère", not bad and bool(cmp_claims),
                    f"{len(cmp_claims)} affirmations de comparaison ; {detail}"))
    _, r = res.accelerations["gmsl-nerem"]
    lo, hi = M5_RANGE
    cs.append(Check("M5 accélération du niveau marin 1993-2017", "critère", lo <= r.value <= hi,
                    f"{r.value:.3f} mm/an² (IC {r.ci_low:.3f} à {r.ci_high:.3f}, p = {r.p_value}) ; fourchette [{lo} ; {hi}] "
                    "(Nerem et al., 2018)"))
    closed = RELECTURE.exists() and CLOSED_MARK in RELECTURE.read_text(encoding="utf-8")
    cs.append(Check("M6 relecture indépendante", "critère", closed,
                    "relecture close : docs/relecture-p8.md" if closed else "relecture indépendante non close (docs/relecture-p8.md)"))
    exp = next(s for s in syn.sections if s.id == "exploratoire")
    exp_claims = [c for g in exp.groups for c in g.claims]
    capped = all(c.confidence in (None, "non_etabli") for c in exp_claims)
    cs.append(Check("M7 section exploratoire (P7)", "critère", capped,
                    "en attente du relevé P7, mention affichée" if exp.pending and not exp_claims
                    else f"{len(exp_claims)} affirmations, toutes plafonnées" if capped else "affirmation P7 non plafonnée"))
    for k, (ind, a) in res.accelerations.items():
        cs.append(Check(f"Accélération {k}", "info", True,
                        f"{ind} {a.start}-{a.end} : {a.value:.4g} par an² (IC {a.ci_low:.4g} à {a.ci_high:.4g}), "
                        f"p = {a.p_value}, Newey-West décalage {a.lag}"))
    kinds = {}
    for c in claims:
        kinds[c.kind] = kinds.get(c.kind, 0) + 1
    cs.append(Check("Répartition des affirmations", "info", True, ", ".join(f"{k} {v}" for k, v in sorted(kinds.items()))))
    return cs


def main(out_dir: Path = PROCESSED_DIR) -> int:
    if not (out_dir / "couverture.json").exists():
        print("Couverture absente : validation P8 non exécutée.")
        return 0
    res = S.build(out_dir)
    cs = checks(res)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P8 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p8` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P8).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    ids = sorted({i.id for s in res.synthesis.sections for g in s.groups for c in g.claims for i in c.indicators})
    rep = ValidationReport(phase="p8", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=ids,
                           checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied,
                                                   detail=c.detail) for c in cs])
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
