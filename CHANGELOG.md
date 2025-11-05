# 🧱 MiniStudioGPT – CHANGELOG (v1.4.0 → v1.4.5)

## 🧩 v1.4.5 – CI/CD Strict & Cortex Prep (Novembre 2025)
**Statut :** 🚀 Stable  
**Focus :** Validation stricte CI/CD, consolidation backend et mapping intelligent.

### 🔧 Changements majeurs
- Ajout du pipeline **CI/CD strict (`test_and_deploy_strict.yml`)**.  
- Vérifications bloquantes : **Black, Flake8, Pytest**.  
- Intégration du build **React (Vite)** dans le pipeline.  
- Correction des imports et noms ambigus (E741, F401, etc.).  
- Préparation du système **Cortex** : ajout des routes `/project/structure` et `/project/map/update`.  
- Mécanisme de mise à jour dynamique pour `memory/project_map.json`.

### 🧠 Objectifs
- Centralisation des logs CI/CD backend/frontend.
- Structure d’orchestration renforcée (FastAPI Orchestrator + Control Panel).
- Préparation à la version 1.5 “Cortex Intelligence”.

---

## 🚀 v1.4.4-8 – CI/CD Tolérant (Octobre 2025)
**Statut :** 🟢 Stable  
**Focus :** Automatisation complète avec pipeline tolérant.

### ✨ Nouvelles fonctionnalités
- Ajout du fichier **`.github/workflows/test_and_deploy.yml`**.  
- Déploiement automatisé des tests FastAPI et React.  
- Vérification Black et Flake8 non bloquante.  
- Première synchronisation GitHub CI/CD réussie.

### ⚙️ Améliorations
- Réécriture du README global avec badges CI/CD.  
- Réorganisation du dossier `.github/workflows/`.  
- Nettoyage et formatage automatique avec Black.  
- Introduction du test pipeline React frontend.

---

## 🧠 v1.4.3 – Session Engine & Audit Logs
**Focus :** Traçabilité et résilience du système mémoire.

### 🔍 Changements
- Ajout de `memory/session_audit.log` et `session_local_fallback.log`.  
- Meilleure gestion des erreurs dans `controller_collab.py`.  
- Orchestrateur refactorisé pour meilleure stabilité.  

---

## 🧩 v1.4.2 – AI Core Refinement
**Focus :** Intelligence d’analyse et synchronisation.

### 🔬 Changements
- Amélioration de `ai_engine.py` et `analyzer_engine.py`.  
- Refonte du `builder_core.py` pour modularité accrue.  
- Introduction de `control_panel.py` (premier mode multi-agent).  

---

## 🧱 v1.4.1 – FastAPI Integration & Modular Core
**Focus :** Fusion backend unifié.

### ⚙️ Détails
- Migration complète vers **FastAPI**.  
- Intégration du système de stockage `storage.py`.  
- Introduction de la structure `core/`, `utils/`, `tests/`.  

---

## 🚧 v1.4.0 – Refactor global et structuration initiale
**Focus :** Mise en place de la base projet.

### 🏗️ Changements clés
- Initialisation du projet **MiniStudioGPT**.  
- Structuration des modules `docs/`, `fastapi_app/`, `frontend/`.  
- Ajout des premiers tests unitaires et configuration `pytest.ini`.  
- Intégration du premier pipeline de test local.  

---

🧩 _MiniStudioGPT continue d’évoluer vers Cortex v1.5 : un environnement CI/CD auto-adaptatif et modulaire._
