# Évolution climatique — Gironde, France, monde

Étude de l'évolution du climat à partir de données ouvertes, publiée sous forme de tableau de bord.
Chaque chiffre affiché est traçable jusqu'à sa source et au script qui l'a produit.

## Architecture

```
Sources ouvertes ──► ETL Python (GitHub Actions, mensuel) ──► data/processed/*.json ──► Site Next.js (Vercel)
                     télécharge, contrôle, calcule             contrat validé              affiche, ne calcule rien
```

| Dossier | Rôle |
|---|---|
| `etl/` | Calcul scientifique. `schema.py` = contrat de données, `pipeline.py` = orchestrateur, `config/indicators.yaml` = registre des indicateurs |
| `data/processed/` | Résultats publiés (JSON + `manifest.json`). Seule interface entre l'ETL et le site |
| `data/raw/` | Cache des téléchargements, hors Git |
| `web/` | Site Next.js (App Router, TypeScript, Tailwind, ECharts, zod) |
| `.github/workflows/` | `ci.yml` (tests à chaque push), `etl.yml` (exécution mensuelle) |
| `docs/` | Sources, méthode, journal des phases |

Le contrat de données existe en deux exemplaires qui doivent rester identiques :
`etl/schema.py` (pydantic) et `web/lib/schema.ts` (zod). Un JSON non conforme est refusé
par la CI côté Python, puis par le build côté site.

## Ajouter un indicateur

1. Écrire un module `etl/sources/<source>.py` exposant `build(ctx) -> Indicator`.
2. Le déclarer dans `etl/config/indicators.yaml`.
3. `python -m etl.pipeline --only <id>` puis `python -m etl.validate`.

La page `/<échelle>/<id>` apparaît automatiquement au build suivant. Aucun code côté site.

## Lancer en local

```bash
pip install -r etl/requirements.txt
python -m etl.pipeline && python -m etl.validate
python -m pytest etl/tests

cd web && npm install && npm run dev     # http://localhost:3000
```

## Déploiement Vercel

Projet Vercel relié à ce dépôt, **Root Directory = `web`**, option « Include files outside the
root directory » activée (le build lit `../data/processed`). Chaque commit sur `main`,
y compris ceux de l'ETL mensuel, redéploie le site.

## État

- **P0** (socle) : close le 22/10/2026.
- **P1** (températures homogénéisées de Gironde) : close le 23/10/2026. 20 indicateurs, validés contre
  ClimatHD et recoupés avec ERA5. Voir `docs/validation-p1.md`.
