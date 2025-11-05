from fastapi import APIRouter, HTTPException, Query
from pathlib import Path

router = APIRouter(
    prefix="/api/files",
    tags=["Explorateur de fichiers"]
)

# Racine du projet (dossier /app dans ton conteneur)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dossiers à ignorer pour éviter les lenteurs et le bruit
EXCLUDED_DIRS = {
    ".venv", "venv", "__pycache__", ".pytest_cache", ".git",
    "site-packages", "usr", "lib", "bin", "tests", "pittestcache"
}


@router.get("/")
def list_files(
    base: str = Query(default="", description="Sous-dossier à explorer (ex: 'memory' ou 'fastapi_app')"),
    max_depth: int = Query(default=4, ge=1, le=10, description="Profondeur maximale de recherche (par défaut 4)")
):
    """
    🔍 Liste récursive des fichiers et dossiers de MiniStudio,
    en excluant automatiquement les dossiers inutiles (.venv, __pycache__, etc.).
    """
    base_path = PROJECT_ROOT / base

    if not base_path.exists():
        raise HTTPException(status_code=404, detail=f"Répertoire introuvable : {base_path}")

    files = []
    for p in base_path.rglob("*"):
        # Calcul de profondeur relative
        depth = len(p.relative_to(base_path).parts)
        if depth > max_depth:
            continue

        # Exclure les dossiers non désirés
        if any(part in EXCLUDED_DIRS for part in p.parts):
            continue

        files.append({
            "name": p.name,
            "path": str(p.relative_to(PROJECT_ROOT)),
            "is_dir": p.is_dir()
        })

    return {
        "base": str(base_path),
        "count": len(files),
        "files": files
    }
