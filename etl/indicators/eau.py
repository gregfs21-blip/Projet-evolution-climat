"""P2b — demande en eau et sécheresse (critères F1-F11, validés par Grég le 26/10/2026 avant tout calcul).

Données mensuelles LSH, toutes homogénéisées (aucune correction à faire) : TN, TX et RR de Bordeaux-Paulin,
Cap-Ferret et Cazaux.
- ETP de Hargreaves (FAO-56, éq. 52) : 0,0023 × 0,408 × Ra × (TM + 17,8) × √(TX − TN) mm/jour, Ra (MJ m⁻² j⁻¹)
  du 15 du mois à la latitude du poste (FAO-56, éq. 21-25), multiplié par le nombre de jours du mois ;
- bilan climatique annuel P − ETP ;
- SPEI (Vicente-Serrano et al., 2010) : P − ETP cumulé sur 3 et 12 mois, loi log-logistique à 3 paramètres dans la
  forme de Hosking (logistique généralisée, Beguería et al., 2014), ajustée par L-moments pour chaque mois calendaire sur la période de calage 1962-2017 ; indicateurs : SPEI-12 de décembre
  et nombre de mois de l'année où SPEI-3 ≤ −1.
Référence R6 (ETP) : ORACLE Nouvelle-Aquitaine 2020, p. 61, [+16 ; +30] mm/déc. sur 1962-2019.
"""

from __future__ import annotations

import calendar
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy import special, stats

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import serie as S
from etl.indicators import temperature as T
from etl.schema import Indicator, Provenance, Station
from etl.sources import meteofrance_lsh as lsh

POSTES = ("33063001", "33236002", "33529001")       # Bordeaux-Paulin, Cap-Ferret, Cazaux (TN, TX, RR homogénéisés)
CALIBRATION = (1962, 2017)
DRY_THRESHOLD = -1.0
R6 = {
    "kind": "slope", "period": [1962, 2019], "range": [16.0, 30.0], "unit": "mm/déc.", "fixed_on": "2026-10-26",
    "statement": ("ORACLE Nouvelle-Aquitaine 2020 (p. 61) : ETP annuelle + 24 mm par décennie en Gironde, + 95 à + 183 mm "
                  "en 60 ans selon les départements (chaîne SIM de Météo-France, Penman-Monteith, 1959-2019) ; "
                  "fourchette des départements"),
    "source": "Chambres d'agriculture de Nouvelle-Aquitaine, ORACLE 2020",
    "url": "https://creuse.chambre-agriculture.fr/fileadmin/user_upload/National/FAL_commun/publications/Nouvelle-Aquitaine/2020_ORACLE_Nouvelle_Aquitaine.pdf",
}


# ---------------------------------------------------------------- calculs (purs, testés)


def ra(lat_deg: float, year: int, month: int) -> float:
    """Rayonnement extraterrestre (MJ m⁻² j⁻¹) le 15 du mois, FAO-56 éq. 21-25."""
    return ra_doy(lat_deg, (np_date(year, month, 15) - np_date(year, 1, 1)) + 1)


def ra_doy(lat_deg: float, j: int) -> float:
    phi = math.radians(lat_deg)
    dr = 1 + 0.033 * math.cos(2 * math.pi * j / 365)
    delta = 0.409 * math.sin(2 * math.pi * j / 365 - 1.39)
    ws = math.acos(max(-1.0, min(1.0, -math.tan(phi) * math.tan(delta))))
    return 24 * 60 / math.pi * 0.0820 * dr * (ws * math.sin(phi) * math.sin(delta) + math.cos(phi) * math.cos(delta) * math.sin(ws))


def np_date(y: int, m: int, d: int) -> int:
    from datetime import date
    return date(y, m, d).toordinal()


def etp_month(tn: float, tx: float, lat: float, year: int, month: int) -> float:
    tm = (tn + tx) / 2
    daily = 0.0023 * 0.408 * ra(lat, year, month) * (tm + 17.8) * math.sqrt(max(tx - tn, 0.0))
    return daily * calendar.monthrange(year, month)[1]


