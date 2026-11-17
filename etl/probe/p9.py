"""Sonde P9 (exploratoire) : données ouvertes pour le Gulf Stream et la circulation de retournement atlantique (AMOC).

1. Câble du détroit de Floride (NOAA AOML) : page des produits, fichiers annuels, mention d'une correction géomagnétique.
2. RAPID 26,5° N : pages de téléchargement (formulaire ou lien direct) et archive BODC. Aucun fichier RAPID téléchargé
   ici : le projet demande une adresse e-mail, la décision revient à Grég.
3. Grilles des zones de Caesar et al. (2018) (gyre subpolaire, région du Gulf Stream), PIK.
4. EN4.2.2 (Met Office) : liste des archives annuelles, taille et contenu d'une archive récente.
Aucun indicateur calculé. Usage : python -m etl.probe.p9   → docs/sonde-p9.md
"""

from __future__ import annotations

import io
import re
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone

from etl.context import ROOT

OUT = ROOT / "docs" / "sonde-p9.md"
UA = {"User-Agent": "projet-evolution-climat (sonde P9 ; github.com/gregfs21-blip/projet-evolution-climat)"}


def get(url: str, limit: int = 600_000_000, method: str | None = None):
    """(statut, URL finale, octets). Les redirections sont suivies ; aucune erreur ne remonte."""
    try:
        req = urllib.request.Request(url, headers=UA, method=method)
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, r.geturl(), (b"" if method == "HEAD" else r.read(limit)), dict(r.headers)
    except urllib.error.HTTPError as exc:
        return exc.code, url, exc.read()[:2000], dict(exc.headers or {})
    except Exception as exc:  # noqa: BLE001
        return f"erreur : {type(exc).__name__} {exc}", url, b"", {}


def links(html: bytes, pattern: str) -> list[str]:
    txt = html.decode("utf-8", "replace")
    return sorted(set(m for m in re.findall(r'href=["\']([^"\']+)["\']', txt) if re.search(pattern, m, re.I)))


def page(url: str, pattern: str, words=()) -> list[str]:
    st, final, data, _ = get(url, limit=5_000_000)
    out = [f"GET {url} → {st} (URL finale : {final}, {len(data)} o)"]
    found = links(data, pattern)
    out.append(f"liens retenus ({len(found)}) :")
    out += [f"  {x}" for x in found[:80]]
    txt = re.sub(r"<[^>]+>", " ", data.decode("utf-8", "replace"))
    for w in words:
        hits = [m.start() for m in re.finditer(w, txt, re.I)]
        out.append(f"mot « {w} » : {len(hits)} occurrence(s)")
        for h in hits[:3]:
            out.append("  … " + " ".join(txt[max(0, h - 200):h + 250].split()) + " …")
    return out


def text_file(url: str, head: int = 12, tail: int = 4) -> list[str]:
    st, final, data, _ = get(url, limit=20_000_000)
    out = [f"GET {url} → {st} ({len(data)} o)"]
    if st == 200 and data:
        lines = data.decode("utf-8", "replace").splitlines()
        out.append(f"{len(lines)} lignes ; début :")
        out += [f"  {x}" for x in lines[:head]]
        out.append("fin :")
        out += [f"  {x}" for x in lines[-tail:]]
    return out


def aoml() -> list[str]:
    base = "https://www.aoml.noaa.gov/phod/floridacurrent/"
    out = page(base + "data_access.php", r"\.(dat|nc|txt|asc|csv|mat|zip)$|transport",
               words=("secular", "geomagnetic", "Volkov", "pressure", "2023"))
    for name in ("FC_cable_transport_1982.dat", "FC_cable_transport_1998.dat", "FC_cable_transport_2000.dat",
                 "FC_cable_transport_2023.dat", "FC_cable_transport_2024.dat", "FC_cable_transport_2025.dat"):
        out += text_file(base + name, head=6, tail=2)
    return out


def rapid() -> list[str]:
    out = []
    for url in ("https://rapid.ac.uk/rapidmoc/rapid_data/datadl.php", "https://rapid.ac.uk/data/data-download",
                "https://rapid.ac.uk/node/10"):
        out += page(url, r"\.nc|\.mat|\.txt|download|form|bodc", words=("e-mail", "email", "version", "licen"))
    out += page("https://doi.org/10.5285/223b34a32dc5c945e0637086abc0f274", r"download|\.nc|\.zip|licen",
                words=("2004", "licen", "download"))
    return out


