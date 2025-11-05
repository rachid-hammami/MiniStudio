
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import os

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = BASE_DIR / "fastapi_app"

@router.get("/control/ping")
async def control_ping():
    return {"status": "ok", "message": "Control panel actif."}

@router.get("/control/list")
async def control_list_files():
    files = [str(p.relative_to(FILES_DIR)) for p in FILES_DIR.glob("**/*") if p.is_file()]
    return {"status": "ok", "files": files}

@router.delete("/control/delete/{filename}")
async def control_delete_file(filename: str):
    target_file = FILES_DIR / filename
    if not target_file.exists():
        raise HTTPException(status_code=404, detail=f"Fichier {filename} introuvable.")
    try:
        os.remove(target_file)
        return {"status": "ok", "message": f"Fichier {filename} supprimé."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression : {e}" )
