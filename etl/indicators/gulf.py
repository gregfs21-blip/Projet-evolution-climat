"""P9 — Gulf Stream et circulation de retournement atlantique (AMOC) : critères N1-N7 validés par Grég le 17/11/2026,
avant tout calcul (docs/phases.md).

- RAPID 26,5° N : débit de l'AMOC, profondeur du maximum de la fonction de courant, transport de chaleur. Séries
  depuis 2004 : confiance plafonnée à « signal non établi » (décision D-Z ; transport de chaleur ajouté le 17/11/2026
  à la demande de Grég, même règle).
- EN4.2.2 : température et salinité moyennes 0-700 m sur les zones de Caesar et al. (2018) (Gulf Stream, gyre
  subpolaire). Tendance à partir de l'année N7 (poids des observations ≥ 0,5 ensuite) ; les années précédentes sont
  publiées mais hors tendance et hors normales. Pas de référence chiffrée : confiance au plus « moyenne » (D-Z).
- Câble du détroit de Floride : « sans donnée » (D-AA), déclaré dans etl/config/couverture.yaml.
"""

from __future__ import annotations

from etl import vocabulary as vocab
from etl.context import BuildContext
from etl.indicators import serie as S
from etl.schema import Indicator, Provenance, Station
from etl.sources import en4 as E
from etl.sources import rapid as R

GROUP = "Exploratoire — Gulf Stream et AMOC"
CAP = ("Série directe de 20 ans environ, trop courte pour séparer une évolution climatique de la variabilité "
       "naturelle : confiance plafonnée à « signal non établi » (décision de Grég du 17/11/2026, P9).")
RAPID_LIMITS = [
    "Mesures du réseau RAPID depuis avril 2004 seulement (année 2004 incomplète, écartée) ; chaque nouvelle version de "
    "RAPID peut modifier légèrement toute la série.",
    "La littérature ne tranche pas : baisse de 18,3 à 15,9 Sv entre 2004 et 2018 (Bryden, 2021), réduite d'environ 40 % "
    "une fois le débit du détroit de Floride corrigé du champ géomagnétique (Volkov et al., 2024). Le GIEC (AR6) "
    "n'accorde qu'une confiance « faible » à un affaiblissement de l'AMOC au XXe siècle.",
    "Depuis novembre 2023, le câble du détroit de Floride est en panne : le débit de ce tronçon vient d'une autre méthode "
    "(capteurs de pression et altimétrie). Contrôle N5 dans le rapport de validation.",
]

RAPID = {
    "debit": dict(variable="amoc-debit", unit="Sv", bounds=(5.0, 30.0),
                  title="Débit de la circulation de retournement atlantique (AMOC) à 26,5° N",
                  description="Volume d'eau transporté vers le nord dans les 1 000 premiers mètres de l'Atlantique, au "
                              "niveau des Bahamas et des Canaries, et qui revient vers le sud en profondeur. Le Gulf "
                              "Stream en est la branche ouest. 1 Sv = 1 million de m³ par seconde.",
                  label="le débit de l'AMOC",
                  method="Maximum mensuel de la fonction de courant publié par RAPID, puis moyenne de l'année."),
    "profondeur": dict(variable="amoc-profondeur", unit="m", bounds=(300.0, 2500.0),
                       title="Profondeur du maximum de la circulation de retournement atlantique à 26,5° N",
                       description="Profondeur à laquelle le courant vers le nord laisse place au retour vers le sud : la "
                                   "fonction de courant y est maximale. Une remontée de cette limite signalerait une "
                                   "branche chaude moins épaisse.",
                       label="la profondeur du maximum de l'AMOC",
                       method="Chaque mois, profondeur du maximum de la fonction de courant RAPID (307 niveaux de 0 à "
                              "5 995 m, pas d'environ 20 m), puis moyenne de l'année."),
    "chaleur": dict(variable="amoc-chaleur", unit="PW", bounds=(0.2, 2.5),
                    title="Transport de chaleur vers le nord dans l'Atlantique à 26,5° N",
                    description="Chaleur transportée vers le nord par l'océan à travers tout l'Atlantique, en "
                                "pétawatts (1 PW = 10¹⁵ W). C'est par ce transport que l'AMOC réchauffe l'Atlantique "
                                "Nord et l'Europe.",
                    label="le transport de chaleur vers le nord",
                    method="Transport mensuel publié par RAPID-MOCHA, puis moyenne de l'année."),
}

ZONES = {
    "gulf-stream": ("Région du Gulf Stream (Caesar et al., 2018)", 41.5, -60.0,
                    "Dans la région du Gulf Stream (35,5-47,5° N, 74,5-45,5° O)"),
    "gyre-subpolaire": ("Gyre subpolaire (Caesar et al., 2018)", 54.0, -38.5,
                        "Dans le gyre subpolaire, au sud du Groenland (42,5-65,5° N, 63,5-13,5° O)"),
}
EN4_Q = {
    "temperature": dict(variable="temperature-0700", unit="°C", bounds=(0.0, 25.0),
                        name="Température", label="la température moyenne de 0 à 700 m"),
    "salinite": dict(variable="salinite-0700", unit="psu", bounds=(33.0, 37.5),
                     name="Salinité", label="la salinité moyenne de 0 à 700 m"),
}