def caesar() -> list[str]:
    url = "https://www.pik-potsdam.de/~caesar/AMOC_slowdown/"
    out = page(url, r"grid|index|\.txt|\.nc")
    _, final, html, _ = get(url, limit=5_000_000)
    for name in ("sg_grid.txt", "gs_grid.txt"):
        cand = [x for x in links(html, re.escape(name))] or [name]
        full = urllib.request.urljoin(final, cand[0])
        st, _, data, _ = get(full, limit=5_000_000)
        out.append(f"GET {full} → {st} ({len(data)} o)")
        if st == 200 and data:
            rows = [r.split() for r in data.decode("utf-8", "replace").splitlines() if r.strip()]
            out.append(f"  {len(rows)} lignes ; 3 premières : {rows[:3]}")
            try:
                nums = [[float(v) for v in r[:2]] for r in rows if len(r) >= 2]
                a, b = zip(*nums)
                out.append(f"  colonne 1 : {min(a)} → {max(a)} ; colonne 2 : {min(b)} → {max(b)}")
            except Exception as exc:  # noqa: BLE001
                out.append(f"  lecture numérique impossible : {exc}")
    return out


def en4() -> list[str]:
    out = []
    lst_url = "https://www.metoffice.gov.uk/hadobs/en4/EN.4.2.2.analyses.g10.download-list.txt"
    st, _, data, _ = get(lst_url, limit=2_000_000)
    urls = data.decode("utf-8", "replace").split() if st == 200 else []
    out.append(f"GET {lst_url} → {st} ; {len(urls)} archives")
    if urls:
        out += [f"  première : {urls[0]}", f"  dernière : {urls[-1]}"]
    out += page("https://www.metoffice.gov.uk/hadobs/en4/download-en4-2-2.html", r"licen|terms|\.txt$",
                words=("licen", "non commercial", "Non-Commercial"))
    target = next((u for u in urls if u.endswith(".2024.zip")), urls[-2] if len(urls) > 1 else None)
    if not target:
        return out
    target = target.replace("http://", "https://")
    t0 = time.time()
    st, _, blob, hdr = get(target)
    out.append(f"GET {target} → {st} ; {len(blob) / 1e6:.1f} Mo en {time.time() - t0:.0f} s")
    if st != 200 or blob[:2] != b"PK":
        return out
    z = zipfile.ZipFile(io.BytesIO(blob))
    out.append(f"{len(z.namelist())} fichiers : " + ", ".join(f"{i.filename} ({i.file_size / 1e6:.0f} Mo)"
                                                         for i in z.infolist()[:3]) + " …")
    path = OUT.parent / "_p9.nc"
    path.write_bytes(z.read(z.namelist()[0]))
    try:
        import netCDF4
        import numpy as np
        with netCDF4.Dataset(path) as ds:
            out.append("dimensions : " + ", ".join(f"{k}={len(v)}" for k, v in ds.dimensions.items()))
            for attr in ("title", "licence", "license", "references", "history"):
                if hasattr(ds, attr):
                    out.append(f"  {attr} : {str(getattr(ds, attr))[:300]}")
            for name, var in ds.variables.items():
                out.append(f"  {name} {var.dimensions} {var.shape} {getattr(var, 'units', '')} "
                           f"{getattr(var, 'long_name', '')}")
                if name in ("depth", "lat", "lon"):
                    v = np.asarray(var[:], dtype=float)
                    out.append(f"    {v.min():.2f} → {v.max():.2f} ; {list(np.round(v[:25], 1)) if name == 'depth' else ''}")
                elif var.ndim >= 3:
                    a = np.ma.filled(var[:].astype(float), np.nan)
                    out.append(f"    min {np.nanmin(a):.4g}, moyenne {np.nanmean(a):.4g}, max {np.nanmax(a):.4g}")
    finally:
        path.unlink(missing_ok=True)
    st, _, _, hdr = get(urls[0].replace("http://", "https://"), method="HEAD")
    out.append(f"HEAD {urls[0]} → {st} ; taille annoncée {hdr.get('Content-Length', '?')} o")
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    md = ["# Sonde P9 — Gulf Stream et AMOC (généré)", "",
          f"Généré par `python -m etl.probe.p9` le {now}. Aucun indicateur calculé."]
    for title, fn in (("1. Câble du détroit de Floride (NOAA AOML)", aoml),
                      ("2. RAPID 26,5° N : accès", rapid),
                      ("3. Zones de Caesar et al. (2018)", caesar),
                      ("4. EN4.2.2 : archives et contenu", en4)):
        try:
            body = fn()
        except Exception as exc:  # noqa: BLE001
            body = [f"échec : {type(exc).__name__} {exc}"]
        md += ["", f"## {title}", "", "```", *body, "```"]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
