"""
MiniStudioGPT v1.4.6 — Docker Health & Cortex Sync Check
Auteur : Code GPT 🧠
Date : 2025-11-08
Usage :
    python fastapi_app/core/check_docker_health.py
Description :
    Vérifie la santé du backend MiniStudioGPT, la synchronisation Cortex,
    la mémoire cognitive et les logs d’audit.
"""

import requests
import os
import json
from datetime import datetime
from pathlib import Path

# ==============================================================
# ⚙️ Configuration
# ==============================================================
LOCAL_URL = "http://localhost:8000"
ENDPOINTS = {
    "ping": "/project/ping",
    "context": "/project/context",
    "memory": "/project/memory",
    "logs": "/project/logs/audit",
}

MEMORY_DIR = Path("memory")
AUDIT_LOG_PATH = MEMORY_DIR / "session_audit.log"
REPORT_PATH = MEMORY_DIR / "docker_health_report.json"


# ==============================================================
# 🧩 Fonctions utilitaires
# ==============================================================
def _log(message: str):
    """Ajoute un message dans le journal d’audit et affiche à l’écran."""
    print(message)
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[Docker Health v1.4.6] {datetime.now().isoformat()} | {message}\n")


def _check_endpoint(name: str, route: str):
    """Teste un endpoint du backend."""
    url = f"{LOCAL_URL}{route}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            _log(f"✅ {name} → OK ({route})")
            return {"endpoint": route, "status": "ok", "data": data}
        else:
            _log(f"❌ {name} → HTTP {response.status_code}")
            return {"endpoint": route, "status": "error", "code": response.status_code}
    except Exception as e:
        _log(f"⚠️ {name} → Erreur : {e}")
        return {"endpoint": route, "status": "failed", "error": str(e)}


# ==============================================================
# 🧠 Vérification complète
# ==============================================================
def check_docker_health():
    """Exécute la vérification complète du système."""
    print("\n🔍 Vérification du conteneur MiniStudioGPT v1.4.6")
    print("=" * 60)

    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "v1.4.6",
        "checks": {},
        "status": "ok",
    }

    # 1️⃣ Vérification du ping
    report["checks"]["ping"] = _check_endpoint("Backend Ping", ENDPOINTS["ping"])

    # 2️⃣ Vérification du contexte projet
    report["checks"]["context"] = _check_endpoint("Cortex Context", ENDPOINTS["context"])

    # 3️⃣ Vérification mémoire cognitive
    report["checks"]["memory"] = _check_endpoint("Mémoire Cognitive", ENDPOINTS["memory"])

    # 4️⃣ Lecture du journal d’audit
    report["checks"]["logs"] = _check_endpoint("Audit Logs", ENDPOINTS["logs"])

    # 5️⃣ Vérification du fichier de sauvegarde le plus récent
    backups = list(MEMORY_DIR.glob("MiniStudio_backup_*.zip"))
    if backups:
        last_backup = max(backups, key=os.path.getmtime)
        size_kb = os.path.getsize(last_backup) // 1024
        report["last_backup"] = {"file": str(last_backup), "size_kb": size_kb}
        _log(f"💾 Dernier backup détecté : {last_backup.name} ({size_kb} Ko)")
    else:
        _log("⚠️ Aucun backup détecté dans /memory")

    # 6️⃣ Vérification de cohérence des résultats
    critical_failures = [
        k for k, v in report["checks"].items()
        if v.get("status") not in ["ok"]
    ]
    if critical_failures:
        report["status"] = "failed"
        _log(f"❌ Incohérence détectée sur : {', '.join(critical_failures)}")
    else:
        _log("✅ Tous les endpoints Cortex sont opérationnels")

    # 7️⃣ Sauvegarde du rapport JSON
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    _log(f"🧾 Rapport complet écrit dans {REPORT_PATH}")

    print("=" * 60)
    print("🧠 Rapport global :", report["status"])
    print("📜 Détails :", REPORT_PATH)
    print("🕒 Test terminé à", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    return report


# ==============================================================
# 🚀 Main
# ==============================================================
if __name__ == "__main__":
    check_docker_health()
