"""
MiniStudioGPT v1.4.4 â€” Test collaboratif complet
------------------------------------------------
Ce test simule le flux complet IA â†” API â†” Builder :
1. Proposition de changement de code (mode review)
2. Application via /project/apply-code
3. VÃ©rification de la mÃ©moire et des journaux
4. Validation de la robustesse et de la tolÃ©rance v1.4.4
"""

import time
from fastapi_app.core.controller_collab import MiniStudioController
import os
import json
from datetime import datetime

# ======================================
# ðŸ”§ Ã‰tape 1 : Initialisation du contrÃ´leur
# ======================================
ctrl = MiniStudioController(mode="review")
print("\n=== Ã‰tape 1 : Initialisation ===")
ctrl.status()

# ======================================
# ðŸ§  Ã‰tape 2 : Proposition de modification
# ======================================
print("\n=== Ã‰tape 2 : Proposition de modification ===")

TARGET_FILE = "./fastapi_app/test_patch_target.py"
FUNC_NAME = "hello_world_v144"
NEW_CODE = """
def hello_world_v144():
    print("ðŸ‘‹ Salut depuis MiniStudioGPT v1.4.4 â€” version tolÃ©rante et robuste")
    return "hello v1.4.4"
"""

ctrl.propose_change(
    filepath=TARGET_FILE, func_name=FUNC_NAME, new_code=NEW_CODE, mode="review"
)

# Simulation dâ€™un dÃ©lai de rÃ©vision IA â†” API
time.sleep(1)

# ======================================
# âš™ï¸ Ã‰tape 3 : Application du patch
# ======================================
print("\n=== Ã‰tape 3 : Application du patch ===")
try:
    result = ctrl.apply_last_proposal()
    print("RÃ©sultat de lâ€™application :", result)
except Exception as e:
    print("âŒ Erreur durant lâ€™application :", e)

# Pause pour journalisation et Ã©criture mÃ©moire
time.sleep(1.5)

# ======================================
# ðŸ’¾ Ã‰tape 4 : VÃ©rification mÃ©moire et logs enrichis
# ======================================
print("\n=== Ã‰tape 4 : VÃ©rification mÃ©moire et logs ===")

MEMORY_PATH = "./memory/memoire.json"
SESSION_LOG = "./memory/session.log"
AUDIT_LOG = "./memory/session_audit.log"


def show_tail(path, lines=10):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            print(f"\nðŸ§¾ DerniÃ¨res lignes de {path}:")
            for line in f.readlines()[-lines:]:
                print(line.strip())
    else:
        print(f"âš ï¸ Fichier {path} introuvable")


# --- VÃ©rification mÃ©moire principale ---
if os.path.exists(MEMORY_PATH):
    memoire = json.load(open(MEMORY_PATH, "r", encoding="utf-8"))
    print(f"ðŸ§  MÃ©moire chargÃ©e ({len(memoire)} clÃ©s)")
    last_patch = memoire.get("last_patch", {})
    if last_patch:
        print("âœ… Dernier patch enregistrÃ© :", last_patch)
        assert FUNC_NAME in str(
            last_patch
        ), "âŒ Fonction non dÃ©tectÃ©e dans la mÃ©moire"
    else:
        print("âš ï¸ Aucun patch trouvÃ© dans la mÃ©moire.")
else:
    print("ðŸš¨ Fichier memoire.json introuvable !")

# --- Logs session standard ---
show_tail(SESSION_LOG, 10)

# --- Logs dâ€™audit v1.4.4 ---
show_tail(AUDIT_LOG, 10)

# ======================================
# ðŸ§© Ã‰tape 5 : VÃ©rification rollback et robustesse
# ======================================
print("\n=== Ã‰tape 5 : Test de rollback automatique ===")

BAD_CODE = "def broken_func(:\n    return 'fail'"
ctrl.propose_change(
    filepath=TARGET_FILE, func_name="broken_func", new_code=BAD_CODE, mode="review"
)

try:
    ctrl.apply_last_proposal()
except Exception as e:
    print("âœ… Erreur dÃ©tectÃ©e (attendue) :", e)

# VÃ©rification du rollback
time.sleep(1)
if os.path.exists(TARGET_FILE):
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        data = f.read()
    assert "broken_func" not in data, "âŒ Rollback Ã©chouÃ©, code erronÃ© prÃ©sent"
    print("âœ… Rollback confirmÃ© : fichier restaurÃ©")

# ======================================
# âœ… Fin du test collaboratif
# ======================================
print("\n=== âœ… Test collaboratif MiniStudioGPT v1.4.4 terminÃ© avec succÃ¨s ===")
print(f"Horodatage : {datetime.now().isoformat()}")
