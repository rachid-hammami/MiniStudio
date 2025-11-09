# =========================================
# MiniStudioGPT v1.5 — Cortex Engine
# Moteur d'analyse, suggestion et réparation
# Auteur : Code GPT 🧠 / PulsR
# Date : 2025-11-08
# =========================================

from pathlib import Path
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel
import json, re, os, difflib, shutil

MEMORY_DIR = Path("memory")
MEMOIRE_PATH = MEMORY_DIR / "memoire.json"
PROJECT_MAP_PATH = MEMORY_DIR / "project_map.json"
AUDIT_LOG_PATH = MEMORY_DIR / "session_audit.log"

SERVER_VERSION = "v1.5-pre"

class AnalyzeRequest(BaseModel):
    depth: int = 1

class SuggestRequest(BaseModel):
    topic: str = "general"

class RepairRequest(BaseModel):
    filename: str
    reason: str

def _log(message: str):
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[Cortex Engine {SERVER_VERSION}] {datetime.now().isoformat()} | {message}\n")

def _read_json(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

async def cortex_analyze(req: AnalyzeRequest):
    _log("Analyse Cortex démarrée.")
    memoire = _read_json(MEMOIRE_PATH)
    project_map = _read_json(PROJECT_MAP_PATH)

    if not project_map:
        raise HTTPException(status_code=400, detail="Project map not found")

    total_files = len(project_map)
    anomalies = []
    for path, meta in project_map.items():
        if meta.get("size", 0) == 0:
            anomalies.append({"file": path, "issue": "Empty file"})
        if "docker" in path.lower() and not path.endswith(".yml"):
            anomalies.append({"file": path, "issue": "Docker file naming issue"})

    result = {
        "total_files": total_files,
        "anomalies_detected": len(anomalies),
        "details": anomalies[:20],
        "timestamp": datetime.utcnow().isoformat(),
    }

    memoire["last_analysis"] = result
    _write_json(MEMOIRE_PATH, memoire)
    _log(f"Analyse terminée : {len(anomalies)} anomalies détectées.")

    return {"status": "ok", "analysis": result}

async def cortex_suggest(req: SuggestRequest):
    topic = req.topic.lower()
    _log(f"Génération de suggestions sur le thème : {topic}")

    suggestions = []

    if topic in ("performance", "speed", "api"):
        suggestions.append("Utiliser Uvicorn avec workers=4 pour les environnements de production.")
        suggestions.append("Mettre en cache les réponses statiques avec FastAPI Cache.")
    elif topic in ("security", "auth"):
        suggestions.append("Vérifier les tokens API dans les endpoints sensibles.")
        suggestions.append("Mettre en place un middleware d’audit pour les appels GPT externes.")
    else:
        suggestions.append("Analyser la cohérence de la mémoire avant chaque déploiement.")
        suggestions.append("Mettre à jour la documentation automatique des endpoints dans Swagger.")

    return {
        "status": "ok",
        "topic": topic,
        "suggestions": suggestions,
        "timestamp": datetime.utcnow().isoformat(),
    }

async def cortex_repair(req: RepairRequest):
    file_path = Path(req.filename)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    shutil.copy(file_path, backup_path)

    content = file_path.read_text(encoding="utf-8")
    fixed = re.sub(r"print\((['\"])(.*?)\1\)", r"logger.info(\1\2\1)", content)

    file_path.write_text(fixed, encoding="utf-8")
    _log(f"Fichier {req.filename} réparé (raison : {req.reason})")

    return {
        "status": "ok",
        "file_repaired": req.filename,
        "backup_created": str(backup_path),
        "timestamp": datetime.utcnow().isoformat(),
    }
