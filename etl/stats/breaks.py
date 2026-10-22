"""Détection de rupture : test de Pettitt (1979).

Implémenté ici plutôt qu'importé : le calcul tient en quelques lignes et la
p-value approchée de Pettitt est déterministe, alors que la bibliothèque de
référence (pyhomogeneity) l'estime par Monte-Carlo, donc avec un résultat qui
varie d'une exécution à l'autre. Le code est vérifié contre pyhomogeneity
dans les tests (même point de rupture, même statistique U).

Sur une série homogénéisée, une rupture détectée peut être climatique (saut
réel) ou un artefact résiduel. Elle n'est interprétable que si elle ne
coïncide pas avec une rupture d'homogénéité corrigée (critère C6).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PettittResult:
    index: int          # dernier indice du premier segment
    u: float            # statistique K = max |U_t|
    p_value: float      # approximation de Pettitt, bornée à 1
    mean_before: float
    mean_after: float


def pettitt(values: list[float] | np.ndarray) -> PettittResult:
    x = np.asarray(values, dtype=float)
    if np.isnan(x).any():
        raise ValueError("Pettitt : la série ne doit pas contenir de lacune")
    n = len(x)
    if n < 10:
        raise ValueError("Pettitt : au moins 10 valeurs")
    # U_t = somme_{i<=t} somme_{j>t} sign(x_j - x_i), calculé via la matrice des signes.
    sign = np.sign(x[None, :] - x[:, None])          # sign[i, j] = sign(x_j - x_i)
    u = np.array([sign[: t + 1, t + 1 :].sum() for t in range(n - 1)])
    t = int(np.argmax(np.abs(u)))
    k = float(np.abs(u[t]))
    p = min(1.0, 2.0 * np.exp(-6.0 * k**2 / (n**3 + n**2)))
    return PettittResult(index=t, u=k, p_value=p, mean_before=float(x[: t + 1].mean()), mean_after=float(x[t + 1 :].mean()))
