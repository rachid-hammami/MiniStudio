"""
MiniStudioGPT v1.3 – Logging Utility
------------------------------------
Ce module permet au Builder MiniStudioGPT d’enregistrer automatiquement ses événements
dans le fichier `session.log` du backend, via l’endpoint `/project/write`.

Fonction principale : log_event(event_text)
Compatibilité : Cloudflare Tunnel (https://ministudio.store)
Auteur : PulsR / CodeGPT
Date : 2025-11
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from time import sleep

# ==============================
# 🔧 Configuration globale
# ==============================

DEFAULT_ENDPOINT = os.getenv("MINISTUDIO_API_WRITE", "https://ministudio.store/project/write")
FALLBACK_LOG_PATH = Path("./memory/session_local_fallback.log")

# ==============================
# 🧠 Fonction principale
# ==============================

def log_event(event_text: str,
              endpoint: str = DEFAULT_ENDPOINT,
              retries: int = 2,
              delay: float = 1.5) -> bool:
    """
    Journalise un événement dans la mémoire distante (session.log) du backend MiniStudioGPT.
    
    Args:
        event_text (str): Texte brut de l’événement à consigner.
        endpoint (str): URL de l’API /project/write.
        retries (int): Nombre de tentatives de réenvoi.
        delay (float): Délai entre les tentatives.

    Returns:
        bool: True si la requête a réussi, False sinon.
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    formatted = f"[{timestamp}] {event_text}"

    payload = {
        "filename": "memory/session.log",
        "content": formatted
    }

    # ============================
    # Tentative de requête HTTP
    # ============================
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(endpoint, json=payload, timeout=6)
            if response.status_code == 200:
                print(f"[MiniStudioGPT Log] ✅ {formatted}")
                return True
            else:
                print(f"[MiniStudioGPT Log] ⚠️ Erreur HTTP ({response.status_code}) – tentative {attempt}/{retries}")
        except Exception as e:
            print(f"[MiniStudioGPT Log] ⚠️ Exception lors du log (tentative {attempt}/{retries}): {e}")
        sleep(delay)

    # ============================
    # Échec → Fallback local
    # ============================
    try:
        FALLBACK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(FALLBACK_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
        print(f"[MiniStudioGPT Log] 🔄 Sauvegarde locale (fallback) : {FALLBACK_LOG_PATH}")
        return False
    except Exception as e:
        print(f"[MiniStudioGPT Log] ❌ Impossible d’écrire le fallback : {e}")
        return False


# ==============================
# 🚀 Exemple d’utilisation
# ==============================
if __name__ == "__main__":
    # Exemple d’appel autonome (pour test direct)
    success = log_event("Session démarrée – test manuel du logger")
    if success:
        print("✅ Journalisation distante réussie.")
    else:
        print("⚠️ Journalisation fallback locale utilisée.")
