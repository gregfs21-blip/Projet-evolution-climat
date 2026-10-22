"""Contrat de données entre l'ETL et le site.

Ce schéma est la référence unique. Le site Next.js en possède le miroir exact
(web/lib/schema.ts, avec zod). Toute modification ici doit être reportée là-bas
et faire monter SCHEMA_VERSION.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SCHEMA_VERSION = "1.0"

Scale = Literal["gironde", "france", "monde"]
Frequency = Literal["annual", "seasonal", "monthly", "daily"]
Confidence = Literal["elevee", "moyenne", "faible", "non_etabli"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Period(_Strict):
    start: int = Field(ge=1700, le=2200)
    end: int = Field(ge=1700, le=2200)

    @model_validator(mode="after")
    def _ordered(self) -> "Period":
        if self.end < self.start:
            raise ValueError("period.end doit être >= period.start")
        return self


class Provenance(_Strict):
    source_name: str = Field(min_length=1)
    source_url: str = Field(pattern=r"^https?://")
    license: str = Field(min_length=1)
    extracted_at: datetime
    script: str = Field(min_length=1, description="Module ETL qui a produit le fichier")
    etl_version: str = Field(min_length=1)
    homogenized: bool = Field(description="Série homogénéisée (ex. LSH) ou brute")


class Trend(_Strict):
    method: str = Field(min_length=1, description="Ex. 'mann-kendall-hamed-rao + sen'")
    period: Period
    slope_per_decade: float = Field(description="Pente de Sen, en unité de l'indicateur par décennie")
    slope_ci_low: float | None = None
    slope_ci_high: float | None = None
    fitted_start: float = Field(description="Valeur de la droite de Sen en début de période (pour le tracé)")
    fitted_end: float = Field(description="Valeur de la droite de Sen en fin de période")
    p_value: float = Field(ge=0, le=1)
    significant: bool
    alpha: float = Field(default=0.05, gt=0, lt=1)


class Breakpoint(_Strict):
    time: str
    method: str
    p_value: float | None = Field(default=None, ge=0, le=1)


class Series(_Strict):
    """Série en colonnes : plus compacte qu'une liste d'objets pour 30 000 points."""

    time: list[str] = Field(min_length=1, description="ISO : 'AAAA', 'AAAA-MM' ou 'AAAA-MM-JJ'")
    value: list[float | None]

    @model_validator(mode="after")
    def _same_length(self) -> "Series":
        if len(self.time) != len(self.value):
            raise ValueError("series.time et series.value doivent avoir la même longueur")
        if self.time != sorted(self.time):
            raise ValueError("series.time doit être trié par ordre croissant")
        if len(set(self.time)) != len(self.time):
            raise ValueError("series.time contient des doublons")
        return self


class Indicator(_Strict):
    schema_version: Literal["1.0"] = SCHEMA_VERSION
    id: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    scale: Scale
    title: str = Field(min_length=1)
    unit: str
    description: str = Field(min_length=1)
    frequency: Frequency
    is_anomaly: bool = Field(description="Valeurs exprimées en écart à reference_period")
    reference_period: Period | None
    series: Series
    trend: Trend | None
    breakpoints: list[Breakpoint] = Field(default_factory=list)
    finding: str = Field(min_length=1, description="Constat en une phrase")
    confidence: Confidence
    limitations: list[str] = Field(min_length=1, description="Au moins une limite explicite")
    provenance: Provenance
    is_demo: bool = False

    @field_validator("limitations")
    @classmethod
    def _no_empty(cls, v: list[str]) -> list[str]:
        if any(not s.strip() for s in v):
            raise ValueError("limitation vide")
        return v

    @model_validator(mode="after")
    def _coherence(self) -> "Indicator":
        if self.is_anomaly and self.reference_period is None:
            raise ValueError("une anomalie exige une reference_period")
        if self.trend and self.trend.significant != (self.trend.p_value < self.trend.alpha):
            raise ValueError("trend.significant incohérent avec p_value et alpha")
        if self.is_demo and "démo" not in self.title.lower():
            raise ValueError("un indicateur de démonstration doit l'afficher dans son titre")
        return self


class ManifestEntry(_Strict):
    id: str
    scale: Scale
    title: str
    unit: str
    path: str = Field(description="Chemin relatif à data/processed")
    confidence: Confidence
    is_demo: bool


class Manifest(_Strict):
    schema_version: Literal["1.0"] = SCHEMA_VERSION
    generated_at: datetime
    etl_version: str
    indicators: list[ManifestEntry]

    @model_validator(mode="after")
    def _unique(self) -> "Manifest":
        keys = [(e.scale, e.id) for e in self.indicators]
        if len(set(keys)) != len(keys):
            raise ValueError("couple (scale, id) dupliqué dans le manifeste")
        return self
