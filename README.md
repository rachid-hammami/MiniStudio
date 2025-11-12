# 🧠 MiniStudioGPT v1.5 – Cortex (FastAPI & React – CI/CD & Mémoire adaptative)

[![CI/CD Tolérant](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy.yml)
[![CI/CD Strict](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy_strict.yml/badge.svg)](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy_strict.yml)

> 🔄 Pipeline CI/CD GitHub – Backend FastAPI + Frontend React  
> 🧱 v1.5 : ajout du module **Cortex** (mémoire adaptative + cartographie dynamique)  
> 🚀 CI/CD complet : tolérant et strict selon les branches

---

## 📘 Description

**MiniStudioGPT** est un environnement de développement automatisé et auto-hébergé construit sur **FastAPI** (backend) et **React (Vite)** (frontend).  
Il centralise les tests, le déploiement, la mémoire et la documentation des projets web grâce à un pipeline **CI/CD intelligent**.

La version **v1.5 – Cortex** introduit la **mémoire adaptative**, un système capable de sauvegarder et d’analyser automatiquement la structure et le contexte des projets, pour une persistance continue entre les sessions.

---

## 🧩 Architecture du projet

```
MiniStudio/
├── fastapi_app/
│   ├── core/                  # Cœur logique : contrôleurs, builders, orchestrateurs
│   ├── cortex/                # Nouveau module de mémoire adaptative (v1.5)
│   ├── tests/                 # Tests unitaires Pytest
│   ├── utils/                 # Logs, validation, mapping dynamique
│   └── main.py                # Point d’entrée FastAPI
│
├── frontend/                  # Interface utilisateur React (Vite + Tailwind)
│   ├── src/                   # Composants React
│   ├── public/                # Ressources statiques
│   └── package.json           # Dépendances frontend
│
├── memory/                    # Fichiers mémoire : memoire.json, session.log, project_map.json
│
├── docs/                      # Cahiers des charges, changelogs, rapports de sessions
│
├── .github/workflows/         # Pipelines CI/CD GitHub Actions
│   ├── test_and_deploy.yml           # CI/CD tolérant
│   └── test_and_deploy_strict.yml    # CI/CD strict
│
├── pytest.ini                 # Configuration des tests
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier
```

---

## ⚙️ Fonctionnalités principales

| Module | Description | Statut |
|--------|--------------|--------|
| 🧠 **Cortex v1.5** | Mémoire adaptative, analyse du contexte, cartographie automatique des projets | 🟢 Stable |
| 🚀 **CI/CD** | Pipelines tolérant et strict (GitHub Actions) | ✅ |
| 🧱 **FastAPI** | API backend orchestrant les projets et la persistance | ✅ |
| 💅 **React (Vite)** | Frontend dynamique (en développement) | 🚧 |
| 💾 **Persistence** | Sauvegarde continue `memoire.json`, `session.log`, `project_map.json` | ✅ |
| 🔐 **Cloudflare Tunnel** | Accès sécurisé à l’environnement local | ✅ |

---

## 🚀 Installation locale

```bash
git clone https://github.com/rachid-hammami/MiniStudio.git
cd MiniStudio

# Backend
pip install -r requirements.txt
uvicorn fastapi_app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## 🧪 Tests unitaires

```bash
pytest -v
```

Les résultats sont collectés automatiquement dans les logs CI/CD et visibles dans l’onglet **Actions** du dépôt GitHub.

---

## 📄 Cahier des charges v1.5 – Cortex

Voir :  
📘 `docs/Cahier_des_charges_MiniStudioGPT_v1.5_Cortex.txt`

> Ajoute les routes `/project/structure`, `/project/map/update`, et la gestion dynamique du fichier `project_map.json`.  
> Introduit le module **CortexMemory** pour la persistance et l’analyse contextuelle.

---

## 🧭 Roadmap

| Version | Statut | Description |
|----------|--------|--------------|
| 🧠 **v1.5 – Cortex** | 🟢 Terminé | Mémoire adaptative, cartographie dynamique, refonte structure backend |
| 🚧 **v1.6 – Interface** | 🔜 En cours | Interface graphique complète (React + FastAPI) + automatisation visuelle des projets |
| 📚 **v1.7 – Automations** | 🕓 Prévu | Module d’automatisation de tâches locales et intégration d’API externes |

---

## 📜 Historique des versions

| Version | Date | Description |
|----------|------|--------------|
| 🧠 **v1.5** | Novembre 2025 | Module Cortex, cartographie dynamique, mémoire adaptative complète |
| 🧱 **v1.4.5** | Novembre 2025 | CI/CD strict, vérifications Black & Flake8 bloquantes, build React intégré |
| 🚀 **v1.4.4-8** | Octobre 2025 | CI/CD tolérant, première intégration GitHub Actions |
| 🧠 **v1.4.3** | Septembre 2025 | Audit de session et logs mémoire |
| ⚙️ **v1.4.2** | Août 2025 | Refonte AI Core et analyseur amélioré |
| 🧩 **v1.4.1** | Juillet 2025 | Migration complète vers FastAPI |
| 🚧 **v1.4.0** | Juin 2025 | Initialisation du projet MiniStudioGPT |

---

_Projet maintenu par **Rachid Hammami** – CI/CD & Mémoire adaptative by MiniStudioGPT Cortex._
