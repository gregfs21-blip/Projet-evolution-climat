"""Sonde Copernicus Climate Data Store (ERA5 niveaux de pression, moyennes mensuelles).

Vérifie l'accès (compte, clé, licence acceptée), le délai de file d'attente et le format réel des fichiers AVANT
d'écrire le lecteur. Aucun résultat climatique. La clé vient du secret GitHub CDSAPI_KEY : jamais affichée.
Usage : python -m etl.probe.cds   → écrit docs/sonde-cds.md
"""

from __future__ import annotations

import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-cds.md"
DATASET = "reanalysis-era5-pressure-levels-monthly-means"
BASE = {"product_type": ["monthly_averaged_reanalysis"], "time": ["00:00"], "data_format": "netcdf",
        "download_format": "unarchived"}

REQUESTS = [
    ("1. Point de Bordeaux, 3 variables × 3 niveaux, 1940-2025 (la série dont les indicateurs auront besoin)",
     {"variable": ["temperature", "geopotential", "u_component_of_wind"], "pressure_level": ["250", "500", "850"],
      "year": [str(y) for y in range(1940, 2026)], "month": [f"{m:02d}" for m in range(1, 13)],
      "area": [45.0, -1.0, 44.5, -0.5]}),
    ("2. Atlantique Nord (60° O-0°, 20-70° N), vent zonal 250 hPa, grille 1°, janvier 2024",
     {"variable": ["u_component_of_wind"], "pressure_level": ["250"], "year": ["2024"], "month": ["01"],
      "area": [70.0, -60.0, 20.0, 0.0], "grid": ["1.0", "1.0"]}),
    ("3. Globe, température 850 hPa, grille 2,5°, 12 mois de 2024",
     {"variable": ["temperature"], "pressure_level": ["850"], "year": ["2024"],
      "month": [f"{m:02d}" for m in range(1, 13)], "grid": ["2.5", "2.5"]}),
    ("4. Point de Bordeaux, température 850 hPa, 1940-2025 (série complète : délai réel de la file)",
     {"variable": ["temperature"], "pressure_level": ["850"], "year": [str(y) for y in range(1940, 2026)],
      "month": [f"{m:02d}" for m in range(1, 13)], "area": [45.0, -1.0, 44.5, -0.5]}),
]


def describe(path: Path) -> list[str]:
    data = path.read_bytes()
    lines = [f"{len(data) / 1e3:.0f} ko, début {data[:8]!r}"]
    try:
        import netCDF4
        with netCDF4.Dataset(path) as ds:
            lines.append("dimensions : " + ", ".join(f"{k}={len(v)}" for k, v in ds.dimensions.items()))
            for name, var in ds.variables.items():
                attrs = {a: getattr(var, a) for a in ("units", "long_name") if a in var.ncattrs()}
                try:
                    import numpy as np
                    head = np.asarray(var[:]).ravel()[:4].tolist() if var.size else []
                except Exception as exc:  # noqa: BLE001
                    head = f"illisible ({exc})"
                lines.append(f"  {name} {var.dimensions} {var.shape} {attrs} : {head}")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"lecture netCDF impossible : {type(exc).__name__} {exc}")
    return lines


DEADLINES = [40, 0, 0, 0]   # minutes ; 0 = requête non soumise. Sonde du 25/10 (22 h) : file saturée, et le CDS
                              # refuse au-delà d'un nombre de requêtes en attente par utilisateur → une à la fois.
API = os.environ.get("CDSAPI_URL", "https://cds.climate.copernicus.eu/api")


