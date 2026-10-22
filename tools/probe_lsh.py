"""Sonde temporaire : récupère les documents de référence de la validation P1 (lecture locale).
Chaque échec est consigné dans probe/erreurs.txt au lieu d'interrompre la sonde."""
import urllib.request, pathlib, traceback
OUT = pathlib.Path("probe"); OUT.mkdir(exist_ok=True)
BASE = "fileadmin/user_upload/National/FAL_commun/publications/Nouvelle-Aquitaine/"
DOCS = {
    "oracle-na-2020.pdf": [f"https://{h}.chambre-agriculture.fr/{BASE}2020_ORACLE_Nouvelle_Aquitaine.pdf"
                           for h in ("creuse", "nouvelle-aquitaine", "charente", "correze", "gironde", "cmds")],
}
errors = []
for name, urls in DOCS.items():
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Firefox/130.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if data[:4] == b"%PDF":
                (OUT / name).write_bytes(data); errors.append(f"OK {url}"); break
            errors.append(f"pas un PDF : {url}")
        except Exception as e:
            errors.append(f"{url} : {e!r}")
(OUT / "erreurs.txt").write_text("\n".join(errors))
print("\n".join(errors))
