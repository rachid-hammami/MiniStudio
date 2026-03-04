# ============================================================
#  fastapi_app/services/cortex_service.py
#  MiniStudioGPT — CORTEX v1.5
#  Service Layer : moteur logique d’analyse et cohérence projet
# ============================================================

from datetime import datetime
from fastapi import HTTPException
from fastapi_app.cortex.cortex_engine import (
    cortex_analyze, cortex_suggest, cortex_repair,
    AnalyzeRequest, SuggestRequest, RepairRequest
)
from pathlib import Path
import json, asyncio

class CortexService:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.log_file = self.project_root / "memory" / "session_audit.log"
        self._ensure_log_file()

    def _ensure_log_file(self):
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.write_text("")

    def _log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[CORTEX] {timestamp} — {message}\n"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry)

    async def run_analysis(self):
        req = AnalyzeRequest(depth=2)
        result = await cortex_analyze(req)
        self._log("Analyse exécutée via service.")
        return result

    async def generate_suggestions(self, topic="general"):
        req = SuggestRequest(topic=topic)
        result = await cortex_suggest(req)
        self._log(f"Suggestions générées ({topic}).")
        return result

    async def auto_repair(self, filename, reason="auto"):
        req = RepairRequest(filename=filename, reason=reason)
        result = await cortex_repair(req)
        self._log(f"Auto-repair exécuté pour {filename}.")
        return result
