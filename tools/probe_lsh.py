"""Sonde temporaire : récupère les documents de référence de la validation P1 (lecture locale)."""
import urllib.request, pathlib
OUT = pathlib.Path("probe"); OUT.mkdir(exist_ok=True)
DOCS = {
    "oracle-na-2020.pdf": "https://creuse.chambre-agriculture.fr/fileadmin/user_upload/National/FAL_commun/publications/Nouvelle-Aquitaine/2020_ORACLE_Nouvelle_Aquitaine.pdf",
}
for name, url in DOCS.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 projet-evolution-climat"})
    with urllib.request.urlopen(req, timeout=120) as r:
        (OUT / name).write_bytes(r.read())
print(sorted(p.name for p in OUT.iterdir()))
