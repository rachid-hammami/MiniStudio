# fastapi_app/project_write.py
# ==============================================================
# 📦 Module : Écriture et lecture complètes du projet MiniStudio
# ==============================================================
# Ce module fournit les routes /project/write, /project/read et
# /project/full-access, permettant à MiniStudioGPT ou à d'autres
# clients autorisés d’interagir directement avec les fichiers du projet.
# ==============================================================
# 🧩 Inclus dans main.py :
#     from fastapi_app import project_write
#     app.include_router(project_write.router)
# ==============================================================

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from pathlib import Path
import json

# === ⚙️ Configuration du routeur ===
router = APIRouter(
    prefix="/project",
    tags=["Gestion du projet MiniStudio"],
    responses={
        400: {"description": "Requête invalide"},
        404: {"description": "Fichier introuvable"},
        500: {"description": "Erreur interne du serveur"},
    },
)

# === 📁 Répertoire de base du projet ===
BASE_PATH = Path("/app").resolve()


# === 🧱 Modèle Pydantic ===
class ProjectWriteRequest(BaseModel):
    """
    Schéma de requête pour l’écriture complète d’un fichier dans le projet MiniStudio.
    - `filename`: chemin relatif du fichier (ex: "memory/memoire.json")
    - `content`: contenu à écrire (texte brut ou dictionnaire JSON)
    """
    filename: str
    content: dict | str


# === 🛡️ Fonction utilitaire de sécurité ===
def safe_path(filename: str) -> Path:
    """
    Génère un chemin sécurisé à l’intérieur de /app et empêche tout accès
    en dehors du projet (protection contre les traversées de répertoires).
    """
    path = Path(filename)
    if not path.is_absolute():
        path = BASE_PATH / path
    path = path.resolve()
    if not str(path).startswith(str(BASE_PATH)):
        raise HTTPException(status_code=400, detail="Chemin hors projet interdit.")
    return path


# === 🗂️ Route : /project/full-access ===
@router.get("/full-access")
async def full_access():
    """
    🔍 Liste tous les fichiers accessibles dans le projet MiniStudio.
    Retourne une arborescence complète pour audit, exploration ou sauvegarde.
    
    ⚠️ Utilisation réservée à l’administrateur ou MiniStudioGPT.
    """
    base = BASE_PATH
    files = [str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()]
    return {"status": "ok", "count": len(files), "files": files}


# === ✍️ Route : /project/write ===
@router.post("/write", response_model=dict)
async def full_write(request: ProjectWriteRequest):
    """
    ✍️ Écriture complète d’un fichier dans le projet MiniStudio.
    
    Permet à MiniStudioGPT ou à un service autorisé d’écrire ou créer des fichiers :
    - fichiers mémoire (`/memory/memoire.json`)
    - journaux de session (`/memory/session.log`)
    - rapports (`/reports/report_*.json`)
    
    ### Exemple de corps JSON attendu :
    ```json
    {
      "filename": "memory/memoire.json",
      "content": {
        "project": "MiniStudio",
        "assistant": "MiniStudioGPT"
      }
    }
    ```
    """
    try:
        target = safe_path(request.filename)
        target.parent.mkdir(parents=True, exist_ok=True)

        with open(target, "w", encoding="utf-8") as f:
            if isinstance(request.content, (dict, list)):
                json.dump(request.content, f, ensure_ascii=False, indent=2)
            else:
                f.write(str(request.content))

        return {"status": "ok", "path": str(target)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur écriture projet : {str(e)}")


# === 📖 Route : /project/read ===
@router.post("/read")
async def full_read(request: Request):
    """
    📖 Lecture complète d’un fichier du projet MiniStudio.
    
    Lit un fichier texte ou JSON depuis `/app`.
    Si le fichier est JSON, il est automatiquement désérialisé.
    
    ### Exemple de corps JSON attendu :
    ```json
    { "filename": "memory/memoire.json" }
    ```
    """
    body = await request.json()
    filename = body.get("filename")

    if not filename:
        raise HTTPException(status_code=400, detail="Champ 'filename' manquant.")

    path = safe_path(filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Fichier '{filename}' introuvable.")

    try:
        if path.suffix == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
        return {"content": path.read_text(encoding="utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lecture projet : {str(e)}")
