
# 🧭 Guide Interne MiniStudio — Exposition, Lancement et Accès

## 📦 1. Structure générale du projet
MiniStudio est une application **FastAPI** exécutée dans un conteneur **Docker**.  
Elle peut être **exposée sur Internet via Ngrok**, pour des tests ou démonstrations distantes.

Les principaux fichiers liés à cette configuration sont :
```
/MiniStudio
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── ngrok_ministudio.yml
└── app/ (ou fastapi_app/)
    └── main.py  ← Point d’entrée FastAPI
```

---

## ⚙️ 2. Lancement du serveur local

### A. Construire l’image Docker
```powershell
docker-compose build
```

### B. Démarrer le conteneur MiniStudio
```powershell
docker-compose up
```

🧠 Ce conteneur démarre un serveur Uvicorn accessible sur :
```
http://localhost:8888
```

Si tu vois dans le terminal :
```
Uvicorn running on http://0.0.0.0:8888
```
➡️ Le serveur FastAPI est bien lancé.

---

## 🌍 3. Exposition du projet avec Ngrok

### A. Démarrage du tunnel direct
Pour exposer MiniStudio à Internet :
```powershell
ngrok http 8888
```

Ngrok te retournera une ligne :
```
Forwarding  https://xxxxx.ngrok-free.dev -> http://localhost:8888
```

➡️ C’est ton lien public.  
Tu peux tester ton API via :
```
https://xxxxx.ngrok-free.dev/docs
```

### B. Interface de suivi (très utile)
Ngrok fournit aussi une interface locale :
```
http://127.0.0.1:4040
```
Tu peux y voir toutes les requêtes reçues et les réponses de ton API.

---

## 🔒 4. Accès et routes principales

| Type d’accès | URL |
|:--|:--|
| Local | `http://localhost:8888/docs` |
| Public (Ngrok) | `https://xxxxx.ngrok-free.dev/docs` |
| Page d’accueil (si ajoutée) | `https://xxxxx.ngrok-free.dev/` |

⚠️ Si tu ouvres l’URL sans `/docs`, tu verras probablement :  
```
{"detail": "Not Found"}
```
→ c’est normal, FastAPI n’a pas de route `/` par défaut.

---

## 🧩 5. (Optionnel) Ajouter une page d’accueil
Pour une meilleure présentation publique, tu peux ajouter ce code à ton `main.py` :

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return '''
    <h2>🚀 MiniStudio est en ligne</h2>
    <p>Documentation disponible ici : <a href="/docs">/docs</a></p>
    '''
```

---

## 🚀 6. Script de lancement tout-en-un (facultatif)
Tu peux créer un fichier `start_ministudio.bat` à la racine :

```bat
@echo off
cd C:\Users\Dell\Documents\Developpement\GitHub\MiniStudio
start cmd /k "docker-compose up"
timeout /t 10
start cmd /k "ngrok http 8888"
```

🧩 Ce script :
- démarre ton conteneur MiniStudio,
- attend 10 secondes,
- ouvre le tunnel Ngrok automatiquement.

---

## ✅ 7. Résumé des commandes essentielles

| Action | Commande |
|:--|:--|
| Construire le conteneur | `docker-compose build` |
| Lancer MiniStudio | `docker-compose up` |
| Vérifier l’état | `docker ps` |
| Lancer Ngrok | `ngrok http 8888` |
| Accéder à l’API | `/docs` |
| Suivre les requêtes Ngrok | `http://127.0.0.1:4040` |

---

## 🧠 8. Points d’attention
- L’URL Ngrok change à chaque redémarrage (sauf compte payant ou domaine personnalisé).  
- Ne ferme pas la fenêtre Ngrok tant que tu veux que ton API reste accessible.  
- Si tu vois `"Not Found"`, pense à tester `/docs`.  
- Si tu modifies le code de ton app, pense à reconstruire ton image Docker :
  ```bash
  docker-compose build && docker-compose up
  ```

---

### ✅ En résumé
- Docker = serveur local  
- Ngrok = exposition publique  
- `/docs` = interface API principale  
- Tout fonctionne dès que tu vois :
  ```
  Forwarding  https://xxxxx.ngrok-free.dev -> http://localhost:8888
  ```
