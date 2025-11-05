# MiniStudio – Étape 6 : IA proactive (version essentielle)

MiniStudio est désormais doté d'une **IA proactive** capable de :
- surveiller en continu les fichiers du dossier `fastapi_app/`,
- analyser automatiquement les modifications de code,
- générer des **suggestions intelligentes**,
- permettre leur validation ou rejet,
- appliquer les corrections localement,
- et sauvegarder les rapports d'analyse dans `/reports/`.

## Endpoints disponibles

| Fonction | Endpoint |
|-----------|-----------|
| Vérification IA | `/ai-ping` |
| Analyse / Suggestions | `/ai-suggest` |
| Validation | `/ai-validate?id=&status=` |
| Application | `/ai-apply?id=` |
| Rapport complet | `/ai-report` |
| Génération manuelle de rapport | `/ai-generate-report` |

## Architecture actuelle

- **Backend :** FastAPI (Python)
- **Base de données :** SQLite (`memory/studio.db`)
- **Modules principaux :** `main.py`, `ai_engine.py`, `database.py`
- **Dossiers clés :**
  - `fastapi_app/`
  - `memory/`
  - `reports/`

## À venir (étape 7)
Un **Dashboard essentiel** permettra de visualiser :
- l’état du serveur et de l’IA,
- les suggestions en attente,
- les rapports récents,
- et les fichiers surveillés.

