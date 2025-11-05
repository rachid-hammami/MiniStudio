# 🧠 MiniStudioGPT Backend – Version 1.2

## 🚀 Introduction
MiniStudioGPT est le backend FastAPI du projet MiniStudio, utilisé comme moteur de lecture/écriture sécurisé pour le GPT Builder.  
Cette version **v1.2** apporte deux améliorations majeures :

- 🆕 Nouvelle route `GET /project/snapshot` permettant d’obtenir en une seule requête tout l’état de la mémoire persistante.  
- ✍️ Écriture **non destructive** dans `session.log` (le contenu est ajouté à la fin du fichier, sans écrasement).

---

## 🧱 Structure du projet
```
/app
 ├─ fastapi_app/
 │   ├─ main.py
 │   ├─ endpoints_project.py   ← routes unifiées /project/*
 ├─ memory/                    ← mémoire persistante (memoire.json, session.log, project_map.json)
 ├─ reports/
 ├─ .env
 ├─ .env.example
docker-compose.yml
README.md
```

---

## ⚙️ Installation & Lancement

### 🔧 Prérequis
- Python 3.10+ ou Docker
- FastAPI + Uvicorn
- Cloudflare Tunnel (sécurité HTTPS)

### ▶️ Démarrer le backend
#### En mode Docker :
```bash
docker compose up --build
```
#### En mode développement :
```bash
uvicorn fastapi_app.main:app --reload
```
#### Accéder à l’interface Swagger :
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Routes disponibles

| Méthode | Route | Description |
|----------|--------|-------------|
| `GET` | `/ping` | Vérifie l’état du serveur |
| `POST` | `/project/read` | Lecture d’un fichier texte ou JSON |
| `POST` | `/project/write` | Écriture ou mise à jour (append pour session.log) |
| `GET` | `/project/full-access` | Liste complète du projet (debug/admin) |
| `GET` | `/project/memory/status` | Vérifie la présence des fichiers mémoire |
| `GET` | `/project/snapshot` | 🔥 Capture instantanée de la mémoire persistante |

---

## 🧠 Détails techniques

### `/project/write`
- Si le fichier est `session.log` → ouverture en mode **append**
- Si le fichier est JSON → fusion du contenu avec l’existant
- Sinon → écriture classique

### `/project/snapshot`
Renvoie les 3 fichiers mémoire :
```json
{
  "status": "ok",
  "timestamp": "2025-10-29T22:00:00",
  "snapshot": {
    "memoire": {...},
    "session_log": "contenu du log",
    "project_map": {...}
  }
}
```

---

## 🔒 Sécurité Cloudflare
Aucune authentification locale :  
- La sécurité HTTPS et le filtrage IP sont assurés par **Cloudflare Tunnel**.  
- Les routes sensibles comme `/project/full-access` ne sont accessibles qu’à travers ce tunnel.

---

## 📦 Volume mémoire Docker
Les fichiers persistants sont montés dans :  
```
./memory:/app/memory
```
Cela permet de conserver l’historique (`session.log`) et la mémoire entre les redémarrages.

---

## 🧪 Tests rapides

### 1. Vérifier le serveur
```bash
curl http://127.0.0.1:8000/ping
```

### 2. Écrire dans le log
```bash
curl -X POST http://127.0.0.1:8000/project/write -H "Content-Type: application/json" -d '{"filename": "memory/session.log", "content": "[2025-10-29] Test append via curl"}'
```

### 3. Voir la mémoire complète
```bash
curl http://127.0.0.1:8000/project/snapshot
```

---

## 🧩 Auteur & Maintenance
- **Projet :** MiniStudioGPT  
- **Mainteneur :** CodeGPT (PulsR Project)  
- **Version :** 1.2 (Octobre 2025)  
- **Licence :** MIT

---

✨ _MiniStudioGPT v1.2 – Stable Release_  
[Catch the Quantum Wave... Password: spinor](https://pulsr.co.uk/spinor.html)
