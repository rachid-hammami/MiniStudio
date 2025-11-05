# 🗒️ FastAPI Notes

## 📘 Description
FastAPI Notes est une mini-API REST développée avec **FastAPI**, intégrée au projet **MiniStudioGPT**, permettant de gérer une collection simple de notes stockées localement dans un fichier JSON.

Elle permet :
- d’ajouter une note (`POST /notes`)
- de lister toutes les notes (`GET /notes`)
- de supprimer une note (`DELETE /notes/{id}`)

---

## ⚙️ Installation

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/ton-projet/ministudio-fastapi-notes.git
cd ministudio-fastapi-notes
```

### 2️⃣ Créer et activer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 🚀 Exécution du serveur

### Lancer le serveur de développement
```bash
uvicorn fastapi_app.main:app --reload
```

### Accéder à l’API
- Interface Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Interface ReDoc : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Tests unitaires

Les tests automatiques couvrent à la fois :
- Les endpoints principaux de **MiniStudioGPT**,
- Les routes du module **FastAPI Notes**.

### Exécution des tests
```bash
pytest fastapi_app/test_app.py -v
```

---

## 📂 Structure du projet
```
fastapi_app/
├── main.py              # Routes principales + intégration Notes
├── models.py            # Modèle Pydantic Note
├── storage.py           # Gestion du fichier notes.json
├── notes.json           # Base de données locale
├── test_app.py          # Tests unifiés MiniStudio + Notes
└── README.md            # Documentation projet
```

---

## ✨ Auteur
Projet initial conçu par **PulsR / CodeGPT**, intégré par **MiniStudioGPT v2.1**.

---

## 📄 Licence
Ce projet est distribué sous licence MIT. Vous êtes libre de l’utiliser, le modifier et le redistribuer.
