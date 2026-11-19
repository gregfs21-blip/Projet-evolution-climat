"""Validation de la phase 10 (démonstration), P10.1 : critères O1-O9 de docs/phases.md.

Critères validés par Grég le 17/11/2026, avant tout calcul (D-AF). Les mesures O1-O8 sont faites par
etl/demonstration.py, qui les écrit dans data/processed/demonstration.json ; ce module les relit, contrôle que la
confiance publiée suit la règle D-AG, et publie le rapport.
Usage : python -m etl.validation.p10   → docs/validation-p10-resultats.md et data/processed/validation-p10.json
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, ROOT
from etl.schema import Demonstration, ValidationCheck, ValidationReport

OUT = ROOT / "docs" / "validation-p10-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p10.json"
# Écarts acceptés par Grég après calcul (docs/phases.md, journal P10). Un écart accepté clôt la sous-phase mais ne
# relève pas la confiance (règle D-AG, pratique de P2b) : demonstration.json garde le résultat brut du critère.
ACCEPTED: dict[str, str] = {
    "O8 robustesse": "écart accepté par Grég le 18/11/2026 (D-AI) : seule la variante « forçage anthropique à 5 % » "
                     "sort de la fourchette, l'estimateur AR(1) y dégénère (docs/validation-p10.md)",
}
# Analyses de l'onglet dont la synthèse tient compte (affirmations `limite-attribution` et `limite-projections` de
# etl/config/synthese.yaml, D-AH). Publier une autre analyse (P10.3 France, P10.4, P10.5 projections) rend ces
# affirmations à revoir : ce contrôle échoue jusqu'à leur reformulation, relue (M6), et la mise à jour de cette liste
# (P10.2 ajoutée le 19/11/2026 après relecture, docs/relecture-p8.md).
SYNTHESIS_COVERS = {"p10.1", "p10.2"}


def checks(demo: Demonstration) -> tuple[list[ValidationCheck], list[str]]:
    reg = next(a.regression for a in demo.analyses if a.phase == "p10.1" and a.regression)
    out = []
    for c in reg.criteria:
        name = f"{c.id} {c.label.lower()}"
        ok = c.satisfied or name in ACCEPTED
        status = "✅ conforme" if c.satisfied else (f"☑ {ACCEPTED[name]}" if name in ACCEPTED else "❌ non conforme")
        out.append(ValidationCheck(name=name, kind="critère", status=status, satisfied=ok, detail=c.detail))
    published = sorted(a.phase for a in demo.analyses if a.status == "publie")
    extra = [ph for ph in published if ph not in SYNTHESIS_COVERS]
    out.append(ValidationCheck(
        name="D-AH cohérence de la synthèse", kind="critère",
        status="✅ conforme" if not extra else "❌ non conforme", satisfied=not extra,
        detail=(f"analyses publiées : {', '.join(published)} ; la synthèse (limite-attribution, limite-projections) en "
                "tient compte" if not extra else
                f"analyses publiées que la synthèse ne prend pas en compte : {', '.join(extra)} ; reformuler "
                "limite-attribution et limite-projections (etl/config/synthese.yaml), les faire relire (M6), puis "
                "compléter SYNTHESIS_COVERS")))
    out.append(ValidationCheck(
        name="O9 technique", kind="info", status="ℹ️ information", satisfied=True,
        detail="Tests, contrat et construction de l'onglet vérifiés par la CI (ci.yml), hors de ce module, comme pour "
               "les phases précédentes."))
    out.append(ValidationCheck(
        name="Confiance P10.1 (règle D-AG)", kind="info", status="ℹ️ information", satisfied=True,
        detail=f"{reg.confidence} — {reg.confidence_reason}"))
    inds = {d.indicator_id for d in reg.datasets} | {"oni-monde"}
    # P10.2 — valeurs extrêmes en Gironde (critères X1-X7, D-AO)
    ext = next((a.extremes for a in demo.analyses if a.phase == "p10.2" and a.extremes), None)
    if ext is not None:
        for c in ext.criteria:
            name = f"P10.2 {c.id} {c.label.lower()}"
            ok = c.satisfied or name in ACCEPTED
            status = "✅ conforme" if c.satisfied else (f"☑ {ACCEPTED[name]}" if name in ACCEPTED else "❌ non conforme")
            out.append(ValidationCheck(name=name, kind="critère", status=status, satisfied=ok, detail=c.detail))
        out.append(ValidationCheck(
            name="P10.2 X7 technique", kind="info", status="ℹ️ information", satisfied=True,
            detail="Tests (etl/tests/test_p10b.py), contrat et construction de l'onglet vérifiés par la CI."))
        out.append(ValidationCheck(
            name="Confiance P10.2 (règle D-AO)", kind="info", status="ℹ️ information", satisfied=True,
            detail=f"{ext.confidence} — {ext.confidence_reason}"))
        inds |= {"temperature-gistemp-monde", "temperature-hadcrut5-monde", "tx-annuelle-bordeaux-merignac"}
    # P10.3 — amplification régionale (critères A1-A7, D-AQ)
    amp = next((a.amplification for a in demo.analyses if a.phase == "p10.3" and a.amplification), None)
    if amp is not None:
        for c in amp.criteria:
            name = f"P10.3 {c.id} {c.label.lower()}"
            ok = c.satisfied or name in ACCEPTED
            status = "✅ conforme" if c.satisfied else (f"☑ {ACCEPTED[name]}" if name in ACCEPTED else "❌ non conforme")
            out.append(ValidationCheck(name=name, kind="critère", status=status, satisfied=ok, detail=c.detail))
        out.append(ValidationCheck(
            name="P10.3 A7 technique", kind="info", status="ℹ️ information", satisfied=True,
            detail="Tests (etl/tests/test_p10c.py), contrat et construction de l'onglet vérifiés par la CI."))
        out.append(ValidationCheck(
            name="Confiance P10.3 (règle D-AQ)", kind="info", status="ℹ️ information", satisfied=True,
            detail=f"{amp.confidence} — {amp.confidence_reason}"))
        # La synthèse (cmp-terres-oceans) affirme que la France et la Gironde se réchauffent plus vite que la moyenne
        # des terres : à revérifier à chaque calcul, sans quoi l'affirmation deviendrait fausse en silence (D-AH).
        lands = {s.label: s.land.k for s in amp.scales}
        above = all(k.ci_low is not None and k.ci_low > 1 for k in lands.values())
        out.append(ValidationCheck(
            name="D-AH cohérence de cmp-terres-oceans", kind="critère",
            status="✅ conforme" if above else "❌ non conforme", satisfied=above,
            detail=("facteur contre les terres émergées, borne basse > 1 : " + " ; ".join(
                f"{lab} [{k.ci_low:.2f} ; {k.ci_high:.2f}]".replace(".", ",") for lab, k in lands.items())
                + ("" if above else " — reformuler cmp-terres-oceans (etl/config/synthese.yaml) et la faire relire"))))
        inds |= {"temperature-gistemp-monde", "temperature-hadcrut5-monde", "temperature-berkeley-monde",
                 "tm-france", "tm-annuelle-gironde"}
    return out, sorted(inds)


def main(out_dir: Path = PROCESSED_DIR) -> int:
    path = out_dir / "demonstration.json"
    if not path.exists():
        print("demonstration.json absent : validation P10 non exécutée.")
        return 0
    demo = Demonstration.model_validate_json(path.read_text(encoding="utf-8"))
    cs, inds = checks(demo)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P10 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p10` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P10).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    rep = ValidationReport(phase="p10", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=inds, checks=cs)
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