def _cap(ind: Indicator) -> Indicator:
    return ind.model_copy(update={"confidence": "non_etabli", "limitations": list(ind.limitations) + [CAP]})


def build_rapid(ctx: BuildContext, quantity: str) -> Indicator:
    q = RAPID[quantity]
    series, _counts = R.annual(R.load()[quantity])
    series = {y: round(v, 4 if quantity == "chaleur" else 3 if quantity == "debit" else 1) for y, v in series.items()}
    lo, hi = q["bounds"]
    bad = {y: v for y, v in series.items() if not lo <= v <= hi}
    if bad or len(series) < 15:
        raise ValueError(f"RAPID {quantity} : valeurs hors [{lo} ; {hi}] ou série courte : {list(bad.items())[:3]}, {len(series)} ans")
    prov = Provenance(source_name=R.source_name(), source_url=R.PAGE, license=R.LICENSE, extracted_at=ctx.extracted_at,
                      script="etl.indicators.gulf", etl_version=ctx.etl_version, homogenized=False)
    ind = S.assemble(ctx, ind_id=f"{q['variable']}-monde", scale="monde", variable=q["variable"],
                     place=vocab.composite("monde", "Atlantique, 26,5° N"), title=q["title"], description=q["description"],
                     unit=q["unit"], series=series, hom=set(series), provenance=prov, limitations=list(RAPID_LIMITS),
                     stations=[], method_note=q["method"], reference=None, baseline=None, group=GROUP,
                     where="Dans l'Atlantique à 26,5° N", label=q["label"])
    return _cap(ind)


def build_en4(ctx: BuildContext, zone: str, quantity: str) -> Indicator:
    q = EN4_Q[quantity]
    name, lat, lon, where = ZONES[zone]
    series, weights = E.load_zone(zone, quantity)
    lo, hi = q["bounds"]
    bad = {y: v for y, v in series.items() if not lo <= v <= hi}
    if bad or len(series) < 100:
        raise ValueError(f"EN4 {zone} {quantity} : valeurs hors [{lo} ; {hi}] ou série courte : {list(bad.items())[:3]}")
    start = E.n7_start(weights)
    if start is None:
        raise ValueError(f"EN4 {zone} {quantity} : aucune année ne satisfait N7")
    hom = {y for y in series if y >= start}
    series = {y: round(v, 4) for y, v in series.items()}
    prov = Provenance(source_name=E.SOURCE_NAME, source_url=E.PAGE, license=E.LICENSE, extracted_at=ctx.extracted_at,
                      script="etl.indicators.gulf", etl_version=ctx.etl_version, homogenized=False)
    lims = [
        f"Avant {start}, l'analyse EN4 est trop peu contrainte par les mesures dans cette zone (poids moyen des observations "
        f"sous {E.N7_WEIGHT:g} au moins une année ensuite, critère N7) : ces années sont affichées « brutes » et n'entrent "
        "ni dans la tendance ni dans les normales.",
        "Analyse objective : là où il n'y a pas de mesure, la valeur revient vers un champ de fond ; les variations "
        "d'une année à l'autre y sont atténuées.",
        "Zones définies par Caesar et al. (2018) pour leur indice de l'AMOC : le gyre subpolaire se refroidit et le Gulf "
        "Stream se réchauffe quand l'AMOC ralentit, mais d'autres causes (vents, aérosols, réchauffement général) jouent "
        "aussi ; une tendance ici ne prouve pas un ralentissement de l'AMOC.",
    ]
    if quantity == "salinite":
        lims.append("Salinité pratique, sans unité (notée psu) ; mesures sous la surface rares avant les flotteurs Argo "
                    "(années 2000).")
    st = Station(id=f"zone-{zone}", name=name, latitude=lat, longitude=lon, altitude=0.0)
    return S.assemble(ctx, ind_id=f"{q['variable']}-{zone}", scale="monde", variable=q["variable"],
                      place=vocab.station(zone, name), title=f"{q['name']} de l'océan entre 0 et 700 m — {name}",
                      description=f"{q['name']} moyenne des 700 premiers mètres de l'océan, moyenne annuelle, d'après "
                                  "l'analyse EN4 du Met Office (profils de navires, bouées et flotteurs Argo).",
                      unit=q["unit"], series=series, hom=hom, provenance=prov, limitations=lims, stations=[st],
                      method_note="Moyenne pondérée par le volume (surface des mailles × épaisseur des niveaux, coupée à "
                      "700 m) sur la zone, chaque mois, puis moyenne de l'année.", reference=None, baseline=None,
                      group=GROUP, where=where, label=q["label"])