def loglogistic_params(x: np.ndarray) -> tuple[float, float, float]:
    """Loi logistique généralisée (forme de Hosking de la log-logistique à 3 paramètres, recommandée par Beguería et
    al., 2014, pour le SPEI) ajustée par L-moments non biaisés : (ξ, α, κ)."""
    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)
    i = np.arange(n)
    b0 = x.mean()
    b1 = np.sum(i / (n - 1) * x) / n
    b2 = np.sum(i * (i - 1) / ((n - 1) * (n - 2)) * x) / n
    l1, l2, l3 = b0, 2 * b1 - b0, 6 * b2 - 6 * b1 + b0
    k = -l3 / l2
    if abs(k) < 1e-6:
        return float(l1), float(l2), 0.0
    a = l2 * math.sin(k * math.pi) / (k * math.pi)
    xi = l1 - a * (1 / k - math.pi / math.sin(k * math.pi))
    return float(xi), float(a), float(k)


def spei_value(x: float, params: tuple[float, float, float]) -> float:
    xi, a, k = params
    if k == 0:
        y = (x - xi) / a
    else:
        arg = 1 - k * (x - xi) / a
        if arg <= 0:                     # hors du support : queue extrême
            return 4.0 if k > 0 else -4.0
        y = -math.log(arg) / k
    p = 1 / (1 + math.exp(-y))
    return float(stats.norm.ppf(min(max(p, 1e-6), 1 - 1e-6)))


def accumulate(d: dict[tuple[int, int], float], k: int) -> dict[tuple[int, int], float]:
    """Somme glissante sur k mois consécutifs ; un mois manquant interrompt la somme (aucune valeur complétée)."""
    out = {}
    for (y, m) in d:
        keys = []
        yy, mm = y, m
        for _ in range(k):
            keys.append((yy, mm))
            yy, mm = (yy, mm - 1) if mm > 1 else (yy - 1, 12)
        if all(kk in d for kk in keys):
            out[(y, m)] = sum(d[kk] for kk in keys)
    return out


def spei(d: dict[tuple[int, int], float], k: int, calib: tuple[int, int] = CALIBRATION) -> dict[tuple[int, int], float]:
    acc = accumulate(d, k)
    out = {}
    for month in range(1, 13):
        ref = [v for (y, m), v in acc.items() if m == month and calib[0] <= y <= calib[1]]
        if len(ref) < 30:
            raise ValueError(f"SPEI-{k} : seulement {len(ref)} années de calage pour le mois {month}")
        params = loglogistic_params(np.array(ref))
        for (y, m), v in acc.items():
            if m == month:
                out[(y, m)] = spei_value(v, params)
    return out


# ---------------------------------------------------------------- données


@lru_cache(maxsize=4)
def _series(var: str, raw_dir: str) -> dict[str, lsh.LshSeries]:
    return {s.station.id: s for s in lsh.load_department(var, "33", Path(raw_dir), download=not T._offline())}


@lru_cache(maxsize=8)
def station_water(poste: str, raw_dir: str):
    """Mensuel : ETP, P, D = P − ETP, statuts homogénéisés, et la station (nommée)."""
    tn, tx, rr = (_series(v, raw_dir)[poste] for v in ("TN", "TX", "RR"))
    lat = tn.station.latitude
    etp, etp_hom, p, d, d_hom = {}, {}, {}, {}, {}
    for k in tn.values.keys() & tx.values.keys():
        etp[k] = etp_month(tn.values[k], tx.values[k], lat, *k)
        etp_hom[k] = tn.homogenized[k] and tx.homogenized[k]
        if k in rr.values:
            p[k] = rr.values[k]
            d[k] = rr.values[k] - etp[k]
            d_hom[k] = etp_hom[k] and rr.homogenized[k]
    cfg = T.station_config().get(poste, {})
    st = tn.station.model_copy(update={"name": cfg.get("name", tn.station.name)})
    return etp, etp_hom, p, d, d_hom, st


def _annual(values: dict, hom: dict, agg=sum) -> tuple[dict[int, float], set[int]]:
    out, h = {}, set()
    for y in sorted({y for y, _ in values}):
        ks = [(y, m) for m in range(1, 13)]
        if all(k in values for k in ks):
            out[y] = round(float(agg([values[k] for k in ks])), 3)
            if all(hom.get(k) for k in ks):
                h.add(y)
    return out, h


def spei_tables(poste: str, raw_dir: str):
    _etp, _eh, _p, d, d_hom, _st = station_water(poste, raw_dir)
    # Le calage et les indices n'utilisent que les mois homogénéisés (P et ETP) : aucun mois brut n'entre.
    dh = {k: v for k, v in d.items() if d_hom.get(k)}
    return spei(dh, 3), spei(dh, 12)


# ---------------------------------------------------------------- indicateurs


