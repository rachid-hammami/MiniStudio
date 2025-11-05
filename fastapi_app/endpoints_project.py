# =========================================
# MiniStudioGPT v1.4.3 â€” Endpoints Project
# Lecture Ã©tendue + Apply-Code intÃ©grÃ©
# Auteur : PulsR / CodeGPT
# Date : 2025-10-31
# =========================================

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import json, os, shutil, re
from fastapi_app.core.builder_core import auto_patch_function, auto_repair_file, session_recovery

router = APIRouter(prefix="/project", tags=["MiniStudioGPT Project"])

# ==============================================================
# ðŸ“¦ 0. ModÃ¨les Pydantic
# ==============================================================
class ProjectFileRequest(BaseModel):
    filename: str

class ProjectWriteRequest(BaseModel):
    filename: str
    content: str


# ==============================================================
# âœ… 1. Ping du backend
# ==============================================================
@app.get("/project/ping")
async def ping():
    return {
        "status": "ok",
        "message": "MiniStudioGPT backend actif (v1.4.4-8)",
        "server_version": "v1.4.4-8",
        "ci_cd": "enabled"
    }



# ==============================================================
# ðŸ’¾ 2. Ã‰criture de fichier (fusion JSON non destructive)
# ==============================================================
@router.post("/write")
async def project_write(request: Request):
    payload = await request.json()
    filename = payload.get("filename")
    content = payload.get("content")

    if not filename or content is None:
        raise HTTPException(status_code=400, detail="Missing filename or content")

    target = Path(filename)
    target.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(content, str):
        stripped = content.strip()
        if stripped.startswith(("{", "[")):
            try:
                content = json.loads(content)
            except Exception:
                content = {"raw_content": content}

    if target.suffix.lower() == ".json" and target.exists():
        try:
            existing_content = json.loads(target.read_text(encoding="utf-8"))
        except Exception:
            existing_content = {}
        if isinstance(existing_content, dict) and isinstance(content, dict):
            for key, value in content.items():
                if (
                    key in existing_content
                    and isinstance(existing_content[key], list)
                    and isinstance(value, list)
                ):
                    existing_content[key] = list(set(existing_content[key] + value))
                else:
                    existing_content[key] = value
            final_content = existing_content
        else:
            final_content = content
    else:
        final_content = content

    try:
        if target.suffix.lower() == ".log":
            with open(target, "a", encoding="utf-8") as f:
                f.write(str(final_content) + "\n")
        elif isinstance(final_content, (dict, list)):
            target.write_text(json.dumps(final_content, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            target.write_text(str(final_content), encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File write failed: {e}")

    return {
        "status": "ok",
        "filename": filename,
        "mode": "fusion" if target.suffix.lower() == ".json" else "overwrite"
    }


# ==============================================================
# ðŸ“– 3. Lecture Ã©tendue de fichier projet
# ==============================================================
@router.post("/read")
async def project_read(req: ProjectFileRequest):
    BASE_DIR = Path(__file__).resolve().parent.parent
    ALLOWED_EXT = [".py", ".json", ".txt", ".md", ".yml", ".yaml"]
    FORBIDDEN = ["env", "docker-compose", "db", "secret", "token", "apikey"]

    target = (BASE_DIR / req.filename).resolve()

    # VÃ©rification de sÃ©curitÃ© : chemin autorisÃ©
    if BASE_DIR not in target.parents and target != BASE_DIR:
        raise HTTPException(status_code=403, detail="Access denied")

    # Fichiers sensibles interdits
    if any(word in target.name.lower() for word in FORBIDDEN):
        raise HTTPException(status_code=403, detail="Forbidden file")

    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if target.suffix.lower() not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="File type not allowed")

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Read failed: {e}")

    return {
        "status": "ok",
        "filename": req.filename,
        "content": content,
    }


# ==============================================================
# ðŸ§  4. Snapshot global (mÃ©moire + logs)
# ==============================================================
@router.get("/snapshot")
async def project_snapshot():
    memory_path = Path("memory")
    memoire_path = memory_path / "memoire.json"
    session_path = memory_path / "session.log"
    project_map_path = memory_path / "project_map.json"

    snapshot = {}
    if memoire_path.exists():
        try:
            snapshot["memoire"] = json.loads(memoire_path.read_text(encoding="utf-8"))
        except Exception:
            snapshot["memoire"] = {}
    else:
        snapshot["memoire"] = {}

    snapshot["session_log"] = session_path.read_text(encoding="utf-8") if session_path.exists() else ""
    snapshot["project_map"] = (
        json.loads(project_map_path.read_text(encoding="utf-8")) if project_map_path.exists() else {}
    )

    return {"status": "ok", "timestamp": datetime.now().isoformat(), "snapshot": snapshot}


# ==============================================================
# ðŸ§© 5. Nouvelle route /project/apply-code
# ==============================================================
# ==============================================================
# ðŸ§© 5. Nouvelle route /project/apply-code (v1.4.4 corrigÃ©e)
# ==============================================================
@router.post("/apply-code")
async def project_apply_code(req: ProjectWriteRequest):
    """
    Applique ou crÃ©e une fonction Python dans un fichier.
    CompatibilitÃ© MiniStudioGPT v1.4.4
    """
    from builder_core import auto_patch_function, auto_repair_file, session_recovery
    import py_compile

    filename = req.filename.strip()
    content = req.content.strip()
    SERVER_VERSION = "v1.4.4"

    BASE_PATH = Path("fastapi_app").resolve()
    FORBIDDEN = [".env", ".git", "docker-compose", "secret", "token", "system32"]
    LOG_PATH = Path("memory/session_audit.log")
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    def log_event(msg: str):
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[MiniStudioGPT {SERVER_VERSION}] {datetime.now().isoformat()} | {msg}\n")

    # VÃ©rifications prÃ©liminaires
    if not filename or not content:
        raise HTTPException(status_code=400, detail="Missing filename or content")
    if not filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only Python files allowed")

    # Normalisation du chemin
    if not filename.startswith("./"):
        filename = f"./{filename}"
    abs_path = Path(filename).resolve()

    # VÃ©rif sÃ©curitÃ©
    if not str(abs_path).startswith(str(BASE_PATH)):
        log_event(f"Refus dâ€™accÃ¨s : {filename}")
        raise HTTPException(status_code=400, detail="Unauthorized path")
    if any(x in filename.lower() for x in FORBIDDEN):
        log_event(f"Refus fichier sensible : {filename}")
        raise HTTPException(status_code=400, detail="Forbidden file type")

    if not abs_path.exists():
        log_event(f"Fichier introuvable : {filename}")
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

    # Extraction automatique du nom de fonction
    match = re.search(r"def\s+([a-zA-Z_]\w*)\s*\(", content)
    func_name = match.group(1) if match else "unknown_function"

    # Sauvegarde avant patch
    backup_path = f"{filename}.bak"
    try:
        shutil.copy(filename, backup_path)
    except Exception as e:
        log_event(f"Backup failed: {e}")

    try:
        # Tente dâ€™appliquer le patch via builder_core
        success = auto_patch_function(filename, func_name, content)
        if not success:
            # Si Ã©chec, on tente la crÃ©ation manuelle
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n\n{content}\n")
            log_event(f"Ajout automatique de la fonction manquante : {func_name}")

        # VÃ©rification de la validitÃ© syntaxique
        try:
            py_compile.compile(filename, doraise=True)
        except py_compile.PyCompileError as e:
            log_event(f"Erreur de syntaxe dÃ©tectÃ©e : {e}")
            shutil.move(backup_path, filename)
            raise HTTPException(status_code=500, detail=f"Compilation error: {e}")

        # Nettoyage du backup si tout est bon
        if os.path.exists(backup_path):
            os.remove(backup_path)

        log_event(f"Code appliquÃ© avec succÃ¨s sur {filename} (fonction {func_name})")

        return {
            "status": "success",
            "file": filename,
            "func_name": func_name,
            "server_version": SERVER_VERSION,
            "message": "Code applied successfully"
        }

    except Exception as e:
        auto_repair_file(filename)
        session_recovery()
        log_event(f"Erreur interne : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Apply-code error: {e}")


# ==============================================================
# ðŸ§¹ 6. Suppression de fichier
# ==============================================================
@router.post("/delete")
async def project_delete(request: Request):
    payload = await request.json()
    filename = payload.get("filename")
    if not filename:
        raise HTTPException(status_code=400, detail="Missing filename")
    target = Path(filename)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    target.unlink()
    return {"status": "ok", "deleted": filename}


# ==============================================================
# ðŸ“‚ 7. Liste des fichiers
# ==============================================================
@router.get("/list")
async def project_list():
    base_path = Path(".")
    files = [str(p) for p in base_path.rglob("*") if p.is_file()]
    return {"status": "ok", "files": files}
