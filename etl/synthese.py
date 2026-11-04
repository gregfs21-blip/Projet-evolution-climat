"""P8 — synthèse par échelle (cadrage et critères M1-M7 validés par Grég le 02/11/2026, avant toute rédaction).

Lit les indicateurs publiés (data/processed) et le fichier d'affirmations etl/config/synthese.yaml, puis écrit
data/processed/synthese.json. Rien n'est recalculé sur les sources : seules les séries publiées sont relues.

- Les chiffres du texte viennent de champs à trous : {indicateur|champ|format}, {acc:id|champ|format},
  {cmp:id|champ|format} (critère M1 : aucun nombre littéral hors années et seuils déclarés dans `literals`).
- Confiance d'une affirmation = la plus faible des indicateurs cités (S1).
- Signal : chaque indicateur cité est significatif et au moins en confiance « moyenne » ; absence : aucun indicateur
  cité n'est significatif, ou il est en « signal non établi » (S2, M2).
- Comparaison : pentes de Sen recalculées sur une période commune ; « plus rapide » seulement si les intervalles à
  95 % sont disjoints (S3, M4). Les mots de comparaison sont interdits ailleurs.
- Accélération : etl/stats/acceleration.py (S5) ; le texte est choisi selon le résultat.
Une règle non respectée à la génération est écrite dans `problem` et affichée telle quelle par le site.

Usage : python -m etl.synthese
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from etl.context import PROCESSED_DIR, ROOT
from etl.schema import (Claim, ClaimGroup, ClaimIndicator, ClaimSource, Coverage, Synthesis, SynthesisSection)
from etl.stats.acceleration import quadratic_acceleration
from etl.stats.trend import annual_trend

CONFIG = ROOT / "etl" / "config" / "synthese.yaml"
OUT = PROCESSED_DIR / "synthese.json"
RANK = {"non_etabli": 0, "faible": 1, "moyenne": 2, "elevee": 3}
PLACEHOLDER = re.compile(r"\{([^{}|]+)\|([^{}|]+)(?:\|([^{}|]*))?\}")
NUMBER = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)?")
YEAR = re.compile(r"(18|19|20)\d\d")
COMPARE_WORDS = re.compile(r"plus (rapide|vite|lent|fort|faible)|moins (rapide|vite)|même ordre", re.IGNORECASE)
ALIASES = {
    "slope": "trend.slope_per_decade", "ci_low": "trend.slope_ci_low", "ci_high": "trend.slope_ci_high",
    "start": "trend.period.start", "end": "trend.period.end", "p": "trend.p_value",
    "nc_first": "normals_comparison.first_value", "nc_second": "normals_comparison.second_value",
    "nc_diff": "normals_comparison.difference", "nc_p": "normals_comparison.p_value",
}


# ---------------------------------------------------------------- formatage (français)


def fmt(value, spec: str | None) -> str:
    if isinstance(value, str) or not spec:
        return str(value)
    if spec == "p":
        return "< 0,001" if value < 0.001 else "= " + fmt(value, ".2" if value >= 0.01 else ".3")
    sign = spec.startswith("+")
    spec = spec.lstrip("+")
    if spec == "d":
        s = f"{round(value):d}"
    else:
        s = f"{value:.{int(spec.lstrip('.'))}f}"
    neg = s.startswith("-")
    s = s.lstrip("-")
    if neg and float(s.replace(",", ".")) == 0:
        neg = False
    ent, _, dec = s.partition(".")
    if len(ent) > 4:
        ent = f"{int(ent):,}".replace(",", " ")
    s = ent + ("," + dec if dec else "")
    return ("−" if neg else "+" if sign else "") + s


# ---------------------------------------------------------------- lecture des indicateurs


def load_indicators(out_dir: Path = PROCESSED_DIR) -> dict[str, dict]:
    inds = {}
    for scale in ("gironde", "france", "monde"):
        for p in sorted((out_dir / scale).glob("*.json")):
            inds[p.stem] = json.loads(p.read_text(encoding="utf-8"))
    return inds


def series(ind: dict, start: int | None = None, end: int | None = None) -> tuple[list[int], list[float]]:
    pts = [(int(t[:4]), v) for t, v in zip(ind["series"]["time"], ind["series"]["value"]) if v is not None]
    pts = [(t, v) for t, v in pts if (start is None or t >= start) and (end is None or t <= end)]
    return [t for t, _ in pts], [v for _, v in pts]


def significant(ind: dict) -> bool:
    if ind.get("headline") == "normals" and ind.get("normals_comparison"):
        return bool(ind["normals_comparison"]["significant"])
    return bool((ind.get("trend") or {}).get("significant"))


def field(ind: dict, name: str):
    if name == "total":
        t = ind["trend"]
        return t["fitted_end"] - t["fitted_start"]
    if name.startswith("mean:"):
        a, b = (int(x) for x in name[5:].split("-"))
        yrs, vals = series(ind, a, b)
        if len(yrs) != b - a + 1:
            raise ValueError(f"{ind['id']} : moyenne {a}-{b} incomplète ({len(yrs)} années)")
        return sum(vals) / len(vals)
    if name in ("last", "last_time"):
        yrs, vals = series(ind)
        return vals[-1] if name == "last" else str(yrs[-1])
    cur = ind
    for part in ALIASES.get(name, name).split("."):
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


# ---------------------------------------------------------------- calculs dérivés (S3, S5)


@dataclass
class Comparison:
    id: str
    a: str
    b: str
    start: int
    end: int
    a_trend: object
    b_trend: object

    @property
    def verdict(self) -> str:
        if self.a_trend.slope_ci_low > self.b_trend.slope_ci_high:
            return "plus rapide que"
        if self.a_trend.slope_ci_high < self.b_trend.slope_ci_low:
            return "plus lent que"
        return "du même ordre que"

    def get(self, name: str):
        if name == "verdict":
            return self.verdict
        if name in ("start", "end"):
            return str(getattr(self, name))
        who, _, what = name.partition("_")
        t = self.a_trend if who == "a" else self.b_trend
        return {"slope": t.slope_per_decade, "low": t.slope_ci_low, "high": t.slope_ci_high}[what]


def compute_comparisons(cfg: list[dict], inds: dict[str, dict]) -> dict[str, Comparison]:
    out = {}
    for c in cfg:
        ta = annual_trend(*series(inds[c["a"]], c["start"], c["end"]))
        tb = annual_trend(*series(inds[c["b"]], c["start"], c["end"]))
        for t, who in ((ta, c["a"]), (tb, c["b"])):
            if (t.period.start, t.period.end) != (c["start"], c["end"]):
                raise ValueError(f"comparaison {c['id']} : {who} ne couvre pas {c['start']}-{c['end']}")
        out[c["id"]] = Comparison(c["id"], c["a"], c["b"], c["start"], c["end"], ta, tb)
    return out


def compute_accelerations(cfg: list[dict], inds: dict[str, dict]) -> dict[str, object]:
    out = {}
    for a in cfg:
        r = quadratic_acceleration(*series(inds[a["indicator"]], a["start"], a["end"]))
        if (r.start, r.end) != (a["start"], a["end"]):
            raise ValueError(f"accélération {a['id']} : la série couvre {r.start}-{r.end}, attendu {a['start']}-{a['end']}")
        out[a["id"]] = (a["indicator"], r)
    return out


def acc_field(r, name: str):
    if name in ("start", "end"):
        return str(getattr(r, name))
    return {"value": r.value, "ci_low": r.ci_low, "ci_high": r.ci_high, "p": r.p_value,
            "rate_start": r.rate_start, "rate_end": r.rate_end,
            "rate_start10": r.rate_start * 10, "rate_end10": r.rate_end * 10}[name]


# ---------------------------------------------------------------- rendu et contrôles


def literal_numbers(template: str, literals: list) -> list[str]:
    """Critère M1 : nombres écrits en dur dans le gabarit, hors années et seuils déclarés."""
    bare = PLACEHOLDER.sub(" ", template)
    allowed = {str(x) for x in literals}
    return [n for n in NUMBER.findall(bare) if not YEAR.fullmatch(n) and n not in allowed]


class Renderer:
    def __init__(self, inds, accs, cmps):
        self.inds, self.accs, self.cmps = inds, accs, cmps

    def refs(self, template: str) -> list[str]:
        out = []
        for key, _, _ in PLACEHOLDER.findall(template):
            if key.startswith("acc:"):
                out.append(self.accs[key[4:]][0])
            elif key.startswith("cmp:"):
                c = self.cmps[key[4:]]
                out += [c.a, c.b]
            else:
                out.append(key)
        return out

    def render(self, template: str) -> str:
        def sub(m):
            key, name, spec = m.group(1), m.group(2), m.group(3)
            if key.startswith("acc:"):
                return fmt(acc_field(self.accs[key[4:]][1], name), spec)
            if key.startswith("cmp:"):
                return fmt(self.cmps[key[4:]].get(name), spec)
            if key not in self.inds:
                raise KeyError(f"indicateur inconnu : {key}")
            return fmt(field(self.inds[key], name), spec)
        return PLACEHOLDER.sub(sub, template).strip()


def claim_from(item: dict, r: Renderer, scale: str | None) -> tuple[Claim, list[str]]:
    """Construit une affirmation ; renvoie aussi les violations M1 (gabarits) pour le rapport de validation."""
    kind = item["kind"]
    literals = item.get("literals", [])
    templates = [item["text"]] if "text" in item else list(item["text_if"].values())
    m1 = [f"{item['id']} : nombre écrit en dur « {n} »" for t in templates for n in literal_numbers(t, literals)]
    problems = []
    if kind not in ("comparaison", "contexte") and any(COMPARE_WORDS.search(PLACEHOLDER.sub(" ", t)) for t in templates):
        problems.append("mot de comparaison hors d'une comparaison sur période commune (S3)")

    accs = item.get("acc", [])
    if "text_if" in item:
        ok = all(r.accs[a][1].significant for a in accs)
        template = item["text_if"]["significant" if ok else "not_significant"]
    else:
        template = item["text"]
    ids = list(dict.fromkeys(item.get("indicators", []) + [r.accs[a][0] for a in accs] + r.refs(template)))
    missing = [i for i in ids if i not in r.inds]
    if missing:
        raise KeyError(f"{item['id']} : indicateurs absents {missing}")
    inds = [r.inds[i] for i in ids]

    confidence = None
    if kind in ("signal", "absence", "comparaison", "acceleration"):
        confidence = min((d["confidence"] for d in inds), key=RANK.get)
        if kind == "signal":
            bad = [d["id"] for d in inds if not significant(d) or RANK[d["confidence"]] < RANK["moyenne"]]
            if bad:
                problems.append(f"signal sur un indicateur non significatif ou de confiance insuffisante : {', '.join(bad)} (M2)")
        elif kind == "absence":
            confidence = "non_etabli"
            bad = [d["id"] for d in inds if significant(d) and d["confidence"] != "non_etabli"]
            if bad:
                problems.append(f"absence de signal affirmée sur un indicateur significatif : {', '.join(bad)} (M2)")
        elif kind == "acceleration" and not all(r.accs[a][1].significant for a in accs):
            confidence = "non_etabli"

    src = item.get("source")
    claim = Claim(id=item["id"], kind=kind, params=item.get("params", []), text=r.render(template),
                  confidence=confidence,
                  indicators=[ClaimIndicator(id=d["id"], scale=d["scale"], title=d["title"], confidence=d["confidence"])
                              for d in inds] if kind not in ("contexte", "lacune") else [],
                  source=ClaimSource(**src) if src else None, problem="; ".join(problems) or None)
    return claim, m1


@dataclass
class Result:
    synthesis: Synthesis
    m1: list[str]
    m3_missing: list[str]
    accelerations: dict
    comparisons: dict


def coverage_gaps(cov: Coverage) -> list[tuple[str, str, str, str | None]]:
    labels = {"gironde": "Gironde", "france": "France", "monde": "Monde"}
    out = []
    for p in cov.parameters:
        for c in p.cells:
            if c.status != "publie":
                status = {"prevu": "prévu", "sans-donnee": "sans donnée ouverte", "instantane": "valeur instantanée, pas de série"}[c.status]
                out.append((p.id, f"{p.label} — {labels[c.scale]} : {status}.", c.scale, c.note))
    return out


def build(out_dir: Path = PROCESSED_DIR, config: Path = CONFIG) -> Result:
    cfg = yaml.safe_load(config.read_text(encoding="utf-8"))
    inds = load_indicators(out_dir)
    accs = compute_accelerations(cfg.get("accelerations", []), inds)
    cmps = compute_comparisons(cfg.get("comparisons", []), inds)
    r = Renderer(inds, accs, cmps)
    cov = Coverage.model_validate_json((out_dir / "couverture.json").read_text(encoding="utf-8"))
    m1: list[str] = []
    sections = []
    for sec in cfg["sections"]:
        for part in ("intro", "conclusion"):
            if sec.get(part):
                m1 += [f"{sec['id']} ({part}) : nombre écrit en dur « {n} »"
                       for n in literal_numbers(sec[part], sec.get("literals", []))]
        groups, pending = [], None
        for g in sec.get("groups", []):
            claims = []
            for item in g["claims"]:
                needed = item.get("indicators", []) + [k for k, _, _ in PLACEHOLDER.findall(item.get("text", ""))
                                                         if ":" not in k]
                if sec.get("optional") and any(i not in inds for i in needed):
                    pending = sec.get("pending")
                    continue
                c, v = claim_from(item, r, sec.get("scale"))
                claims.append(c)
                m1 += v
            if claims:
                groups.append(ClaimGroup(title=g["title"], claims=claims))
        if sec.get("gaps_from_coverage"):
            claims = [Claim(id=f"lacune-{pid}-{scale}", kind="lacune", params=[pid], text=text + (f" {note}" if note else ""),
                            confidence=None) for pid, text, scale, note in coverage_gaps(cov)]
            if claims:
                groups.insert(0, ClaimGroup(title="Cases de la couverture sans série publiée", claims=claims))
        if sec.get("optional") and not groups:
            pending = sec.get("pending")
        sections.append(SynthesisSection(id=sec["id"], title=sec["title"], scale=sec.get("scale"),
                                         intro=r.render(sec["intro"]) if sec.get("intro") else None, groups=groups,
                                         conclusion=r.render(sec["conclusion"]) if sec.get("conclusion") else None,
                                         pending=pending))
    covered = {(s.scale, p) for s in sections if s.scale for g in s.groups for c in g.claims
               if c.kind != "lacune" for p in c.params}
    m3 = [f"{p.id} / {c.scale}" for p in cov.parameters for c in p.cells
          if c.status == "publie" and (c.scale, p.id) not in covered]
    syn = Synthesis(generated_at=datetime.now(timezone.utc).replace(microsecond=0), sections=sections)
    return Result(syn, m1, m3, accs, cmps)


def main() -> int:
    res = build()
    OUT.write_text(res.synthesis.model_dump_json(indent=1, exclude_none=True) + "\n", encoding="utf-8")
    n = sum(len(g.claims) for s in res.synthesis.sections for g in s.groups)
    probs = [c for s in res.synthesis.sections for g in s.groups for c in g.claims if c.problem]
    print(f"→ {OUT.relative_to(ROOT)} : {n} affirmations, {len(probs)} à revoir, M1 {len(res.m1)} écart(s), "
          f"M3 {len(res.m3_missing)} case(s) non traitée(s)")
    for c in probs:
        print(f"  ⚠ {c.id} : {c.problem}")
    for x in res.m1 + res.m3_missing:
        print(f"  ⚠ {x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
