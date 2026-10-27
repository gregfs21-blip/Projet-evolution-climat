"""Validation de la phase 2b (pluies intenses, demande en eau, sécheresse) : critères F1-F11 de docs/phases.md.

Critères, seuils et références fixés le 26/10/2026 et validés par Grég avant tout calcul. Ce module mesure et publie ;
il n'interprète pas. F8 est aussi appliqué, en diagnostic (« info »), aux indices de température de P2a (décision D-H).

Usage : python -m etl.validation.p2b   → docs/validation-p2b-resultats.md et data/processed/validation-p2b.json
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import eau as E
from etl.indicators import extremes as X
from etl.indicators import pluie as P
from etl.schema import Indicator, ValidationCheck, ValidationReport

RAIN = tuple(P.INDICES)
WATER = ("etp", "bilan-hydrique", "spei12", "mois-secs")
OUT = ROOT / "docs" / "validation-p2b-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p2b.json"
F5_TOLERANCE = 0.5        # mm

# Écarts acceptés par Grég le 26/10/2026, APRÈS calcul (analyse : docs/validation-p2b.md). Un écart accepté compte
# comme satisfait pour la clôture ; il ne relève pas la confiance des indicateurs concernés.
ACCEPTED = {
    "F4 validation externe (R6, ETP)": "écart accepté le 26/10/2026 (formule de Hargreaves)",
    "F6 cohérence inter-stations (r10mm)": "écart expliqué le 26/10/2026 (aucune pente significative)",
}


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


def load_indicators(out_dir: Path) -> list[Indicator]:
    out = []
    for path in sorted((out_dir / "gironde").glob("*.json")):
        ind = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
        if ind.variable and ind.variable.id in RAIN + WATER:
            out.append(ind)
    return out


def _sign(x: float) -> int:
    return 0 if x == 0 else (1 if x > 0 else -1)


def checks(inds: list[Indicator], raw_dir: Path) -> tuple[list[Check], list[str]]:
    raw = str(raw_dir)
    cs: list[Check] = []
    tables: list[str] = []
    by_id = {i.id: i for i in inds}

    # F1 — exhaustivité
    ok, excluded = P.eligible(raw)
    members, comp_excl = P.composite_members(raw)
    expected = {f"{x}-{P.station_name(P.rain_daily(p, raw).station)[1]}" for p in ok for x in RAIN}
    expected |= {f"{x}-gironde" for x in RAIN} if len(members) >= 3 else set()
    expected |= {f"{v}-{P.station_name(E.station_water(p, raw)[5])[1]}" for p in E.POSTES for v in WATER}
    missing = sorted(expected - set(by_id))
    cs.append(Check("F1 exhaustivité", "critère", not missing,
                    f"{len(ok)} postes de pluie retenus, {len(members)} au composite 1961-2017"
                    + (f" (hors composite : {', '.join(comp_excl)})" if comp_excl else "")
                    + (f" ; exclus : {excluded}" if excluded else "") + f" ; 3 postes ETP/SPEI ; "
                    + (f"manquants : {', '.join(missing)}" if missing else f"{len(expected)} indicateurs attendus, tous publiés")))

    cs.append(Check("F2 complétude", "info", True,
                    "Appliquée par le code : quotidien ETCCDI, correction B′ sur mois complets seulement, années de 12 mois, "
                    "cumuls SPEI interrompus par tout mois manquant."))
    cs.append(Check("F3 brut ≠ homogénéisé", "critère", True,
                    f"{len(inds)} indicateurs validés par le contrat : aucune tendance ni normale sur une année brute (règle C2)."))

    # F4 — R6 (ETP)
    etps = [i for i in inds if i.variable.id == "etp"]
    lines = [f"{i.place.name} : {i.reference_check.measured if i.reference_check else '—'} mm/déc."
             for i in etps]
    sat = bool(etps) and all(i.reference_check and i.reference_check.satisfied for i in etps)
    cs.append(Check("F4 validation externe (R6, ETP)", "critère", sat,
                    "Attendu [+16 ; +30] mm/déc. sur 1962-2019 ; mesuré : " + "; ".join(lines)
                    + ". Pluies intenses : pas de référence (R7 abandonnée), confiance au plus « moyenne »."))

    # F5 — cohérence du correctif
    worst, n_months = 0.0, 0
    for p in ok:
        rd = P.rain_daily(p, raw)
        for (y, m), f in rd.factors.items():
            total = sum(rd.corrected[d] for d in P.days_of(y, m))
            worst = max(worst, abs(total - rd.lsh_month[(y, m)]))
            n_months += 1
    cs.append(Check("F5 cohérence du correctif", "critère", worst <= F5_TOLERANCE,
                    f"{n_months} mois corrigés ; écart maximal au cumul LSH : {worst:.3f} mm (tolérance {F5_TOLERANCE} mm)."))

    # F6 — cohérence inter-stations (R10mm, ETP)
    for var in ("r10mm", "etp"):
        sts = [i for i in inds if i.variable.id == var and i.place.kind == "station" and i.trend]
        signs = {i.place.name: _sign(i.trend.slope_per_decade) for i in sts}
        same = len(set(s for s in signs.values() if s != 0)) <= 1
        cs.append(Check(f"F6 cohérence inter-stations ({var})", "critère", same,
                        ", ".join(f"{k} {'+' if v > 0 else '−' if v < 0 else '0'}" for k, v in signs.items())))

    # F7 — contrôle A
    rows, bad, na = [], [], []
    for i in [i for i in inds if i.variable.id in RAIN]:
        a = next((t for t in i.alt_trends if t.label.startswith("Contrôle A")), None)
        b = next((t for t in i.alt_trends if t.label.startswith("Série corrigée sur la période du contrôle A")), None)
        if a is None or b is None:
            na.append(i.id)
            continue
        agree = X.control_agrees(a, b)
        if not agree:
            bad.append(i.id)
        rows.append(f"| {i.id} | {a.period.start}-{a.period.end} | {a.slope_per_decade:+.2f} | {b.slope_per_decade:+.2f} | "
                    f"{'oui' if agree else 'non'} |")
    cs.append(Check("F7 robustesse méthode (A et B′)", "critère", not bad and not na,
                    f"{len(rows) - len(bad)} concordants sur {len(rows)} évaluables ; non concordants : {', '.join(bad) or 'aucun'} ; "
                    f"non évaluables : {', '.join(na) or 'aucun'}."))
    tables += ["", "### F7 — contrôle A", "", "| Indicateur | Période A | Pente A | Pente B′ | Concordant |", "|---|---|---|---|---|", *rows]

    # F8 — période ancienne (P2b)
    rows, ruptures = [], []
    for p in ok:
        rd = P.rain_daily(p, raw)
        for x in RAIN:
            idx = P.INDICES[x]
            ser = {y: v for y, v in rd.index(idx).items() if y in rd.hom()}
            r = P.f8(ser, P._others(p, idx, raw), rd.last_break_regime, idx.unit)
            if r["status"] == "rupture":
                ruptures.append(f"{rd.station.name} {x}")
            rows.append(f"| {rd.station.name} | {x} | {r['status']} | {r['detail']} |")
    cs.append(Check("F8 période ancienne (P2b)", "critère", not ruptures,
                    f"ruptures établies : {', '.join(ruptures) or 'aucune'} (tendance alors limitée à la période postérieure)."))
    tables += ["", "### F8 — période ancienne, pluies", "", "| Poste | Indice | Résultat | Détail |", "|---|---|---|---|", *rows]

    # F8 — diagnostic P2a (décision D-H)
    rows, ruptures = [], []
    for key, idx in X.INDICES.items():
        sds = {sid: X.station_daily(idx.variable, sid, raw_dir) for sid in X.stations_for(idx.variable, raw_dir)}
        ser = {sid: {y: float(v) for y, v in X.counts(sd, idx).items() if sd.year_status.get(y) == "homogenized"}
               for sid, sd in sds.items()}
        for sid, sd in sds.items():
            r = P.f8(ser[sid], [s for o, s in ser.items() if o != sid], sd.last_break_regime, "jours")
            if r["status"] == "rupture":
                ruptures.append(f"{sd.station.name} {key}")
            rows.append(f"| {sd.station.name} | {key} | {r['status']} | {r['detail']} |")
    cs.append(Check("F8 diagnostic sur P2a (extrêmes de température)", "info", True,
                    f"ruptures établies : {', '.join(ruptures) or 'aucune'}. Diagnostic seulement : ne modifie pas P2a."))
    tables += ["", "### F8 — diagnostic P2a", "", "| Poste | Indice | Résultat | Détail |", "|---|---|---|---|", *rows]

    rare = [i.id for i in inds if i.variable.id in ("r10mm", "r20mm") and any("Indice rare" in l for l in i.limitations)]
    cs.append(Check("F9 indices rares", "info", True, f"{len(rare)} indice(s) rare(s) : {', '.join(rare) or 'aucun'}."))

    # F10 — SPEI standardisé sur la période de calage
    lines, ok10 = [], True
    for p in E.POSTES:
        s3, s12 = E.spei_tables(p, raw)
        for k, s in ((3, s3), (12, s12)):
            v = np.array([x for (y, m), x in s.items() if E.CALIBRATION[0] <= y <= E.CALIBRATION[1]])
            good = abs(v.mean()) <= 0.05 and abs(v.std() - 1) <= 0.1
            ok10 &= good
            lines.append(f"{E.station_water(p, raw)[5].name} SPEI-{k} : moyenne {v.mean():+.3f}, écart-type {v.std():.3f}")
    cs.append(Check("F10 contrôle du SPEI", "critère", ok10, " ; ".join(lines)))
    cs.append(Check("F11 technique", "info", True, "Tests, CI et contrat vérifiés par les workflows."))
    return cs, tables


def build_report(cs: list[Check], verdict: str, indicators: list[str]) -> ValidationReport:
    counted = [c for c in cs if c.kind == "critère"]
    return ValidationReport(
        phase="p2b", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
        closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=indicators,
        checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied, detail=c.detail) for c in cs],
    )


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load_indicators(out_dir)
    if not inds:
        print("Aucun indicateur P2b publié : validation P2b non exécutée.")
        return 0
    cs, tables = checks(inds, raw_dir)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P2b — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p2b` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères et seuils : `docs/phases.md` (P2b).", "", f"**{verdict}**", "",
          "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], *tables, ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    (out_dir / OUT_JSON.name).write_text(build_report(cs, verdict, [i.id for i in inds]).model_dump_json(indent=2) + "\n",
                                         encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
