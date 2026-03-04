"""
MiniStudioGPT v1.3 – Log Validation Utility
-------------------------------------------
Ce module vérifie la cohérence et la complétude du journal `session.log`
en le récupérant via `/project/snapshot`. Il confirme que les événements
majeurs du Builder sont bien consignés selon les exigences du cahier des charges v1.3.

Auteur : PulsR / CodeGPT
Date : 2025-11
"""

import requests
from datetime import datetime
from typing import List, Dict

BASE_URL = "https://ministudio.store"

# ==============================
# 🧠 1. Téléchargement du snapshot
# ==============================


def fetch_snapshot() -> Dict:
    """
    Récupère la mémoire complète du projet (incluant session.log)
    depuis /project/snapshot.
    """
    try:
        response = requests.get(f"{BASE_URL}/project/snapshot", timeout=8)
        if response.status_code == 200:
            data = response.json()
            return data.get("snapshot", {})
        else:
            print(f"[Validation] ⚠️ Erreur HTTP {response.status_code}")
            return {}
    except Exception as e:
        print(f"[Validation] ❌ Exception lors du snapshot : {e}")
        return {}


# ==============================
# 🧩 2. Analyse du journal
# ==============================


def analyze_log(session_log: str) -> Dict[str, bool]:
    """
    Analyse le contenu de session.log pour détecter la présence
    des événements clés exigés par le cahier des charges v1.3.
    """
    checks = {
        "Session démarrée": "Session démarrée" in session_log,
        "Snapshot chargé": "snapshot chargé" in session_log.lower(),
        "Fichier modifié": "modifié via API" in session_log,
        "Mémoire mise à jour": "Mémoire persistante mise à jour" in session_log,
        "Fin de session": "Fin de session" in session_log,
    }
    return checks


# ==============================
# 🔎 3. Validation complète
# ==============================


def validate_logs() -> None:
    """
    Effectue une validation complète de la journalisation Builder.
    """
    snapshot = fetch_snapshot()
    session_log = snapshot.get("session_log", "")

    if not session_log:
        print("❌ Aucun contenu trouvé dans session.log")
        return

    checks = analyze_log(session_log)

    print("\n=== 🔍 Validation MiniStudioGPT v1.3 – Journalisation automatique ===")
    for key, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {key}")

    completeness = sum(checks.values()) / len(checks)
    print(f"\nTaux de conformité : {completeness*100:.1f}%")

    if completeness == 1:
        print("🎉 Journalisation Builder conforme au cahier des charges v1.3 !")
    else:
        print("⚠️ Des événements requis sont manquants dans session.log.")


# ==============================
# 🚀 4. Test autonome
# ==============================

if __name__ == "__main__":
    validate_logs()
