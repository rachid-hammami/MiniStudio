# Cahier des Charges — MiniStudioGPT v1.4.6 “Cortex Sync Layer — Édition Finale”

**Date :** 2025-11-08 09:29:33  
**Auteur :** Code GPT & Rachid  
**Version précédente :** v1.4.5 (Structure & Map Update)  
**Version suivante :** v1.5 (CORTEX Engine)

---

## 🧠 Objectif principal

Mettre en place la **Cortex Sync Layer**, une couche d’API assurant la synchronisation cognitive entre **MiniStudio** (backend FastAPI), la **mémoire persistante**, et un **agent GPT distant**.  
Cette étape établit la communication bidirectionnelle et l’auto-cohérence du système avant l’intégration du **Cortex Engine (v1.5)**.

---

## ⚙️ Description fonctionnelle

### 🎯 But
Créer un ensemble d’endpoints REST et de mécanismes internes permettant :

1. La **lecture/écriture cohérente de la mémoire interne** (`memory/memoire.json`)
2. La **synchronisation automatique** entre CI/CD ↔ mémoire ↔ Cortex
3. L’**accès structuré au contexte** du projet (version, map, logs, fichiers clés)
4. La **génération automatique de sauvegardes intelligentes**
5. La **traçabilité complète** des actions IA dans `session_audit.log`
6. Une **API stable et extensible** pour les futures versions Cortex (v1.5 et +)

---

## 📡 Nouveaux Endpoints REST

### `/project/context`
Renvoie les métadonnées globales du projet.  
Exemple :
```json
{
  "api_version": "1.4.6",
  "timestamp": "2025-11-06T22:33:10Z",
  "files_detected": 162,
  "core_files": ["main.py", "endpoints_project.py"],
  "last_sync": "2025-11-06T22:31:45Z"
}
```

### `/project/memory`
Retourne le contenu actuel de la mémoire interne (`memory/memoire.json`).

### `/project/memory/update`
Met à jour la mémoire interne en fusionnant les clés existantes.  
Valide d’abord la cohérence avec `project_map.json` et effectue un backup automatique avant écriture.

### `/project/agent/sync`
Point de synchronisation entre agent GPT, pipeline CI/CD et MiniStudio.  
- Enregistre les événements (“deploy_success”, “auto_patch”, “backup_created”)
- Met à jour la mémoire et ajoute une trace dans `session_audit.log`

### `/project/logs/audit`
Retourne le contenu complet ou filtré de `memory/session_audit.log`.

### `/project/backup`
Crée une archive ZIP du projet complet dans `memory/`.  
Nom du fichier : `MiniStudio_backup_YYYYMMDD_HHMM.zip`

---

## 🧩 Structure d’arborescence cible

```
fastapi_app/
├── core/
│   ├── builder_core.py
│   ├── controller_collab.py
│   ├── check_docker_health.py
│   └── cortex_service.py     ← (nouveau module de liaison agent/IA)
├── cortex/
│   ├── cortex_engine.py      ← (préparation v1.5)
│   └── cortex_service.py
├── endpoints_project.py
└── main.py

memory/
├── memoire.json
├── project_map.json
├── session_audit.log
└── MiniStudio_backup_YYYYMMDD_HHMM.zip
```

---

## 🧠 Comportement attendu

1. Chaque appel à `/project/memory/update` ou `/project/agent/sync` :  
   - vérifie la cohérence de `project_map.json`,  
   - sauvegarde la version précédente dans `/memory/MiniStudio_backup_*.zip`,  
   - journalise l’événement dans `session_audit.log`.  

2. `/project/context` et `/project/map/update` doivent rester synchronisés.  
3. Le pipeline CI/CD doit appeler `/project/agent/sync` après chaque build réussi.

---

## 🔄 CI/CD Cognitive — Intégration GitHub Actions

### Exemple d’étapes ajoutées dans `.github/workflows/test_and_deploy.yml`

```yaml
- name: Update Project Map
  run: curl -X POST http://localhost:8000/project/map/update

- name: Synchronize Cortex Memory
  run: |
    echo "🧠 Synchronisation Cortex / CI-CD"
    curl -X POST http://localhost:8000/project/agent/sync       -H "Content-Type: application/json"       -d '{"ci_cd_event":"deploy_success","version":"v1.4.6","timestamp":"$(date --iso-8601=seconds)"}'

- name: Generate Backup
  run: curl -X POST http://localhost:8000/project/backup
```

💡 Ces appels assurent une **synchronisation cognitive automatique** entre les fichiers, la mémoire et les logs à chaque déploiement.

---

## 🔐 Sécurité et intégrité

- Validation stricte des payloads JSON (via `pydantic`)
- Taille maximale de requête : 2 Mo
- Horodatage ISO8601 sur chaque trace
- Sauvegarde avant écriture critique
- Journalisation systématique des événements IA / CI/CD
- Gestion de fallback automatique (`session_local_fallback.log`)

---

## 🧱 Étapes de développement

1. Implémenter les endpoints manquants dans `endpoints_project.py`
2. Ajouter `fastapi_app/core/cortex_service.py`
3. Mettre à jour le pipeline CI/CD (`test_and_deploy.yml`)
4. Tester en local via Swagger `/docs`
5. Vérifier `session_audit.log` après sync ou backup

---

## 🧩 Dépendances
- Python **3.11+**
- FastAPI / Uvicorn / Pydantic
- Docker / Docker Compose
- GitHub Actions
- JSON / zipfile / datetime

---

## 🧠 Préparation v1.5 (Cortex Engine)
Cette version 1.4.6 prépare la base du **Cortex Engine (v1.5)** :  
- Cohérence mémoire / logs / fichiers  
- API cognitive bidirectionnelle  
- Interopérabilité entre MiniStudio, GPT, CI/CD et Cortex Engine

---

## ✅ Livrables
- `endpoints_project.py` mis à jour  
- Nouveau `cortex_service.py` dans `core/`  
- Pipeline CI/CD cognitif fonctionnel  
- `memory/MiniStudio_backup_*.zip` généré automatiquement  
- `session_audit.log` complet  
- Documentation Swagger à jour  
- Présent cahier des charges signé : **v1.4.6 — Cortex Sync Layer (Édition Finale)**

---

## 📜 Auteur
Projet MiniStudioGPT — Architecture par Code GPT & Rachid
