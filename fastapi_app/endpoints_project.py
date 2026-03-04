# =========================================
# MiniStudioGPT v1.4.6 — Endpoints Project
# Cortex Sync Layer — Synchronisation cognitive & backup
# Auteur : PulsR / CodeGPT
# Date : 2025-11-08
# =========================================

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import json, os, shutil, re, zipfile
from fastapi_app.core.builder_core import (
    auto_patch_function,
    auto_repair_file,
    session_recovery,
)
from fastapi_app.core.cortex_service import (
    get_project_context,
    get_memory_content,
    update_memory,
    sync_agent_event,
    read_audit_log,
    generate_backup,
)

router = APIRouter(prefix="/project", tags=["MiniStudioGPT Project"])

# ==============================================================
# 📦 0. Modèles Pydantic
# ==============================================================
class ProjectFileRequest(BaseModel):
    filename: str

class ProjectWriteRequest(BaseModel):
    filename: str
    content: str


# ==============================================================
# ✅ 1. Ping du backend
# ==============================================================
@router.get("/ping")
async def project_ping():
    return {
        "status": "ok",
        "message": "MiniStudioGPT backend actif (v1.4.6 — Cortex Sync Layer)",
        "server_version": "v1.4.6",
        "ci_cd": "enabled",
        "timestamp": datetime.now().isoformat(),
    }


