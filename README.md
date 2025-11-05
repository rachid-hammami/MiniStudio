# 🧠 MiniStudioGPT v1.4.4-8 – FastAPI & React CI/CD

[![CI/CD Tolérant](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy.yml)
[![CI/CD Strict](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy_strict.yml/badge.svg)](https://github.com/rachid-hammami/MiniStudio/actions/workflows/test_and_deploy_strict.yml)

> 🔄 Pipeline CI/CD GitHub – Backend FastAPI + Frontend React  
> 🧱 v1.4.5 : validation stricte complète  
> 🚀 v1.4.4-8 : tolérante et continue

---

## 📘 Description

**MiniStudioGPT** est un environnement de développement automatisé construit sur **FastAPI** (backend) et **React (Vite)** (frontend).  
Son objectif est de centraliser les tests, le déploiement et la maintenance d’applications modulaires à travers un pipeline **CI/CD intelligent**.

---

## 🧩 Architecture du projet

```
MiniStudio/
├── fastapi_app/               # Application backend FastAPI
│   ├── core/                  # Cœur logique : contrôleurs, builders, orchestrateurs
│   ├── tests/                 # Tests unitaires Pytest
│   ├── utils/                 # Outils de logs, validation, etc.
│   └── main.py                # Point d’entrée FastAPI
│
├── frontend/                  # Interface utilisateur React (Vite + Tailwind)
│   ├── src/                   # Composants React
│   ├── public/                # Ressources statiques
│   └── package.json           # Dépendances frontend
│
├── memory/                    # Fichiers de mémoire et logs (audit, snapshot, map)
│
├── docs/                      # Cahiers des charges, rapports de sessions, etc.
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

## ⚙️ Fonctionnalités CI/CD

| Pipeline | Description | Statut |
|-----------|--------------|--------|
| 🚀 **Tolérant (v1.4.4-8)** | Tests automatiques backend/frontend, erreurs de style ignorées | 🟢 Stable |
| 🧱 **Strict (v1.4.5)** | Tests complets backend + frontend, erreurs bloquantes | 🟢 Opérationnel |
| 🔍 **Tests unitaires** | Pytest exécuté automatiquement à chaque commit | ✅ |
| 💅 **Style Black + Flake8** | Vérification de conformité PEP8 | ✅ |
| 🏗️ **Build React (Vite)** | Vérifie la validité du frontend | ✅ |

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

Les résultats sont automatiquement collectés dans les logs CI/CD et affichés dans l’onglet **Actions** du dépôt GitHub.

---

## 📄 Cahier des charges CI/CD (v1.4.4-8)

Voir :  
📘 `docs/Cahier_des_charges_MiniStudioGPT_v1.4.4-8_CI-CD.txt`

> Intègre les routes `/project/test/run`, `/project/deploy/run`, `/project/ping`  
> et prépare la mise à jour **v1.4.5 – Structure & Map Update**

---

## 🔮 Prochaine étape : MiniStudioGPT Cortex v1.5

- Introduction des routes `/project/structure` et `/project/map/update`
- Mécanisme de cartographie dynamique `project_map.json`
- Consolidation du système mémoire Cortex

---

🧠 _MiniStudioGPT – CI/CD fiable, automatisée et traçable._