def _api(path: str) -> dict:
    import json
    import urllib.request
    req = urllib.request.Request(f"{API}/retrieve/v1/{path}", headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", "")})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def _download(href: str, path: Path, max_seconds: int = 300, max_mb: float = 200) -> str:
    """Téléchargement par morceaux avec une durée TOTALE bornée (un serveur lent ne doit pas bloquer la sonde)."""
    import urllib.request
    t0, size = time.time(), 0
    req = urllib.request.Request(href, headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", "")})
    with urllib.request.urlopen(req, timeout=60) as r, path.open("wb") as f:
        total = r.headers.get("Content-Length")
        if total and int(total) > max_mb * 1e6:
            return f"non téléchargé : {int(total) / 1e9:.1f} Go (au-delà de {max_mb:.0f} Mo, pas une requête de la sonde)"
        while chunk := r.read(1 << 20):
            f.write(chunk)
            size += len(chunk)
            if time.time() - t0 > max_seconds:
                return f"interrompu après {max_seconds} s : {size / 1e6:.1f} Mo sur {int(total) / 1e6 if total else '?'} Mo"
    return f"{size / 1e6:.2f} Mo en {time.time() - t0:.0f} s"


def jobs_report(tmp: str, md: list[str]) -> None:
    """Travaux déjà soumis : état (écrit tout de suite), puis lecture des résultats de ceux qui ont abouti."""
    def flush():
        OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    md += ["", "### 0. Travaux déjà soumis", "", "```"]
    try:
        jobs = _api("jobs?limit=20").get("jobs", [])
    except Exception as exc:  # noqa: BLE001
        md += [f"liste des travaux impossible : {type(exc).__name__} {exc}", "```"]
        flush()
        return
    for j in jobs:
        md.append(f"{j.get('jobID')} {j.get('status')} créé {j.get('created')} début {j.get('started')} fin {j.get('finished')}")
        if j.get("status") in ("rejected", "failed") and j.get("created", "") >= "2026-10-26":
            try:
                _api(f"jobs/{j['jobID']}/results")
            except Exception as exc:  # noqa: BLE001
                body = getattr(exc, "read", lambda: b"")()[:600].decode("utf-8", "replace")
                md.append(f"    motif : {body}")
    md.append("```")
    flush()
    for j in [j for j in jobs if j.get("status") == "successful"][:4]:
        lines = [f"Résultat du travail {j['jobID']} :"]
        try:
            href = _api(f"jobs/{j['jobID']}/results")["asset"]["value"]["href"]
            path = Path(tmp) / f"{j['jobID']}.nc"
            lines.append(_download(href, path))
            lines += describe(path)
        except Exception as exc:  # noqa: BLE001
            lines.append(f"résultat illisible : {type(exc).__name__} {exc}")
        md += ["", "```", *lines, "```"]
        flush()


def wait_queue_empty(max_minutes: int) -> str:
    t0 = time.time()
    while time.time() - t0 < max_minutes * 60:
        try:
            pending = [j for j in _api("jobs?limit=50").get("jobs", []) if j.get("status") in ("accepted", "running")]
        except Exception as exc:  # noqa: BLE001
            return f"état de la file illisible : {exc}"
        if not pending:
            return f"aucun travail en attente (après {time.time() - t0:.0f} s)"
        time.sleep(60)
    return f"encore {len(pending)} travail(aux) en attente après {max_minutes} min"


def _retrieve(req: dict, path: str, queue) -> None:
    """Processus fils : une requête, résultat renvoyé par la file (le parent peut l'arrêter à l'échéance)."""
    try:
        import cdsapi
        client = cdsapi.Client(url=os.environ.get("CDSAPI_URL", "https://cds.climate.copernicus.eu/api"),
                               key=os.environ.get("CDSAPI_KEY"), quiet=True, progress=False)
        client.retrieve(DATASET, {**BASE, **req}, path)
        queue.put(("ok", ""))
    except Exception as exc:  # noqa: BLE001
        msg = str(exc).replace(os.environ.get("CDSAPI_KEY") or "§§", "***")
        queue.put(("err", f"{type(exc).__name__} : {msg[:1500]}"))


# Requêtes utiles (25-26/10/2026) : le CDS met des HEURES à les traiter (file de 3 à 7 h constatée) ; elles sont
# donc soumises sans attendre, et leurs résultats relevés par une exécution ultérieure (liste des travaux ci-dessus).
USEFUL = {
    "bordeaux-1940-2025": {"variable": ["temperature", "geopotential", "u_component_of_wind"],
                           "pressure_level": ["250", "500", "850"], "year": [str(y) for y in range(1940, 2026)],
                           "month": [f"{m:02d}" for m in range(1, 13)], "area": [45.0, -1.0, 44.5, -0.5]},
    "atlantique-u250-1940-2025": {"variable": ["u_component_of_wind"], "pressure_level": ["250"],
                                  "year": [str(y) for y in range(1940, 2026)], "month": [f"{m:02d}" for m in range(1, 13)],
                                  "area": [70.0, -60.0, 20.0, 0.0], "grid": ["1.0", "1.0"]},
}
MAX_PENDING = 4      # le CDS a rejeté la 5e requête en attente le 25/10/2026


# Requêtes de test du 25/10/2026 (un mois, janvier 2024) restées en file : inutiles, elles occupent le quota de
# requêtes en attente. Annulées (26/10/2026) pour laisser passer les requêtes utiles.
OBSOLETE = ("14c71edd-e872-46c9-999b-41277d0bc5de", "55875211-dff8-4682-abca-59c589116bf2")


def cancel_obsolete(md: list[str]) -> None:
    import urllib.request
    lines = []
    for jid in OBSOLETE:
        try:
            req = urllib.request.Request(f"{API}/retrieve/v1/jobs/{jid}", method="DELETE",
                                         headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", "")})
            with urllib.request.urlopen(req, timeout=60) as r:
                lines.append(f"{jid} : annulé ({r.status})")
        except Exception as exc:  # noqa: BLE001
            lines.append(f"{jid} : {type(exc).__name__} {exc}")
    md += ["", "### Annulation des requêtes de test inutiles", "", "```", *lines, "```"]


def submit_useful(md: list[str]) -> None:
    import json
    import urllib.request
    try:
        jobs = _api("jobs?limit=50").get("jobs", [])
        pending = [j for j in jobs if j.get("status") in ("accepted", "running")]
        # Une requête déjà soumise (même contenu) n'est jamais resoumise.
        known = []
        for j in jobs:
            if j.get("status") in ("accepted", "running", "successful"):
                try:
                    known.append(_api(f"jobs/{j['jobID']}?request=true").get("metadata", {}).get("request", {}).get("ids", {}))
                except Exception:  # noqa: BLE001
                    pass
    except Exception as exc:  # noqa: BLE001
        md += ["", f"Soumission impossible : {type(exc).__name__} {exc}"]
        return
    lines = []
    for name, req in USEFUL.items():
        body = {**BASE, **req}
        if any(k and k.get("variable") == body["variable"] and k.get("area") == body.get("area") and
               len(k.get("year", [])) == len(body["year"]) for k in known):
            lines.append(f"{name} : déjà soumise")
            continue
        if len(pending) >= MAX_PENDING:
            lines.append(f"{name} : non soumise, {len(pending)} travaux déjà en attente")
            continue
        try:
            req_ = urllib.request.Request(f"{API}/retrieve/v1/processes/{DATASET}/execution",
                                          data=json.dumps({"inputs": body}).encode(), method="POST",
                                          headers={"PRIVATE-TOKEN": os.environ.get("CDSAPI_KEY", ""),
                                                   "Content-Type": "application/json"})
            with urllib.request.urlopen(req_, timeout=60) as r:
                job = json.loads(r.read())
            pending.append(job)
            lines.append(f"{name} : soumise, travail {job.get('jobID')} ({job.get('status')})")
        except Exception as exc:  # noqa: BLE001
            detail = getattr(exc, "read", lambda: b"")()[:500]
            lines.append(f"{name} : ÉCHEC {type(exc).__name__} {exc} {detail!r}")
    md += ["", "### Soumission des requêtes utiles (sans attendre)", "", "```", *lines, "```"]


def main() -> int:
    import multiprocessing as mp
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde Copernicus CDS — ERA5 niveaux de pression, moyennes mensuelles (généré)", "",
          f"Généré par `python -m etl.probe.cds` le {now}. Aucun calcul : accès, délais et format constatés.", "",
          f"Jeu de données : `{DATASET}`.", "",
          f"Clé présente dans l'environnement : **{'oui' if os.environ.get('CDSAPI_KEY') else 'NON'}** (jamais affichée)."]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        jobs_report(tmp, md)
        cancel_obsolete(md)
        submit_useful(md)
        OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
        md += ["", "Mode relevé : aucune requête bloquante (le CDS traite en plusieurs heures)."]
        OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
        return 0
        state = wait_queue_empty(10)
        md += ["", "File : " + state]
        OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
        if not state.startswith("aucun travail"):
            # Travaux précédents encore en file : on n'en ajoute pas (le CDS rejette au-delà d'une limite par utilisateur).
            md += ["", "Aucune nouvelle requête soumise : travaux précédents encore en file."]
            OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
            return 0
        for i, ((title, req), minutes) in enumerate(zip(REQUESTS, DEADLINES)):
            if not minutes:
                continue
            path = Path(tmp) / f"r{i}.nc"
            q = mp.Queue()
            proc = mp.Process(target=_retrieve, args=(req, str(path), q))
            t0 = time.time()
            proc.start()
            proc.join(minutes * 60)
            if proc.is_alive():
                proc.terminate()
                proc.join(10)
                lines = [f"PAS DE RÉPONSE après {minutes} min (requête encore en file d'attente ou en cours chez Copernicus)"]
            else:
                status, msg = q.get() if not q.empty() else ("err", "processus terminé sans résultat")
                lines = ([f"OK en {time.time() - t0:.0f} s"] + describe(path)) if status == "ok" else \
                        [f"ÉCHEC après {time.time() - t0:.0f} s", msg]
            md += ["", f"### {title}", "", "```", *lines, "```"]
            OUT.write_text("\n".join(md) + "\n", encoding="utf-8")     # rapport écrit au fil de l'eau
            print(title, "→", lines[0], flush=True)
    print(f"→ {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
