# ============================================================
# 🧠 MiniStudioGPT v1.5 — Test Unifié Cortex + Project
# Auteur : Code GPT / PulsR
# Date : 2025-11-09
# ============================================================

import requests
import json
from datetime import datetime
from pathlib import Path
import os

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
BASE_URL = os.getenv("CORTEX_BASE_URL", "http://127.0.0.1:8100")
MEMORY_DIR = Path("memory")
REPORT_PATH = MEMORY_DIR / "test_report.json"
AUDIT_PATH = MEMORY_DIR / "session_audit.log"
PROJECT_MAP_PATH = MEMORY_DIR / "project_map.json"

# ------------------------------------------------------------
# Outils internes
# ------------------------------------------------------------
def log(msg: str):
    """Affiche et enregistre dans le log mémoire."""
    print(msg)
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(f"[TEST v1.5] {datetime.now().isoformat()} | {msg}\n")

def test_endpoint(route: str, method="get", payload=None):
    """Teste un endpoint FastAPI et renvoie le résultat JSON ou None."""
    url = f"{BASE_URL}{route}"
    try:
        if method.lower() == "get":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=payload or {}, timeout=10)
        response.raise_for_status()
        data = response.json()
        log(f"✅ {route} → OK ({response.status_code})")
        return data
    except Exception as e:
        log(f"❌ {route} → {e}")
        return None

def check_memory_integrity():
    """Vérifie la cohérence de la mémoire et du project_map."""
    report = {}
    if PROJECT_MAP_PATH.exists():
        try:
            data = json.loads(PROJECT_MAP_PATH.read_text(encoding="utf-8"))
            report["project_map_files"] = len(data)
            log(f"🧩 project_map.json chargé ({len(data)} fichiers)")
        except Exception as e:
            log(f"⚠️ Erreur lecture project_map.json : {e}")
            report["project_map_files"] = 0
    else:
        log("⚠️ project_map.json introuvable")

    if AUDIT_PATH.exists():
        lines = AUDIT_PATH.read_text(encoding="utf-8").splitlines()
        recent = lines[-5:] if len(lines) > 5 else lines
        report["audit_tail"] = recent
        log(f"🧠 Journal d’audit contient {len(lines)} lignes")
    else:
        log("⚠️ Aucun fichier session_audit.log détecté")

    return report

# ------------------------------------------------------------
# Tests principaux
# ------------------------------------------------------------
def run_all_tests():
    """Exécute l'ensemble des tests Cortex + Project."""
    log("=== 🧠 Démarrage du Test Unifié MiniStudio v1.5 ===")
    report = {"timestamp": datetime.now().isoformat(), "results": {}, "status": "ok"}

    # --- Project layer ---
    report["results"]["ping"] = test_endpoint("/project/ping")
    report["results"]["map_update"] = test_endpoint("/project/map/update", method="post")
    report["results"]["snapshot"] = test_endpoint("/project/snapshot")

    # --- Cortex layer ---
    report["results"]["check_integrity"] = test_endpoint("/cortex/check-integrity")
    report["results"]["map_inspect"] = test_endpoint("/cortex/map-inspect")
    report["results"]["analyze"] = test_endpoint("/cortex/analyze", method="post")
    report["results"]["suggest"] = test_endpoint("/cortex/suggest", method="post")
    report["results"]["auto_fix"] = test_endpoint("/cortex/auto-fix", method="post")

    # --- Vérification interne ---
    report["results"]["memory_check"] = check_memory_integrity()

    # --- Évaluation du statut global ---
    failures = [k for k, v in report["results"].items() if v is None]
    report["status"] = "failed" if failures else "ok"

    # --- Sauvegarde du rapport ---
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if failures:
        log(f"❌ Tests échoués sur : {', '.join(failures)}")
    else:
        log("✅ Tous les endpoints testés avec succès.")
    log(f"🧾 Rapport complet : {REPORT_PATH}")
    log("=== Fin du Test Unifié ===")

# ------------------------------------------------------------
# Lancement direct
# ------------------------------------------------------------
if __name__ == "__main__":
    run_all_tests()
