"""Sonde P11 (localités la plus chaude et la plus froide à l'instant t) : sources temps réel candidates.

1. Observations METAR mondiales (NOAA Aviation Weather Center) : fichier cache de toutes les stations, mis à jour en
   continu. Taille, colonnes, nombre de stations, âge des observations, couverture (Antarctique, déserts), valeurs
   extrêmes brutes et en-têtes CORS (lecture possible depuis le navigateur ?).
2. API METAR de l'AWC (JSON) : format et CORS.
3. Open-Meteo, température « actuelle » du modèle sur plusieurs points à la fois : limites, CORS, cohérence avec les
   METAR extrêmes du moment.
Aucun indicateur publié, aucun choix fait. Usage : python -m etl.probe.p11   → docs/sonde-p11.md
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p11.md"
UA = {"User-Agent": "projet-evolution-climat (sonde P11 ; github.com/gregfs21-blip/projet-evolution-climat)",
      "Origin": "https://projet-evolution-climat.vercel.app"}
METAR_CACHE = "https://aviationweather.gov/data/cache/metars.cache.csv.gz"
METAR_API = "https://aviationweather.gov/api/data/metar?ids=LFBD,NZSP,OERK,KDRA&format=json"


def get(url: str, limit: int = 50_000_000):
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read(limit)
            return r.status, dict(r.headers), data, time.time() - t0
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers or {}), exc.read()[:2000], time.time() - t0
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}", {}, b"", time.time() - t0


def headers_line(h: dict) -> str:
    keys = ("Content-Type", "Content-Length", "Last-Modified", "Cache-Control", "Access-Control-Allow-Origin",
            "Content-Encoding")
    return " ; ".join(f"{k}={h.get(k) or h.get(k.lower())}" for k in keys if h.get(k) or h.get(k.lower()))


def metar_cache() -> tuple[list[str], list[dict]]:
    st, h, data, dt = get(METAR_CACHE)
    out = [f"GET {METAR_CACHE} → {st} en {dt:.1f} s, {len(data)} o", f"en-têtes : {headers_line(h)}"]
    rows: list[dict] = []
    if st != 200 or not data:
        return out, rows
    try:
        text = gzip.decompress(data).decode("utf-8", "replace")
    except OSError:
        text = data.decode("utf-8", "replace")
    lines = text.splitlines()
    head = next(i for i, ln in enumerate(lines) if ln.startswith("raw_text"))
    out.append(f"{len(lines)} lignes ; préambule : {lines[:head]}")
    out.append(f"colonnes : {lines[head]}")
    rows = list(csv.DictReader(io.StringIO("\n".join(lines[head:]))))
    now = datetime.now(timezone.utc)
    ok = []
    for r in rows:
        try:
            t = float(r["temp_c"])
            obs = datetime.fromisoformat(r["observation_time"].replace("Z", "+00:00"))
            ok.append((t, (now - obs).total_seconds() / 60, r))
        except (ValueError, KeyError):
            continue
    out.append(f"stations : {len(rows)} ; avec température : {len(ok)}")
    ages = sorted(a for _, a, _ in ok)
    if ages:
        q = lambda p: ages[int(p * (len(ages) - 1))]  # noqa: E731
        out.append(f"âge des observations (min) : médiane {q(0.5):.0f}, 90 % {q(0.9):.0f}, max {ages[-1]:.0f}")
    lat = [float(r["latitude"]) for _, _, r in ok if r.get("latitude")]
    out.append(f"stations au sud de 60° S : {sum(1 for x in lat if x < -60)} ; au nord de 70° N : "
               f"{sum(1 for x in lat if x > 70)}")
    srt = sorted(ok, key=lambda x: x[0])
    out.append("10 plus chaudes (brut, sans contrôle) :")
    out += [f"  {t:+.1f} °C {r['station_id']} ({r['latitude']}, {r['longitude']}) âge {a:.0f} min : {r['raw_text'][:90]}"
            for t, a, r in srt[-10:][::-1]]
    out.append("10 plus froides (brut, sans contrôle) :")
    out += [f"  {t:+.1f} °C {r['station_id']} ({r['latitude']}, {r['longitude']}) âge {a:.0f} min : {r['raw_text'][:90]}"
            for t, a, r in srt[:10]]
    return out, rows


def stations(rows: list[dict]) -> list[str]:
    """Noms des stations (le cache METAR n'en donne pas) et présence de quelques stations clés dans le cache."""
    out = []
    for url in ("https://aviationweather.gov/data/cache/stations.cache.json.gz",
                "https://aviationweather.gov/api/data/stationinfo?ids=FYKT,UEEE,NZSP,LFBD&format=json"):
        st, h, data, dt = get(url)
        out += [f"GET {url} → {st} en {dt:.1f} s, {len(data)} o", f"en-têtes : {headers_line(h)}"]
        if st == 200 and data:
            try:
                raw = gzip.decompress(data) if url.endswith(".gz") else data
                js = json.loads(raw)
                out.append(f"{len(js)} stations ; exemple : {json.dumps(js[0], ensure_ascii=False)[:400]}")
            except Exception as exc:  # noqa: BLE001
                out.append(f"lecture : {exc}")
    ids = {r["station_id"] for r in rows}
    for sid in ("NZSP", "NZCM", "FYKT", "KDRA", "OIZB", "UEEE", "LFBD", "BGSC"):
        out.append(f"{sid} dans le cache METAR : {'oui' if sid in ids else 'non'}")
    return out


def metar_api() -> list[str]:
    st, h, data, dt = get(METAR_API)
    out = [f"GET {METAR_API} → {st} en {dt:.1f} s", f"en-têtes : {headers_line(h)}"]
    if st == 200:
        try:
            js = json.loads(data)
            out.append(f"{len(js)} enregistrements ; clés : {sorted(js[0].keys()) if js else '-'}")
            out += [f"  {x.get('icaoId')} {x.get('temp')} °C {x.get('reportTime')} {x.get('name')}" for x in js]
        except Exception as exc:  # noqa: BLE001
            out.append(f"lecture : {exc}")
    return out


def open_meteo(rows: list[dict]) -> list[str]:
    out = []
    # Points de test : quelques stations METAR extrêmes du moment, plus des déserts et l'Antarctique.
    pts = [(36.46, -116.87, "Vallée de la Mort"), (24.8, 46.7, "Riyad"), (31.0, 58.3, "Désert de Lut"),
           (-78.46, 106.84, "Vostok"), (-90.0, 0.0, "Pôle Sud"), (67.55, 133.38, "Verkhoïansk"),
           (44.83, -0.69, "Bordeaux-Mérignac")]
    temps = []
    for r in rows:
        try:
            temps.append((float(r["temp_c"]), float(r["latitude"]), float(r["longitude"]), r["station_id"]))
        except (ValueError, KeyError):
            pass
    temps.sort()
    pts += [(la, lo, f"METAR {sid} ({t:+.1f} °C)") for t, la, lo, sid in temps[-3:] + temps[:3]]
    lat = ",".join(f"{p[0]}" for p in pts)
    lon = ",".join(f"{p[1]}" for p in pts)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
    st, h, data, dt = get(url)
    out += [f"GET {url[:160]}… → {st} en {dt:.1f} s", f"en-têtes : {headers_line(h)}"]
    if st == 200:
        js = json.loads(data)
        js = js if isinstance(js, list) else [js]
        for p, j in zip(pts, js):
            c = j.get("current", {})
            out.append(f"  {p[2]} ({p[0]}, {p[1]}) : {c.get('temperature_2m')} °C à {c.get('time')} "
                       f"(intervalle {c.get('interval')} s ; altitude du modèle {j.get('elevation')} m)")
    # Limite du nombre de points par requête
    n = 1000
    lat = ",".join(str(round(-60 + (i % 50) * 2.4, 2)) for i in range(n))
    lon = ",".join(str(round(-180 + (i // 50) * 18, 2)) for i in range(n))
    st, _, data, dt = get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m")
    out.append(f"requête de {n} points → {st} en {dt:.1f} s ; {data[:200]!r}" if st != 200 else
               f"requête de {n} points → 200 en {dt:.1f} s, {len(json.loads(data))} réponses")
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P11 — localités extrêmes à l'instant t (généré)", "",
          f"Généré par `python -m etl.probe.p11` le {now}, depuis GitHub Actions. Aucun indicateur, aucun choix."]
    rows: list[dict] = []
    sections = []
    try:
        body, rows = metar_cache()
    except Exception as exc:  # noqa: BLE001
        body = [f"échec : {type(exc).__name__} {exc}"]
    sections.append(("1. METAR mondiaux, fichier cache de l'AWC (NOAA)", body))
    for title, fn in (("2. API METAR de l'AWC (JSON)", metar_api),
                      ("2 bis. Noms des stations", lambda: stations(rows)),
                      ("3. Open-Meteo, température actuelle du modèle", lambda: open_meteo(rows))):
        try:
            body = fn()
        except Exception as exc:  # noqa: BLE001
            body = [f"échec : {type(exc).__name__} {exc}"]
        sections.append((title, body))
    for title, body in sections:
        md += ["", f"## {title}", "", "```", *body, "```"]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
