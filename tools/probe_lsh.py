"""Sonde temporaire : récupère la documentation LSH et les séries TN/TX complètes de Gironde."""
import io, urllib.request, zipfile, pathlib

BASE = "https://meteofrance.s3.sbg.io.cloud.ovh.net/data/synchro_ftp/REF_CC/LSH/"
DOC = "https://static.data.gouv.fr/resources/donnees-changement-climatique-lsh-longues-series-homogeneisees/20260709-100626/climatologie-description-lsh-20260709.pdf"
OUT = pathlib.Path("probe"); OUT.mkdir(exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "projet-evolution-climat/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

(OUT / "description-lsh.pdf").write_bytes(get(DOC))
for var in ("TN", "TX"):
    z = zipfile.ZipFile(io.BytesIO(get(f"{BASE}SH_{var}_metropole.zip")))
    for n in z.namelist():
        if n[8:10] == "33":   # SH_MTNx33...: département 33
            (OUT / n).write_bytes(z.read(n))
print(sorted(p.name for p in OUT.iterdir()))
