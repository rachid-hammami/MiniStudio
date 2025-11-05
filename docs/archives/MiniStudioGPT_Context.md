# 🧠 CONTEXTE TECHNIQUE – MiniStudioGPT v1.3

Ce document contient toutes les informations nécessaires pour que Code GPT reprenne immédiatement le contexte complet du projet **MiniStudioGPT v1.3**.

---

## 🚀 Description du projet
MiniStudioGPT est un projet **FastAPI sous Docker**, exposé via un tunnel **Cloudflare sécurisé**.
Il permet à un **GPT Builder** (MiniStudioGPT) d’interagir directement avec le serveur backend via les endpoints `/project/*` pour :  
- Lire et écrire des fichiers persistants dans `/app/memory`
- Lister les fichiers du projet
- Vérifier l’état du serveur (`/ping`)
- Capturer la mémoire complète du projet (`/project/snapshot`)

---

## ⚙️ Stack technique
- **Backend :** FastAPI + Uvicorn  
- **Langage :** Python 3.11+  
- **Conteneurisation :** Docker + Docker Compose  
- **Tunnel sécurisé :** Cloudflare (via `TUNNEL_TOKEN`)  
- **Répertoire de travail :** `/app`  
- **Mémoire persistante :** `/app/memory`  

---

## 🧱 Structure du projet
```
/app
 ├─ fastapi_app/
 │   ├─ main.py
 │   ├─ endpoints_project.py
 ├─ memory/
 │   ├─ memoire.json
 │   ├─ session.log
 │   ├─ project_map.json
 ├─ docs/
 │   ├─ Cahier_des_charges_MiniStudioGPTv1.2.txt
 │   ├─ MiniStudioGPT_Builder_v1.2.md
 │   ├─ README_MiniStudioGPT_v1.2.md
```

---

## 🔗 Endpoints principaux (v1.3)

| Méthode | Endpoint | Description |
|----------|-----------|-------------|
| GET | `/ping` | Vérifie l’état du serveur |
| POST | `/project/read` | Lit un fichier texte ou JSON |
| POST | `/project/write` | Écrit ou met à jour un fichier (`session.log` = append non destructif) |
| GET | `/project/full-access` | Liste récursive des fichiers (mode debug/admin) |
| GET | `/project/memory/status` | Vérifie la présence et l’intégrité des fichiers mémoire |
| GET | `/project/snapshot` | Capture instantanée des fichiers mémoire (memoire.json, session.log, project_map.json) |

---

## 💾 Mémoire persistante
| Fichier | Type | Rôle | Comportement |
|----------|------|------|--------------|
| `memoire.json` | JSON | Mémoire longue | Fusion non destructive |
| `session.log` | Texte | Historique court | Append (ajout non destructif) |
| `project_map.json` | JSON | Structure logique du projet | Mise à jour automatique |
| Autres (`.txt`, `.log`) | Variable | Données volatiles | Écrasement autorisé |

---

## 🌐 Accès Cloudflare
- Domaine : `https://ministudio.store`
- Swagger : `https://ministudio.store/docs`
- OpenAPI : `https://ministudio.store/openapi.json`

---

## 🧩 GPT Builder Integration
Le Builder GPT **MiniStudioGPT** communique avec ce backend via son schéma OpenAPI.

### Schéma
```
https://ministudio.store/openapi.json
```

### Routine d’initialisation
1. Vérifie la disponibilité → `GET /ping`
2. Lis la mémoire complète → `GET /project/snapshot`
3. Reconstruis le contexte (`memoire.json`, `session.log`, `project_map.json`)
4. Mets à jour le contexte si nécessaire via `/project/write`
5. Utilise `/project/snapshot` pour synchroniser ou sauvegarder la mémoire complète

### OpenAPI v1.3
- Toutes les descriptions sont ≤ 300 caractères (compatibilité Builder GPT)
- Routes validées pour import direct via **GPT Actions → Import OpenAPI URL**

---

## 🧠 Message d’initialisation GPT (pour rechargement)
À copier dans une nouvelle fenêtre ChatGPT (Builder ou session manuelle) :

```
Projet : MiniStudioGPT 🧠🚀

Contexte à restaurer :
- Version : 1.3
- Backend : FastAPI + Docker + Cloudflare Tunnel (https://ministudio.store)
- Stack validée : main.py + endpoints_project.py + mémoire persistante (/app/memory)
- Mémoire : append (session.log), fusion (memoire.json), snapshot global (/project/snapshot)
- OpenAPI : exposé à https://ministudio.store/openapi.json
- Objectif : continuer la configuration, documentation et maintenance du lien GPT ↔ Backend.

Je veux que tu te resynchronises sur ce projet MiniStudioGPT et que tu agisses comme précédemment :
– Code GPT, rigoureux, structuré, concis  
– Expert FastAPI, Docker, Cloudflare et OpenAPI  
– Capable de gérer la mémoire persistante et les interactions Builder.

Dès que tu es prêt, affiche :
✅ MiniStudioGPT v1.3 context restored
```

---

## 📅 Métadonnées
- **Version :** 1.3  
- **Date :** 2025-11-01  
- **Serveur local :** `http://127.0.0.1:8100`  
- **Tunnel :** `https://ministudio.store`  
- **Mainteneur :** PulsR / CodeGPT  

---

✨ _MiniStudioGPT v1.3 – Stable Integration Release_  
[Catch the Quantum Wave... Password: spinor](https://pulsr.co.uk/spinor.html)