def _prov(ctx: BuildContext) -> Provenance:
    return Provenance(source_name=lsh.SOURCE_NAME, source_url=lsh.DATASET_URL, license=lsh.LICENSE,
                      extracted_at=ctx.extracted_at, script="etl.indicators.eau", etl_version=ctx.etl_version,
                      homogenized=True)


LIMITS = [
    "ETP de Hargreaves : calculée à partir des seules températures minimale et maximale ; elle ignore le vent, "
    "l'humidité et le rayonnement mesuré, que prend en compte la formule de Penman-Monteith utilisée par Météo-France.",
    "Séries mensuelles homogénéisées par Météo-France (LSH) ; pluie homogénéisée jusqu'en 2017 seulement : au-delà, "
    "le bilan et le SPEI ne sont pas calculés.",
]

SPEC = {
    "etp": ("mm", "l'évapotranspiration potentielle annuelle", "Évapotranspiration potentielle (Hargreaves) à {name}",
            "Somme annuelle de l'évapotranspiration potentielle mensuelle de Hargreaves, à partir des températures "
            "minimales et maximales homogénéisées de {name}."),
    "bilan-hydrique": ("mm", "le bilan climatique pluie − ETP", "Bilan climatique pluie − ETP à {name}",
                       "Différence annuelle entre la pluie homogénéisée et l'ETP de Hargreaves à {name}. Négatif : "
                       "l'air « réclame » plus d'eau qu'il n'en tombe."),
    "spei12": ("SPEI", "le SPEI à 12 mois de décembre", "Indice de sécheresse SPEI-12 (bilan de l'année) à {name}",
               "SPEI-12 de décembre : bilan pluie − ETP des 12 mois de l'année, exprimé en écarts-types par rapport à "
               "1962-2017 (0 = année normale, −1 = sèche, −2 = très sèche)."),
    "mois-secs": ("mois", "le nombre de mois secs", "Mois secs (SPEI-3 ≤ −1) à {name}",
                  "Nombre de mois de l'année où le bilan pluie − ETP des 3 derniers mois est au moins un écart-type "
                  "sous la normale 1962-2017 (SPEI-3 ≤ −1)."),
}
PLAUSIBLE = {"etp": (500.0, 1400.0), "bilan-hydrique": (-1000.0, 1200.0), "spei12": (-4.0, 4.0), "mois-secs": (0.0, 12.0)}


def build(ctx: BuildContext, variable: str, poste: str, limitations: list[str] | None = None) -> Indicator:
    raw = str(ctx.raw_dir)
    etp, etp_hom, _p, d, d_hom, st = station_water(poste, raw)
    if variable == "etp":
        series, hom = _annual(etp, etp_hom)
    elif variable == "bilan-hydrique":
        series, hom = _annual(d, d_hom)
    else:
        s3, s12 = spei_tables(poste, raw)
        if variable == "spei12":
            series = {y: round(v, 3) for (y, m), v in s12.items() if m == 12}
        else:
            years = sorted({y for y, _ in s3})
            series = {y: float(sum(1 for m in range(1, 13) if s3[(y, m)] <= DRY_THRESHOLD))
                      for y in years if all((y, m) in s3 for m in range(1, 13))}
        hom = set(series)        # SPEI calculé sur les seuls mois homogénéisés
    lo, hi = PLAUSIBLE[variable]
    bad = {y: v for y, v in series.items() if not lo <= v <= hi}
    if bad:
        raise ValueError(f"{variable} {poste} : valeurs hors de [{lo} ; {hi}] : {list(bad.items())[:3]}")
    unit, label, title, desc = SPEC[variable]
    name = st.name
    slug = T.station_config().get(poste, {}).get("slug") or S.slugify(name)
    note = ("ETP de Hargreaves (FAO-56, éq. 52) au pas mensuel, rayonnement extraterrestre du 15 du mois à la latitude "
            "du poste." + (" SPEI : loi log-logistique (forme logistique généralisée) ajustée par L-moments sur "
                           "1962-2017, mois par mois (Vicente-Serrano et al., 2010 ; Beguería et al., 2014)." if variable in ("spei12", "mois-secs") else ""))
    return S.assemble(ctx, ind_id=f"{variable}-{slug}", scale="gironde", variable=variable,
                      place=vocab.station(slug, name), title=title.format(name=name), description=desc.format(name=name),
                      unit=unit, series=series, hom=hom, provenance=_prov(ctx), limitations=LIMITS + (limitations or []),
                      stations=[st], method_note=note, reference=R6 if variable == "etp" else None, baseline=None,
                      group="Stations — demande en eau et sécheresse", where=f"À {name}", label=label)
