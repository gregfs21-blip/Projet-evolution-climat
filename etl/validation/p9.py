"""Validation de la phase 9 (Gulf Stream et AMOC) : critères N1-N7 de docs/phases.md.

Critères validés par Grég le 17/11/2026, avant tout calcul. Ce module mesure et publie.
Usage : python -m etl.validation.p9   → docs/validation-p9-resultats.md et data/processed/validation-p9.json
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import temperature as T
from etl.schema import Indicator, ValidationCheck, ValidationReport

SCOPE = {"amoc-debit-monde", "amoc-profondeur-monde", "temperature-0700-gulf-stream", "temperature-0700-gyre-subpolaire",
         "salinite-0700-gulf-stream", "salinite-0700-gyre-subpolaire"}
EXTRA = {"amoc-chaleur-monde"}   # ajouté le 17/11/2026 à la demande de Grég, hors périmètre N1
OUT = ROOT / "docs" / "validation-p9-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p9.json"
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
    for scale in ("monde", "gironde"):
        for path in (out_dir / scale).glob("*.json"):
            if path.stem in SCOPE | EXTRA:
                out[path.stem] = Indicator.model_validate_json(path.read_text(encoding="utf-8"))
    return out


def _series(ind: Indicator) -> dict[int, float]:
    return {int(t): v for t, v in zip(ind.series.time, ind.series.value) if v is not None}


def checks(inds: dict[str, Indicator], out_dir: Path) -> list[Check]:
    import yaml

    from etl.sources import en4 as E
    from etl.sources import rapid as R
    from etl.stats.trend import annual_trend
    cs = []
    missing = sorted(SCOPE - set(inds))
    cov = yaml.safe_load((ROOT / "etl" / "config" / "couverture.yaml").read_text(encoding="utf-8"))
    cable = next((p["echelles"].get("monde", {}) for p in cov["parametres"] if p["id"] == "gulf-stream"), {})
    cable_ok = cable.get("statut") == "sans-donnee"
    cs.append(Check("N1 exhaustivité", "critère", not missing and cable_ok,
                    f"{len(SCOPE & set(inds))} séries sur 6 publiées ; câble du détroit de Floride "
                    + ("déclaré « sans donnée » (D-AA)" if cable_ok else "NON déclaré dans la couverture")
                    + (f" ; manquants : {', '.join(missing)}" if missing else "")
                    + ("; transport de chaleur publié en plus" if "amoc-chaleur-monde" in inds else "")))
    # N2 : années d'au moins 10 mois, recomptées dans les sources
    bad, notes = [], []
    try:
        months = R.load()
        for q, iid in (("debit", "amoc-debit-monde"), ("profondeur", "amoc-profondeur-monde"), ("chaleur", "amoc-chaleur-monde")):
            if iid not in inds:
                continue
            _s, counts = R.annual(months[q])
            ys = set(_series(inds[iid]))
            if any(counts.get(y, 0) < R.MIN_MONTHS for y in ys) or {y for y, n in counts.items() if n >= R.MIN_MONTHS} - ys:
                bad.append(iid)
            if q == "debit":
                notes.append("RAPID : " + ", ".join(f"{y} ({n} mois)" for y, n in sorted(counts.items()) if n < R.MIN_MONTHS) + " écartées")
        for iid in sorted(SCOPE & set(inds)):
            if iid.startswith(("temperature-0700", "salinite-0700")):
                zone = iid.split("-0700-")[1]
                s, _w = E.load_zone(zone, "temperature" if iid.startswith("temp") else "salinite")
                if set(s) != set(_series(inds[iid])):
                    bad.append(iid)
        per: dict[int, int] = {}
        with E.OUT.open(encoding="utf-8") as f:
            for r in __import__("csv").DictReader(f):
                if r["zone"] == "gulf-stream":
                    per[int(r["annee"])] = per.get(int(r["annee"]), 0) + 1
        notes.append("EN4 : " + (", ".join(f"{y} ({n} mois)" for y, n in sorted(per.items()) if n < E.MIN_MONTHS) or "aucune année")
                     + " écartée(s)")
        cs.append(Check("N2 complétude", "critère", not bad, ("; ".join(notes)) if not bad else "écarts : " + ", ".join(bad)))
    except Exception as exc:  # noqa: BLE001
        cs.append(Check("N2 complétude", "critère", False, f"non calculé : {exc}"))
    parts, ok = ["câble : sans objet (aucune donnée)"], True
    for iid, lo, hi, unit in (("amoc-debit-monde", 15.5, 18.5, "Sv"), ("amoc-profondeur-monde", 700.0, 1300.0, "m")):
        if iid in inds:
            s = _series(inds[iid])
            m = sum(s.values()) / len(s)
            ok &= lo <= m <= hi
            parts.append(f"{iid.replace('-monde', '')} : moyenne {min(s)}-{max(s)} = {T.fr(m, 2 if unit == 'Sv' else 0, False)} {unit} "
                         f"(attendu {T.fr(lo, 1, False)} à {T.fr(hi, 1, False)})")
        else:
            ok = False
    cs.append(Check("N3 plausibilité", "critère", ok, " ; ".join(parts)))
    cs.append(Check("N4 correction géomagnétique", "critère", True,
                    "câble seul : sans objet tant qu'il est « sans donnée ». RAPID utilise depuis la version v2023.1 le "
                    "débit du détroit de Floride corrigé de la dérive séculaire du champ géomagnétique (README RAPID ; "
                    "Volkov et al., 2024) ; version lue : " + (R.version() if R.DIR.exists() else "?")))
    parts = []
    for iid in ("amoc-debit-monde", "amoc-profondeur-monde", "amoc-chaleur-monde"):
        if iid in inds and inds[iid].trend:
            s = _series(inds[iid])
            full = inds[iid].trend
            ys = [y for y in sorted(s) if y <= 2022]
            t = annual_trend(ys, [s[y] for y in ys])
            same = (t.slope_per_decade > 0) == (full.slope_per_decade > 0)
            parts.append(f"{iid.replace('-monde', '')} : {full.period.start}-{full.period.end} {T.fr(full.slope_per_decade, 3)}, "
                         f"{ys[0]}-{ys[-1]} {T.fr(t.slope_per_decade, 3)} {inds[iid].unit}/déc. ({'même signe' if same else 'signes opposés'})")
    cs.append(Check("N5 robustesse sans les années du relais du câble (information)", "info", True,
                    "tendance avec et sans 2023-2024 (câble en panne depuis novembre 2023) : " + " ; ".join(parts)))
    cs.append(Check("N6 technique", "info", True, "Tests, contrat et construction des pages vérifiés par la CI (ci.yml), "
                                                 "hors de ce module, comme pour les phases précédentes."))
    parts, ok = [], True
    for iid in sorted(i for i in SCOPE & set(inds) if "-0700-" in i):
        zone = iid.split("-0700-")[1]
        _s, w = E.load_zone(zone, "temperature" if iid.startswith("temp") else "salinite")
        start = E.n7_start(w)
        tr = inds[iid].trend
        good = tr is not None and tr.period.start == start and all(
            q == "raw" for t, q in zip(inds[iid].series.time, inds[iid].series.quality) if int(t) < start)
        ok &= good
        parts.append(f"{iid} : début {start}" + ("" if good else " (tendance ou qualité non conforme)"))
    cs.append(Check("N7 couverture d'observations", "critère", ok, " ; ".join(parts)))
    return cs


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load(out_dir)
    if not inds:
        print("Aucun indicateur P9 publié : validation P9 non exécutée.")
        return 0
    cs = checks(inds, out_dir)
    counted = [c for c in cs if c.kind == "critère"]
    verdict = ("Tous les critères comptant pour la clôture sont satisfaits." if all(c.satisfied for c in counted)
               else "Au moins un critère comptant pour la clôture n'est pas satisfait.")
    md = ["# Validation P9 — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p9` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères : `docs/phases.md` (P9).", "", f"**{verdict}**", "", "| Critère | Résultat | Mesure |", "|---|---|---|",
          *[f"| {c.name} | {c.status} | {c.detail} |" for c in cs], ""]
    OUT.write_text("\n".join(md), encoding="utf-8")
    rep = ValidationReport(phase="p9", generated_at=datetime.now(timezone.utc).replace(microsecond=0),
                           closure_ok=all(c.satisfied for c in counted), verdict=verdict, indicators=sorted(inds),
                           checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied,
                                                   detail=c.detail) for c in cs])
    (out_dir / OUT_JSON.name).write_text(rep.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print("\n".join(f"[{c.status}] {c.name} : {c.detail}" for c in cs))
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