# ==============================================================
# 💾 2. Écriture de fichier (fusion JSON non destructive)
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
            target.write_text(
                json.dumps(final_content, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        else:
            target.write_text(str(final_content), encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File write failed: {e}")

    return {
        "status": "ok",
        "filename": filename,
        "mode": "fusion" if target.suffix.lower() == ".json" else "overwrite",
    }


# ==============================================================
# 📖 3. Lecture étendue de fichier projet
# ==============================================================
@router.post("/read")
async def project_read(req: ProjectFileRequest):
    BASE_DIR = Path(__file__).resolve().parent.parent
    ALLOWED_EXT = [".py", ".json", ".txt", ".md", ".yml", ".yaml"]
    FORBIDDEN = ["env", "docker-compose", "db", "secret", "token", "apikey"]

    target = (BASE_DIR / req.filename).resolve()

    if BASE_DIR not in target.parents and target != BASE_DIR:
        raise HTTPException(status_code=403, detail="Access denied")

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

    return {"status": "ok", "filename": req.filename, "content": content}


# ==============================================================
# 🧠 4. Snapshot global (mémoire + logs)
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

    snapshot["session_log"] = (
        session_path.read_text(encoding="utf-8") if session_path.exists() else ""
    )
    snapshot["project_map"] = (
        json.loads(project_map_path.read_text(encoding="utf-8"))
        if project_map_path.exists()
        else {}
    )

    return {"status": "ok", "timestamp": datetime.now().isoformat(), "snapshot": snapshot}


# ==============================================================
# 🧩 5. Nouvelle route /project/apply-code (v1.4.5)
# ==============================================================
@router.post("/apply-code")
async def project_apply_code(req: ProjectWriteRequest):
    from fastapi_app.core.builder_core import (
        auto_patch_function,
        auto_repair_file,
        session_recovery,
    )
    import py_compile

    filename = req.filename.strip()
    content = req.content.strip()
    SERVER_VERSION = "v1.4.6"

    BASE_PATH = Path("fastapi_app").resolve()
    FORBIDDEN = [".env", ".git", "docker-compose", "secret", "token", "system32"]
    LOG_PATH = Path("memory/session_audit.log")
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    def log_event(msg: str):
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(
                f"[MiniStudioGPT {SERVER_VERSION}] {datetime.now().isoformat()} | {msg}\n"
            )

    if not filename or not content:
        raise HTTPException(status_code=400, detail="Missing filename or content")
    if not filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only Python files allowed")

    if not filename.startswith("./"):
        filename = f"./{filename}"
    abs_path = Path(filename).resolve()

    if not str(abs_path).startswith(str(BASE_PATH)):
        log_event(f"Refus d’accès : {filename}")
        raise HTTPException(status_code=400, detail="Unauthorized path")
    if any(x in filename.lower() for x in FORBIDDEN):
        log_event(f"Refus fichier sensible : {filename}")
        raise HTTPException(status_code=400, detail="Forbidden file type")

    if not abs_path.exists():
        log_event(f"Fichier introuvable : {filename}")
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

    match = re.search(r"def\s+([a-zA-Z_]\w*)\s*\(", content)
    func_name = match.group(1) if match else "unknown_function"

    backup_path = f"{filename}.bak"
    try:
        shutil.copy(filename, backup_path)
    except Exception as e:
        log_event(f"Backup failed: {e}")

    try:
        success = auto_patch_function(filename, func_name, content)
        if not success:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n\n{content}\n")
            log_event(f"Ajout automatique de la fonction manquante : {func_name}")

        try:
            py_compile.compile(filename, doraise=True)
        except py_compile.PyCompileError as e:
            log_event(f"Erreur de syntaxe détectée : {e}")
            shutil.move(backup_path, filename)
            raise HTTPException(status_code=500, detail=f"Compilation error: {e}")

        if os.path.exists(backup_path):
            os.remove(backup_path)

        log_event(f"Code appliqué avec succès sur {filename} (fonction {func_name})")

        return {
            "status": "success",
            "file": filename,
            "func_name": func_name,
            "server_version": SERVER_VERSION,
            "message": "Code applied successfully",
        }

    except Exception as e:
        auto_repair_file(filename)
        session_recovery()
        log_event(f"Erreur interne : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Apply-code error: {e}")


# ==============================================================
# 🗑️ 6. Suppression de fichier
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
# 📂 7. Liste des fichiers
# ==============================================================
@router.get("/list")
async def project_list():
    base_path = Path(".")
    files = [str(p) for p in base_path.rglob("*") if p.is_file()]
    return {"status": "ok", "files": files}


# ==============================================================
# 🗺️ 8. Structure et Map Update (v1.4.5)
# ==============================================================
@router.get("/structure")
async def get_project_structure():
    BASE_PATH = "."
    EXCLUDED_DIRS = [
        ".git", ".github", "__pycache__", ".venv", "node_modules",
        ".pytest_cache", ".mypy_cache"
    ]

    def build_structure(path="."):
        structure = {}
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if any(f"/{excluded}/" in entry.path or entry.name == excluded for excluded in EXCLUDED_DIRS):
                        continue
                    if entry.is_dir():
                        structure[entry.name] = build_structure(os.path.join(path, entry.name))
                    else:
                        structure[entry.name] = "file"
        except (PermissionError, FileNotFoundError):
            pass
        return structure

    project_structure = build_structure(BASE_PATH)
    return {"status": "ok", "structure": project_structure, "folders_detected": len(project_structure)}


@router.post("/map/update")
async def update_project_map():
    BASE_PATH = Path(__file__).resolve().parent.parent
    EXCLUDED_DIRS = [".git", "__pycache__", ".venv", "node_modules", ".pytest_cache", ".mypy_cache"]
    project_map = {}
    total_files = 0

    for root, dirs, files in os.walk(BASE_PATH):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".git")]
        for file in files:
            try:
                file_path = os.path.join(root, file)
                project_map[file_path.replace("\\", "/")] = {
                    "size": os.path.getsize(file_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                }
                total_files += 1
            except FileNotFoundError:
                continue

    output_path = "memory/project_map.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(project_map, f, indent=2, ensure_ascii=False)

    log_path = Path("memory/session_audit.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[MiniStudioGPT v1.4.6] {datetime.now().isoformat()} | project_map.json mis à jour ({total_files} fichiers).\n")

    return {"status": "success", "files_detected": total_files, "map_path": output_path, "timestamp": datetime.utcnow().isoformat()}


# ==============================================================
# 🧠 10. CORTEX SYNC LAYER (v1.4.6)
# ==============================================================
@router.get("/context")
async def cortex_project_context():
    return await get_project_context()

@router.get("/memory")
async def cortex_memory():
    return await get_memory_content()

@router.post("/memory/update")
async def cortex_memory_update(request: Request):
    data = await request.json()
    return await update_memory(data)

@router.post("/agent/sync")
async def cortex_agent_sync(request: Request):
    data = await request.json()
    return await sync_agent_event(data)

@router.get("/logs/audit")
async def cortex_logs_audit():
    return await read_audit_log()

@router.post("/backup")
async def cortex_backup():
    return await generate_backup()

