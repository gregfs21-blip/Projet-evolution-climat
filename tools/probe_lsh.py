"""Sonde temporaire : inventorie le jeu LSH de data.gouv.fr (structure des fichiers).

Produit probe/ avec la liste des ressources, l'en-tête de chaque CSV et les lignes
concernant la Gironde (département 33). Ne fait aucun calcul.
"""
import io, json, urllib.request, zipfile, csv, pathlib

DATASET = "https://www.data.gouv.fr/api/1/datasets/6569b2c4f1937611d4c8b1a3/"
OUT = pathlib.Path("probe"); OUT.mkdir(exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "projet-evolution-climat/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

meta = json.loads(get(DATASET))
lines = []
for res in meta["resources"]:
    lines.append(f"## {res['title']} | {res.get('format')} | {res.get('filesize')} | {res['url']}\n{(res.get('description') or '')[:500]}\n")
    try:
        blob = get(res["url"])
    except Exception as e:
        lines.append(f"ERREUR téléchargement : {e}\n"); continue
    members = []
    if blob[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(blob))
        for n in z.namelist():
            members.append((n, z.read(n)))
        lines.append("ZIP : " + ", ".join(n for n, _ in members) + "\n")
    else:
        members.append((res["title"], blob))
    for name, data in members:
        if name.lower().endswith(".pdf"):
            continue
        text = None
        for enc in ("utf-8", "latin-1"):
            try:
                text = data.decode(enc); break
            except UnicodeDecodeError:
                pass
        rows = text.splitlines()
        lines.append(f"### {name} ({len(rows)} lignes, {len(data)} o)\n```\n" + "\n".join(rows[:6]) + "\n```\n")
        g33 = [r for r in rows if ";33" in r[:40] or "MERIGNAC" in r.upper() or "BORDEAUX" in r.upper() or r.startswith("33")]
        if g33:
            lines.append(f"Lignes Gironde (max 40 sur {len(g33)}) :\n```\n" + "\n".join(g33[:40]) + "\n```\n")
(OUT / "inventaire.md").write_text("\n".join(lines), encoding="utf-8")
print("ok", len(meta["resources"]))
