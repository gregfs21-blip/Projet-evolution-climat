"""Validation de la phase 2a (extrêmes de température) : critères E1-E9 de docs/phases.md.

Les critères et les seuils sont ceux de docs/phases.md, fixés le 23/10/2026 avant tout calcul.
Ce module mesure et publie ; il n'interprète pas. L'analyse des écarts sera rédigée à la main dans
docs/validation-p2a.md.

E4 (validation externe) : références fixées le 23/10/2026 par Grég, avant tout calcul sur données réelles
(voir REFERENCES). Si REFERENCES est vide, E4 est publié « en attente » et compte comme non satisfait.

Usage : python -m etl.validation.p2a   → écrit docs/validation-p2a-resultats.md et data/processed/validation-p2a.json
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path

from etl.context import PROCESSED_DIR, RAW_DIR, ROOT
from etl.indicators import extremes as X
from etl.schema import Indicator, ValidationCheck, ValidationReport

# E4 : références fixées le 23/10/2026 (décision de Grég), AVANT tout calcul P2a sur données réelles.
# Deux sources concordantes citant les données Météo-France (ClimatHD), de seconde main :
#   - CNPF Nouvelle-Aquitaine, « Le changement climatique et la forêt en Nouvelle-Aquitaine », 2023, p. 5-6 :
#     journées chaudes (TX > 25 °C) +4 à +5 j/déc. sur la côte, +6 à +8 j/déc. à l'intérieur ; gelées −1 à −2 j/déc. ;
#     période 1960-2010 ;
#   - PNR Périgord-Limousin, diagnostic de vulnérabilité, oct. 2025, p. 28 (ClimatHD, 1961-2018) : mêmes ordres de grandeur.
# Fourchettes publiées, prises telles quelles (pas d'élargissement), comme pour C3 en P1.
# `stations` : postes moyennés ; None = membres du composite à réseau constant de la variable.
REFERENCES: dict[str, dict] = {
    "R3 littoral": {"variable": "TX", "op": ">", "threshold": 25.0, "definition": "journées chaudes (TX > 25 °C), littoral",
                    "stations": ["33236002", "33529001"], "range": (4.0, 5.0)},          # Cap-Ferret, Cazaux
    "R3 intérieur": {"variable": "TX", "op": ">", "threshold": 25.0, "definition": "journées chaudes (TX > 25 °C), intérieur",
                     "stations": ["33281001", "33550001"], "range": (6.0, 8.0)},         # Mérignac, Villenave-d'Ornon
    "R4": {"variable": "TN", "op": "<=", "threshold": 0.0, "definition": "jours de gel (TN ≤ 0 °C), composite",
           "stations": None, "range": (-2.0, -1.0)},
}

E5_TOLERANCE = 0.05     # °C
P2A_VARIABLES = tuple(X.INDICES)
OUT = ROOT / "docs" / "validation-p2a-resultats.md"
OUT_JSON = PROCESSED_DIR / "validation-p2a.json"


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str
    kind: str = "critère"
    pending: bool = False

    @property
    def status(self) -> str:
        if self.kind == "info":
            return "ℹ information"
        if self.pending:
            return "⏳ en attente"
        return "✅ conforme" if self.passed else "❌ écart"

    @property
    def satisfied(self) -> bool:
        return self.passed and not self.pending


def external_validation_passed(raw_dir: Path = RAW_DIR) -> bool:
    """E4. Faux tant que les références ne sont pas fixées."""
    if not REFERENCES:
        return False
    return all(c.satisfied for c in _e4_cached(str(raw_dir)))


@lru_cache(maxsize=4)
def _e4_cached(raw_dir: str) -> tuple[Check, ...]:
    return tuple(e4(Path(raw_dir)))


def e4(raw_dir: Path) -> list[Check]:
    if not REFERENCES:
        return [Check("E4 validation externe (ClimatHD)", False,
                      "références R3/R4 en attente de confirmation sur ClimatHD (décision D-C du 23/10/2026)", pending=True)]
    out = []
    w = X.CLIMATHD_WINDOW
    names = X.T.station_config()
    years = list(range(w.start, w.end + 1))
    for key, ref in REFERENCES.items():
        idx = X.IndexDef(key, ref["variable"], ref["op"], ref["threshold"], key, ref["definition"])
        if ref["stations"] is None:
            members, _ = X.composite_members(idx.variable, raw_dir)
        else:
            members = [X.station_daily(idx.variable, sid, raw_dir) for sid in ref["stations"]]
        name = f"E4 {key} : {ref['definition']} {w.start}-{w.end}"
        incomplete = [names.get(sd.station.id, {}).get("name", sd.station.id) for sd in members
                      if any(sd.year_status.get(y) != "homogenized" for y in years)]
        if incomplete or not members:
            out.append(Check(name, False, f"non évaluable : années manquantes ou non corrigées pour {incomplete}"))
            continue
        per = [X.counts(sd, idx) for sd in members]
        t = X.annual_trend(years, [sum(c[y] for c in per) / len(per) for y in years], label="E4")
        lo, hi = ref["range"]
        who = ", ".join(names.get(sd.station.id, {}).get("name", sd.station.id) for sd in members)
        out.append(Check(name, lo <= t.slope_per_decade <= hi,
                         f"pente de Sen {t.slope_per_decade:+.2f} j/déc. (IC 95 % {t.slope_ci_low:+.2f} à "
                         f"{t.slope_ci_high:+.2f}), attendu [{lo:g} ; {hi:g}] ; {who}"))
    return out


def in_scope(ind: Indicator) -> bool:
    return ind.variable is not None and ind.variable.id in P2A_VARIABLES


def load_indicators(out_dir: Path = PROCESSED_DIR) -> list[Indicator]:
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    inds = [Indicator.model_validate_json((out_dir / e["path"]).read_text(encoding="utf-8")) for e in manifest["indicators"]]
    return [i for i in inds if in_scope(i)]


def checks(inds: list[Indicator], raw_dir: Path) -> tuple[list[Check], list[str]]:
    out: list[Check] = []
    lines: list[str] = []
    stations = [i for i in inds if i.place and i.place.kind == "station"]

    # E1 — exhaustivité : chaque indice à chaque poste disposant de la série LSH de sa variable.
    expected = {(ix, sid) for ix, d in X.INDICES.items() for sid in X.stations_for(d.variable, raw_dir)}
    got = {(i.variable.id, i.stations[0].id) for i in stations}
    missing = sorted(expected - got)
    names = X.T.station_config()
    no_lsh = sorted({(d.variable, names[s]["name"]) for d in X.INDICES.values() for s in names
                     if s not in X.stations_for(d.variable, raw_dir)})
    out.append(Check("E1 exhaustivité", not missing,
                     f"{len(got)}/{len(expected)} couples indice × poste traités"
                     + (f" ; manquants : {missing}" if missing else "")
                     + (" ; exclus faute de série LSH (ni correction B ni dates de ruptures) : "
                        + ", ".join(f"{v} {n}" for v, n in no_lsh) if no_lsh else "")))

    # E2 — complétude : années écartées par la règle ETCCDI, par station et variable.
    lines += ["", "### E2 — Années complètes (règle ETCCDI) et corrigées, par poste", "",
              "| Variable | Poste | Années complètes | dont corrigées | Première | Dernière corrigée |", "|---|---|---|---|---|---|"]
    for var in ("TN", "TX"):
        for sid in X.stations_for(var, raw_dir):
            sd = X.station_daily(var, sid, raw_dir)
            hom = sd.hom_years()
            lines.append(f"| {var} | {names[sid]['name']} | {len(sd.year_status)} | {len(hom)} | "
                         f"{min(sd.year_status) if sd.year_status else '—'} | {hom[-1] if hom else '—'} |")
    out.append(Check("E2 complétude ETCCDI", True, "règle appliquée à la construction (mois manquant au-delà de 3 jours "
                     "absents, année manquante si un mois l'est) ; détail par poste ci-dessous"))

    # E3 — brut ≠ homogénéisé : garanti par le schéma (règle C2), vérifié ici sur les JSON publiés.
    bad = [i.id for i in inds for t in [i.trend, *i.alt_trends] if t
           for y, q in zip(i.series.time, i.series.quality or []) if q == "raw" and t.period.start <= int(y) <= t.period.end
           and not t.label.startswith("Contrôle A")]
    out.append(Check("E3 brut exclu des tendances", not bad,
                     "aucune tendance de série corrigée ne contient d'année brute" if not bad else f"en défaut : {sorted(set(bad))}"))

    # E4 — validation externe.
    out += e4(raw_dir)

    # E5 — la correction reproduit la moyenne mensuelle LSH (contrôle du calcul).
    worst, where = 0.0, ""
    for var in ("TN", "TX"):
        for sid in X.stations_for(var, raw_dir):
            sd = X.station_daily(var, sid, raw_dir)
            for y in sd.hom_years():
                corr = [sum(sd.corrected[d] for d in X.days_of(y, m) if d in sd.corrected)
                        / sum(d in sd.corrected for d in X.days_of(y, m)) for m in range(1, 13)]
                ref = [sd.lsh_month[(y, m)] for m in range(1, 13)]
                gap = abs(sum(corr) / 12 - sum(ref) / 12)
                if gap > worst:
                    worst, where = gap, f"{var} {names[sid]['name']} {y}"
    out.append(Check("E5 cohérence du correctif", worst <= E5_TOLERANCE,
                     f"écart annuel maximal corrigé − LSH : {worst:.4f} °C ({where or '—'}), tolérance {E5_TOLERANCE} °C"))

    # E6 — même signe de tendance à toutes les stations (TX ≥ 25 °C et gel).
    for ix in ("jours-tx25", "jours-gel"):
        signs = {i.place.name: i.trend.slope_per_decade for i in stations if i.variable.id == ix and i.trend}
        pos = [n for n, v in signs.items() if v > 0]
        neg = [n for n, v in signs.items() if v < 0]
        ok = not (pos and neg)
        out.append(Check(f"E6 même signe {ix}", ok, f"{len(pos)} hausse(s), {len(neg)} baisse(s), "
                         f"{len(signs) - len(pos) - len(neg)} nulle(s)" + ("" if ok else f" ; hausse : {pos} ; baisse : {neg}")))

    # E7 — concordance A / B.
    lines += ["", "### E7 — Contrôle A (brut après dernière rupture) contre B (corrigé), même période", "",
              "| Indicateur | Période | Pente A | IC A | Pente B | IC B | Concordance |", "|---|---|---|---|---|---|---|"]
    disagree, unevaluated = [], []
    for i in inds:
        a = next((t for t in i.alt_trends if t.label.startswith("Contrôle A")), None)
        b = next((t for t in i.alt_trends if t.label.startswith("Série corrigée sur la période du contrôle A")), None)
        if a is None or b is None:
            unevaluated.append(i.id)
            lines.append(f"| {i.id} | — | — | — | — | — | non évaluable (période trop courte) |")
            continue
        ok = X.control_agrees(a, b)
        if not ok:
            disagree.append(i.id)
        lines.append(f"| {i.id} | {a.period.start}-{a.period.end} | {a.slope_per_decade:+.2f} | {a.slope_ci_low:+.2f} à "
                     f"{a.slope_ci_high:+.2f} | {b.slope_per_decade:+.2f} | {b.slope_ci_low:+.2f} à {b.slope_ci_high:+.2f} | "
                     f"{'oui' if ok else '**non**'} |")
    out.append(Check("E7 concordance des méthodes", not disagree and not unevaluated,
                     f"{len(inds) - len(disagree) - len(unevaluated)}/{len(inds)} concordants ; "
                     f"{len(disagree)} discordant(s) ; {len(unevaluated)} non évaluable(s)"))

    # E8 — robustesse au code qualité 9 : même signe et même significativité sans ces valeurs.
    changed = []
    lines += ["", "### E8 — Sans les valeurs de code qualité 9", "",
              "| Indicateur | Pente | Significative | Pente sans code 9 | Significative | Conclusion modifiée |", "|---|---|---|---|---|---|"]
    for i in stations:
        if not i.trend:
            continue
        idx = X.INDICES[i.variable.id]
        sd = X.station_daily(idx.variable, i.stations[0].id, raw_dir, drop_q9=True)
        c = X.counts(sd, idx)
        run = X.longest_run(sd.hom_years())
        if len(run) < 10:
            changed.append(i.id)
            lines.append(f"| {i.id} | {i.trend.slope_per_decade:+.2f} | {'oui' if i.trend.significant else 'non'} | — | — | **série trop courte** |")
            continue
        t = X.annual_trend(run, [c[y] for y in run])
        flip = (t.significant != i.trend.significant) or (t.significant and (t.slope_per_decade > 0) != (i.trend.slope_per_decade > 0))
        if flip:
            changed.append(i.id)
        lines.append(f"| {i.id} | {i.trend.slope_per_decade:+.2f} | {'oui' if i.trend.significant else 'non'} | "
                     f"{t.slope_per_decade:+.2f} | {'oui' if t.significant else 'non'} | {'**oui**' if flip else 'non'} |")
    out.append(Check("E8 robustesse au code qualité 9", not changed,
                     f"{len(changed)} conclusion(s) modifiée(s) sur {len([i for i in stations if i.trend])}"))

    # E9 — indices rares : signalés, chiffre mis en avant = écart entre normales.
    rare = [i.id for i in inds if i.headline == "normals"]
    over = [i.id for i in inds if i.headline == "normals" and i.confidence == "elevee"]
    out.append(Check("E9 indices rares", not over, f"{len(rare)} indicateur(s) rare(s), aucun en confiance « élevée »"
                     if not over else f"confiance « élevée » interdite : {over}"))
    return out, lines


def build_report(cs: list[Check], verdict: str, indicators: list[str]) -> ValidationReport:
    counted = [c for c in cs if c.kind == "critère"]
    return ValidationReport(
        phase="p2a",
        generated_at=datetime.now(timezone.utc).replace(microsecond=0),
        closure_ok=all(c.satisfied for c in counted),
        verdict=verdict,
        indicators=indicators,
        checks=[ValidationCheck(name=c.name, kind=c.kind, status=c.status, satisfied=c.satisfied, detail=c.detail) for c in cs],
    )


def main(out_dir: Path = PROCESSED_DIR, raw_dir: Path = RAW_DIR) -> int:
    inds = load_indicators(out_dir)
    if not inds:
        print("Aucun indicateur P2a publié : validation P2a non exécutée.")
        return 0
    cs, tables = checks(inds, raw_dir)
    counted = [c for c in cs if c.kind == "critère"]
    pending = [c.name for c in counted if c.pending]
    if all(c.satisfied for c in counted):
        verdict = "Tous les critères comptant pour la clôture sont satisfaits."
    elif pending and all(c.satisfied or c.pending for c in counted):
        verdict = f"Critères satisfaits, sauf en attente : {', '.join(pending)}."
    else:
        verdict = "Au moins un critère comptant pour la clôture n'est pas satisfait."
    md = ["# Validation P2a — résultats automatiques", "",
          "Fichier généré par `python -m etl.validation.p2a` à chaque exécution de l'ETL. Ne pas éditer à la main. "
          "Critères et seuils : `docs/phases.md` (P2a).", "", f"**{verdict}**", "",
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
