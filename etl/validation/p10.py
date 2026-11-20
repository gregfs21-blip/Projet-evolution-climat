"""Validation de la phase 10 (démonstration), P10.1 : critères O1-O9 de docs/phases.md.

Critères validés par Grég le 17/11/2026, avant tout calcul (D-AF). Les mesures O1-O8 sont faites par
etl/demonstration.py, qui les écrit dans data/processed/demonstration.json ; ce module les relit, contrôle que la
confiance publiée suit la règle D-AG, et publie le rapport.
Usage : python -m etl.validation.p10   → docs/validation-p10-resultats.md et data/processed/validation-p10.json
"""

from __future__ import annotations

import json

from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, ROOT
from etl.demonstration import _f
from etl.schema import Demonstration, ValidationCheck, ValidationReport

OUT = ROOT / "docs" / "validation-p10-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p10.json"
# Écarts acceptés par Grég après calcul (docs/phases.md, journal P10). Un écart accepté clôt la sous-phase mais ne
# relève pas la confiance (règle D-AG, pratique de P2b) : demonstration.json garde le résultat brut du critère.
ACCEPTED: dict[str, str] = {
    "O8 robustesse": "écart accepté par Grég le 18/11/2026 (D-AI) : seule la variante « forçage anthropique à 5 % » "
                     "sort de la fourchette, l'estimateur AR(1) y dégénère (docs/validation-p10.md)",
    "P10.3 A2 ajustement": "écart accepté par Grég le 19/11/2026 (D-AR) : Ljung-Box de la Gironde à 10 ans (p = 0,03), "
                           "dû à une seule autocorrélation à 10 ans déjà présente dans la série ; A3 tient avec les "
                           "erreurs de Newey-West (docs/validation-p10.md)",
}
# Critères de P10.4 recadrés en P10.4b par décision de Grég après calcul (D-AV, 20/11/2026) : ni acceptés ni corrigés,
# leur résultat reste publié ; ils ne bloquent la clôture que si P10.4b n'est pas publiée.
# Chaque critère recadré suit son correspondant de P10.4b : il n'est traité que si celui-ci est conforme ou accepté.
REFRAMED: dict[str, str] = {
    "P10.4 C2 vapeur d'eau": "B2",
    "P10.4 C4 niveau marin": "B3",
    "P10.4 C6 robustesse": "B4",
}
# Analyses de l'onglet dont la synthèse tient compte (affirmations `limite-attribution` et `limite-projections` de
# etl/config/synthese.yaml, D-AH). Publier une autre analyse (P10.4 cohérence physique, P10.5 projections) rend ces
# affirmations à revoir : ce contrôle échoue jusqu'à leur reformulation, relue (M6), et la mise à jour de cette liste
# (P10.2 et P10.3 ajoutées le 19/11/2026 après relecture, docs/relecture-p8.md).
SYNTHESIS_COVERS = {"p10.1", "p10.2", "p10.3"}


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
        periods = [f"{s.land.period.start}-{s.land.period.end}" for s in amp.scales]
        syn_path = PROCESSED_DIR / "synthese.json"
        claim = ""
        if syn_path.exists():
            syn = json.loads(syn_path.read_text(encoding="utf-8"))
            claim = next((c["text"] for sec in syn["sections"] for g in sec["groups"] for c in g["claims"]
                          if c["id"] == "cmp-terres-oceans"), "")
        dated = all(p in claim for p in periods)
        above = all(k.ci_low is not None and k.ci_low > 1 for k in lands.values()) and dated
        out.append(ValidationCheck(
            name="D-AH cohérence de cmp-terres-oceans", kind="critère",
            status="✅ conforme" if above else "❌ non conforme", satisfied=above,
            detail=("facteur contre les terres émergées, borne basse > 1 : " + " ; ".join(
                f"{lab} [{_f(k.ci_low, 2)} ; {_f(k.ci_high, 2)}]" for lab, k in lands.items())
                + f" ; périodes citées dans l'affirmation ({', '.join(periods)}) {'présentes' if dated else 'ABSENTES'}"
                + ("" if above else " — reformuler cmp-terres-oceans (etl/config/synthese.yaml) et la faire relire"))))
        inds |= {"temperature-gistemp-monde", "temperature-hadcrut5-monde", "temperature-berkeley-monde",
                 "tm-france", "tm-annuelle-gironde"}
    # P10.4 — cohérence physique (critères C1-C7, D-AT)
    coh = next((a.coherence for a in demo.analyses if a.phase == "p10.4" and a.coherence), None)
    cob = next((a.coherence for a in demo.analyses if a.phase == "p10.4b" and a.coherence), None)
    if coh is not None:
        b_ok = {}
        if cob is not None:
            for c in cob.criteria:
                b_ok[c.id] = c.satisfied or f"P10.4b {c.id} {c.label.lower()}" in ACCEPTED
        for c in coh.criteria:
            name = f"P10.4 {c.id} {c.label.lower()}"
            # D-AV : un critère recadré n'est ni accepté ni corrigé ; il suit son correspondant de P10.4b.
            follow = REFRAMED.get(name)
            reframed = follow is not None and cob is not None
            ok = c.satisfied or name in ACCEPTED or (reframed and b_ok.get(follow, False))
            status = ("✅ conforme" if c.satisfied else f"☑ {ACCEPTED[name]}" if name in ACCEPTED
                      else (f"↪ non conforme, recadré en P10.4b (D-AV), suit {follow} "
                            f"({'✅ ou accepté' if b_ok.get(follow) else '❌'})") if reframed else "❌ non conforme")
            out.append(ValidationCheck(name=name, kind="critère", status=status, satisfied=ok, detail=c.detail))
        out.append(ValidationCheck(
            name="P10.4 C7 technique", kind="info", status="ℹ️ information", satisfied=True,
            detail="Tests (etl/tests/test_p10d.py), contrat et construction de l'onglet vérifiés par la CI."))
        out.append(ValidationCheck(
            name="Confiance P10.4 (règle D-AT)", kind="info", status="ℹ️ information", satisfied=True,
            detail=f"{coh.confidence} — {coh.confidence_reason}"))
        inds |= {"sst-hadsst-monde", "sst-noaa-monde", "tlt-rss-monde", "tlt-uah-monde", "niveau-mer-monde",
                 "ohc-2000-monde", "desequilibre-energetique-monde"}
    # P10.4b — recadrage de V et N (critères B1-B5, D-AX)
    if cob is not None:
        for c in cob.criteria:
            name = f"P10.4b {c.id} {c.label.lower()}"
            ok = c.satisfied or name in ACCEPTED
            status = "✅ conforme" if c.satisfied else (f"☑ {ACCEPTED[name]}" if name in ACCEPTED else "❌ non conforme")
            out.append(ValidationCheck(name=name, kind="critère", status=status, satisfied=ok, detail=c.detail))
        out.append(ValidationCheck(
            name="P10.4b B5 technique", kind="info", status="ℹ️ information", satisfied=True,
            detail="Tests (etl/tests/test_p10d.py), contrat et construction de l'onglet vérifiés par la CI."))
        out.append(ValidationCheck(
            name="Confiance P10.4b (règle D-AX)", kind="info", status="ℹ️ information", satisfied=True,
            detail=f"{cob.confidence} — {cob.confidence_reason}"))
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
