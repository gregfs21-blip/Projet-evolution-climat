"""Test de Mann-Kendall classique et modifié de Hamed-Rao (1998).

Code repris de pymannkendall (Md. Manjurul Hussain Shourov, licence MIT), commit
ec2e3ab16b4299517bd69b9f1ca949580797cd6d (22/03/2025), fonctions `original_test`
et `hamed_rao_modification_test` et leurs utilitaires, réduits aux séries sans
lacune. Seules modifications : noms des fonctions, docstrings, suppression du
pré-traitement des lacunes (refusées en amont par etl.stats.trend).

Pourquoi l'embarquer plutôt que l'installer :
- la 1.4.3 publiée sur PyPI peut rendre la variance corrigée négative (p = NaN),
  corrigé en amont par le commit ci-dessus (issue 29) mais jamais publié ;
- ce commit ne s'installe pas depuis GitHub sous Python ≥ 3.12 (versioneer obsolète).
La 1.4.3 reste utilisée dans les tests, pour recouper ces fonctions sur les
séries où elle est valide.

Le correctif amont borne le facteur de correction n/n* à ≥ 1 (abs(sni)) : en cas
d'autocorrélation négative, le test reste aussi exigeant que le test classique au
lieu de devenir plus permissif. Écart conservateur à la méthode originale.

---
MIT License — Copyright (c) 2019 Md. Manjurul Hussain Shourov

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions: The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS",
WITHOUT WARRANTY OF ANY KIND.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import norm, rankdata


@dataclass(frozen=True)
class MKResult:
    p: float
    z: float
    s: float
    var_s: float


def _acf(x: np.ndarray, nlags: int) -> np.ndarray:
    y = x - x.mean()
    n = len(x)
    d = n * np.ones(2 * n - 1)
    acov = (np.correlate(y, y, "full") / d)[n - 1 :]
    return acov[: nlags + 1] / acov[0] if acov[0] != 0 else acov[: nlags + 1]


def _mk_score(x: np.ndarray) -> float:
    n = len(x)
    s = 0.0
    for k in range(n - 1):
        s += np.sum(x[k + 1 :] > x[k]) - np.sum(x[k + 1 :] < x[k])
    return s


def _variance_s(x: np.ndarray) -> float:
    n = len(x)
    unique_x, counts = np.unique(x, return_counts=True)
    if len(unique_x) == n:
        return n * (n - 1) * (2 * n + 5) / 18
    tp = counts.astype(float)
    return (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18


def _z_score(s: float, var_s: float) -> float:
    if s > 0:
        return (s - 1) / np.sqrt(var_s)
    if s < 0:
        return (s + 1) / np.sqrt(var_s)
    return 0.0


def _p_value(z: float) -> float:
    return float(2 * (1 - norm.cdf(abs(z))))


def _sens_slope_index(x: np.ndarray) -> float:
    n = len(x)
    d = [(x[j] - x[i]) / (j - i) for i in range(n - 1) for j in range(i + 1, n)]
    return float(np.median(d))


def original_test(x) -> MKResult:
    x = np.asarray(x, dtype=float)
    s, var_s = _mk_score(x), _variance_s(x)
    z = _z_score(s, var_s)
    return MKResult(p=_p_value(z), z=z, s=s, var_s=var_s)


def hamed_rao_test(x, alpha: float = 0.05) -> MKResult:
    x = np.asarray(x, dtype=float)
    n = len(x)
    s, var_s = _mk_score(x), _variance_s(x)
    lag = n
    # Autocorrélation des rangs de la série détendancée (pente de Sen en indice).
    x_detrend = x - np.arange(1, n + 1) * _sens_slope_index(x)
    acf = _acf(rankdata(x_detrend), nlags=lag - 1)
    bound = norm.ppf(1 - alpha / 2) / np.sqrt(n)
    sni = 0.0
    for i in range(1, lag):
        if not (-bound <= acf[i] <= bound):          # seules les autocorrélations significatives
            sni += (n - i) * (n - i - 1) * (n - i - 2) * acf[i]
    n_ns = 1 + (2 / (n * (n - 1) * (n - 2))) * abs(sni)   # correctif amont (issue 29)
    var_s = var_s * n_ns
    z = _z_score(s, var_s)
    return MKResult(p=_p_value(z), z=z, s=s, var_s=var_s)
