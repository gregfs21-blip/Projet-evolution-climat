"""Indicateurs ERA5 sur niveaux de pression (Copernicus CDS) : altitude au-dessus de Bordeaux et jet stream.

Choix fixés le 26/10/2026, AVANT tout calcul (aucune série ERA5 niveaux de pression n'avait encore été relevée) :
- température à 850 et 500 hPa et altitude de la surface 500 hPa, maille ERA5 la plus proche de Bordeaux-Mérignac :
  moyenne annuelle des 12 moyennes mensuelles ; une année exige ses 12 mois ;
- jet stream de l'Atlantique Nord en hiver (décembre de l'année précédente, janvier, février) : vent zonal à
  850 hPa moyenné sur 60° O-0°, entre 15 et 75° N, grille 1° (indice de Woollings et al., 2010, adapté aux moyennes
  mensuelles) ; VITESSE = maximum du profil moyen de l'hiver, LATITUDE = position de ce maximum, affinée par une
  parabole sur les trois latitudes qui l'encadrent.
  Décision de Grég du 26/10/2026 : la première définition, à 250 hPa, basculait entre jet subtropical et jet des
  tempêtes (constat sur la distribution seule, avant tout calcul de tendance) ;
- ERA5 traitée comme un produit publié (comme les autres séries ERA5 du projet) : tendance calculée, provenance
  « non homogénéisée », sans référence publiée → confiance au plus « moyenne ». Séries de plus de 80 ans : tendance
  mise en avant sur les 50 dernières années (règle du 23/10/2026).
"""

from __future__ import annotations

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import serie as S
from etl.schema import Indicator, Provenance, Station
from etl.sources import cds_era5 as cds

# variable → (niveau hPa, grandeur du CSV, unité, bornes plausibles de la valeur annuelle)
POINT_VARS = {
    "t850": (850, "t_c", "°C", (-5.0, 15.0)),
    "t500": (500, "t_c", "°C", (-35.0, -5.0)),
    "z500": (500, "z_m", "m", (5400.0, 5900.0)),
}
JET_VARS = {"jet-vitesse": ("m/s", (3.0, 30.0)), "jet-latitude": ("°N", (25.0, 72.0))}

LIMITS = [
    "Réanalyse ERA5 : un modèle météorologique contraint par les observations disponibles (radiosondages, avions, "
    "satellites depuis 1979), pas une mesure ; les changements du système d'observation peuvent créer de fausses "
    "tendances, surtout avant 1979. Aucune homogénéisation n'est appliquée.",
]


def _check(variable: str, series: dict[int, float], bounds: tuple[float, float]) -> None:
    lo, hi = bounds
    bad = {y: v for y, v in series.items() if not lo <= v <= hi}
    if bad:
        raise ValueError(f"{variable} : {len(bad)} valeur(s) annuelle(s) hors de [{lo} ; {hi}] (ex. {list(bad.items())[:3]})")
    if len(series) < 30:
        raise ValueError(f"{variable} : seulement {len(series)} années complètes")


def _provenance(ctx: BuildContext) -> Provenance:
    return Provenance(source_name=cds.SOURCE_NAME, source_url=cds.PAGE, license=cds.LICENSE,
                      extracted_at=ctx.extracted_at, script="etl.indicators.altitude", etl_version=ctx.etl_version,
                      homogenized=False)


def annual(monthly: dict[str, float]) -> dict[int, float]:
    """Moyenne des 12 mois ; une année incomplète n'est pas calculée."""
    years = sorted({int(m[:4]) for m in monthly})
    out = {}
    for y in years:
        vals = [monthly.get(f"{y}-{mo:02d}") for mo in range(1, 13)]
        if all(v is not None for v in vals):
            out[y] = round(sum(vals) / 12, 3)
    return out


def jet_indices(zonal: dict[str, dict[float, float]]) -> dict[int, tuple[float, float]]:
    """Année (de janvier) → (vitesse m/s, latitude °N) du profil moyen de l'hiver décembre-janvier-février."""
    out = {}
    years = sorted({int(m[:4]) for m in zonal})
    for y in years:
        months = [f"{y - 1}-12", f"{y}-01", f"{y}-02"]
        if not all(m in zonal for m in months):
            continue
        lats = sorted(zonal[months[0]])
        prof = [sum(zonal[m][lat] for m in months) / 3 for lat in lats]
        k = max(range(len(prof)), key=prof.__getitem__)
        lat = lats[k]
        if 0 < k < len(prof) - 1:
            a, b, c = prof[k - 1], prof[k], prof[k + 1]
            den = a - 2 * b + c
            if den != 0:
                lat = lats[k] + 0.5 * (a - c) / den * (lats[k + 1] - lats[k])
        out[y] = (round(prof[k], 3), round(lat, 3))
    return out


def build_point(ctx: BuildContext, variable: str, title: str, description: str, label: str,
                limitations: list[str] | None = None) -> Indicator:
    level, qty, unit, bounds = POINT_VARS[variable]
    series = annual(cds.load_point()[level][qty])
    _check(variable, series, bounds)
    lat, lon = cds.BORDEAUX
    st = Station(id="era5-pl-bordeaux", name=f"Bordeaux (maille ERA5 {lat:.2f} N ; {-lon:.2f} O)".replace(".", ","),
                 latitude=lat, longitude=lon, altitude=0.0)
    v = vocab.variable(variable)
    return S.assemble(ctx, ind_id=f"{variable}-bordeaux-era5", scale="gironde", variable=variable,
                      place=vocab.station("bordeaux-era5", "Bordeaux (ERA5)"), title=title, description=description,
                      unit=unit, series=series, hom=set(series), provenance=_provenance(ctx),
                      limitations=LIMITS + (limitations or []), stations=[st], method_note=None, reference=None,
                      baseline=None, group=f"Réanalyse ERA5 — {v.theme_label}", where="Au-dessus de Bordeaux (ERA5)",
                      label=label)


def build_jet(ctx: BuildContext, variable: str, title: str, description: str, label: str,
              limitations: list[str] | None = None) -> Indicator:
    unit, bounds = JET_VARS[variable]
    idx = jet_indices(cds.load_zonal())
    series = {y: (s if variable == "jet-vitesse" else lat) for y, (s, lat) in idx.items()}
    _check(variable, series, bounds)
    note = ("Vent zonal à 850 hPa (environ 1 500 m) moyenné sur 60° O-0°, entre 15 et 75° N (grille 1°), puis sur l'hiver "
            "(décembre de l'année précédente, janvier, février) ; vitesse = maximum du profil en latitude, latitude = "
            "position de ce maximum affinée par une parabole sur trois points. L'année est celle de janvier. Indice de "
            "Woollings et al. (2010), calculé ici sur des moyennes mensuelles et non sur des valeurs quotidiennes filtrées.")
    return S.assemble(ctx, ind_id=f"{variable}-monde", scale="monde", variable=variable,
                      place=vocab.composite("monde", "Atlantique Nord"), title=title, description=description,
                      unit=unit, series=series, hom=set(series), provenance=_provenance(ctx),
                      limitations=LIMITS + (limitations or []), stations=[], method_note=note, reference=None,
                      baseline=None, group=vocab.variable(variable).theme_label, where="Sur l'Atlantique Nord, en hiver",
                      label=label)
