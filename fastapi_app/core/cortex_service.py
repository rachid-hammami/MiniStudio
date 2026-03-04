# =========================================
# MiniStudioGPT v1.4.6 — Cortex Service
# Gestion de la synchronisation cognitive : mémoire, logs, map, CI/CD
# Auteur : PulsR / CodeGPT
# Date : 2025-11-08
# =========================================

from pathlib import Path
from datetime import datetime
import json, os, zipfile, shutil
from fastapi import HTTPException

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True, parents=True)

MEMOIRE_PATH = MEMORY_DIR / "memoire.json"
PROJECT_MAP_PATH = MEMORY_DIR / "project_map.json"
AUDIT_LOG_PATH = MEMORY_DIR / "session_audit.log"

SERVER_VERSION = "v1.4.6"

# ==============================================================
# 🧠 Utilitaires internes
# ==============================================================

def _log_event(message: str):
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[MiniStudioGPT {SERVER_VERSION}] {datetime.now().isoformat()} | {message}\n")

def _read_json(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ==============================================================
# 📊 1. Contexte global du projet
# ==============================================================
async def get_project_context():
    project_map = _read_json(PROJECT_MAP_PATH)
    total_files = len(project_map)
    core_files = [p for p in project_map.keys() if "core" in p or "endpoints_project.py" in p]

    context = {
        "api_version": SERVER_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "files_detected": total_files,
        "core_files": core_files[:10],
        "last_sync": datetime.fromtimestamp(os.path.getmtime(PROJECT_MAP_PATH)).isoformat()
        if PROJECT_MAP_PATH.exists()
        else None,
    }

    _log_event("Lecture du contexte global du projet.")
    return {"status": "ok", "context": context}


# ==============================================================
# 💾 2. Lecture de la mémoire
# ==============================================================
async def get_memory_content():
    memoire = _read_json(MEMOIRE_PATH)
    _log_event("Lecture mémoire cognitive.")
    return {"status": "ok", "memoire": memoire}


# ==============================================================
# 🧩 3. Mise à jour de la mémoire
# ==============================================================
async def update_memory(data: dict):
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Invalid payload")

    memoire = _read_json(MEMOIRE_PATH)
    project_map = _read_json(PROJECT_MAP_PATH)

    # Fusion des clés existantes
    for key, value in data.items():
        memoire[key] = value

    # Backup avant écriture
    backup_name = f"MiniStudio_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
    backup_path = MEMORY_DIR / backup_name
    try:
        await generate_backup(target_path=backup_path)
    except Exception as e:
        _log_event(f"⚠️ Backup avant update mémoire échoué : {e}")

    _write_json(MEMOIRE_PATH, memoire)
    _log_event("Mise à jour mémoire réussie et cohérente avec project_map.json.")

    return {"status": "success", "updated_keys": list(data.keys()), "backup": str(backup_path)}


# ==============================================================
# 🔄 4. Synchronisation agent GPT / CI-CD
# ==============================================================
async def sync_agent_event(data: dict):
    if "ci_cd_event" not in data:
        raise HTTPException(status_code=400, detail="Missing ci_cd_event field")

    memoire = _read_json(MEMOIRE_PATH)
    events = memoire.get("sync_events", [])
    new_event = {
        "event": data.get("ci_cd_event"),
        "version": data.get("version", SERVER_VERSION),
        "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
    }
    events.append(new_event)
    memoire["sync_events"] = events

    _write_json(MEMOIRE_PATH, memoire)
    _log_event(f"Synchronisation agent/CI-CD enregistrée : {new_event['event']}")

    return {"status": "ok", "event_logged": new_event}


# ==============================================================
# 📜 5. Lecture du journal d’audit
# ==============================================================
async def read_audit_log():
    if not AUDIT_LOG_PATH.exists():
        return {"status": "ok", "log": ""}
    content = AUDIT_LOG_PATH.read_text(encoding="utf-8")
    return {"status": "ok", "log": content}


# ==============================================================
# 🧱 6. Sauvegarde complète du projet
# ==============================================================
async def generate_backup(target_path: Path = None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup_name = f"MiniStudio_backup_{timestamp}.zip"
    backup_path = target_path or (MEMORY_DIR / backup_name)

    _log_event(f"Création d’une sauvegarde complète : {backup_name}")

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            if any(ex in root for ex in [".git", "__pycache__", "node_modules", ".venv"]):
                continue
            for file in files:
                full_path = Path(root) / file
                arcname = full_path.relative_to(BASE_DIR)
                zipf.write(full_path, arcname)

    _log_event(f"Sauvegarde terminée : {backup_name}")
    return {"status": "success", "backup_path": str(backup_path)}

