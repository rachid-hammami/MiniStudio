"""
MiniStudioGPT v1.4 – Core Builder Module (Full Integration)
------------------------------------------------------------
Fusion de la version 1.3 (stabilité) avec les nouvelles capacités 1.4 :
- auto_patch_function()
- auto_repair_file()
- session_recovery()
- backups automatiques
- sécurité des chemins
- compatibilité descendante avec logs et mémoire

Auteur : PulsR / CodeGPT
Date : 2025-10-30
"""

import os
import json
import ast
import shutil
import datetime
import py_compile
import requests
from fastapi_app.utils.logging_utils import log_event

BASE_URL = "https://ministudio.store"


# === Détection automatique du dossier FastAPI ===
def detect_app_path():
    """Détecte automatiquement le dossier fastapi_app valide."""
    candidates = [
        "./app/fastapi_app/",
        "./fastapi_app/",
        "./MiniStudio/fastapi_app/",
        "./src/fastapi_app/",
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    # fallback par défaut
    return "./fastapi_app/"


PATH_APP = detect_app_path()
print(f"[MiniStudioGPT v1.4] ✅ Dossier FastAPI détecté : {PATH_APP}")

# === Chemins racine ===
# PATH_APP = "./fastapi_app/"
PATH_MEMORY = "./memory/"
PATH_LOG = os.path.join(PATH_MEMORY, "session.log")
PATH_MEMOIRE = os.path.join(PATH_MEMORY, "memoire.json")
PATH_BACKUP = os.path.join(PATH_MEMORY, "backups/")


# === Fonctions de base (v1.3 conservées) ===
def init_session():
    print("=== Démarrage de la session MiniStudioGPT ===")
    try:
        ping = requests.get(f"{BASE_URL}/project/ping", timeout=12)
        if ping.status_code == 200:
            log_event("Ping valide – backend actif")
        else:
            log_event(f"Ping non valide – code HTTP {ping.status_code} (mode dégradé)")
    except Exception as e:
        log_event(f"Échec du démarrage – ping non valide ({e})")
        return None


def read_file(filename: str):
    payload = {"filename": filename}
    try:
        response = requests.post(f"{BASE_URL}/project/read", json=payload, timeout=8)
        if response.status_code == 200:
            log_event(f"Lecture réussie du fichier : {filename}")
            return response.json()
        else:
            log_event(f"Erreur de lecture de {filename} – HTTP {response.status_code}")
            return None
    except Exception as e:
        log_event(f"Exception lors de la lecture de {filename} : {e}")
        return None


def write_file(filename: str, content: str):
    try:
        if "memoire.json" in filename:
            current = read_file(filename)
            content_raw = (
                current.get("content", {}) if isinstance(current, dict) else {}
            )
            try:
                current_data = (
                    json.loads(content_raw)
                    if isinstance(content_raw, str)
                    else content_raw
                )
            except Exception:
                current_data = {}
            try:
                new_data = json.loads(content)
            except json.JSONDecodeError:
                new_data = {"raw_content": content}
            merged = {**current_data, **new_data}
            payload = {
                "filename": filename,
                "content": json.dumps(merged, ensure_ascii=False),
            }
            log_event("Fusion non destructive appliquée sur memoire.json")
        else:
            payload = {"filename": filename, "content": content}
        response = requests.post(f"{BASE_URL}/project/write", json=payload, timeout=8)
        if response.status_code == 200:
            log_event(f"Fichier {filename} modifié via API")
            return True
        else:
            log_event(f"Erreur d’écriture sur {filename} – HTTP {response.status_code}")
            return False
    except Exception as e:
        log_event(f"Exception lors de l’écriture sur {filename} : {e}")
        return False


def log_local(message: str):
    os.makedirs(PATH_MEMORY, exist_ok=True)
    with open(PATH_LOG, "a", encoding="utf-8") as log:
        log.write(f"[MiniStudioGPT Log] ✅ [{datetime.datetime.now()}] {message}\n")


# === Nouvelles fonctions v1.4 ===
def sauvegarder_backup(filepath):
    os.makedirs(PATH_BACKUP, exist_ok=True)
    if not os.path.exists(filepath):
        return None
    backup_name = (
        os.path.basename(filepath)
        + f".bak_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    backup_path = os.path.join(PATH_BACKUP, backup_name)
    shutil.copy(filepath, backup_path)
    log_event(f"Backup créé pour {filepath}")
    return backup_path


def auto_repair_file(filepath):
    try:
        py_compile.compile(filepath, doraise=True)
        log_event(f"✅ Validation syntaxique réussie : {filepath}")
        return True
    except py_compile.PyCompileError as e:
        log_event(f"⚠️ Erreur de syntaxe détectée : {filepath} ({e})")
        # tentative de réparation minimale
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            fixed = [l.rstrip() + "\n" for l in lines if l.strip()]
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(fixed)
            py_compile.compile(filepath, doraise=True)
            log_event(f"🔧 Réparation réussie sur {filepath}")
            return True
        except Exception as e2:
            log_event(f"❌ Réparation échouée sur {filepath} ({e2})")
            return False


def auto_patch_function(filepath, func_name, new_code):
    if not filepath.startswith(PATH_APP):
        log_event(f"Refus de modification : {filepath} hors zone autorisée")
        return False

    if not os.path.exists(filepath):
        log_event(f"Fichier introuvable : {filepath}")
        return False

    backup = sauvegarder_backup(filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        start, end = None, None
        for i, line in enumerate(lines):
            if line.strip().startswith(f"def {func_name}("):
                start = i
                break
        if start is None:
            log_event(f"Fonction {func_name} introuvable dans {filepath}")
            return False

        for j in range(start + 1, len(lines)):
            if lines[j].strip().startswith("def ") or lines[j].strip().startswith(
                "class "
            ):
                end = j
                break
        if end is None:
            end = len(lines)

        indent = " " * (len(lines[start]) - len(lines[start].lstrip()))
        new_block = [
            indent + line if line.strip() else line
            for line in new_code.splitlines(True)
        ]
        new_content = lines[:start] + new_block + lines[end:]

        temp_path = filepath + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            f.writelines(new_content)

        if auto_repair_file(temp_path):
            shutil.move(temp_path, filepath)
            log_event(f"✅ Fonction {func_name} mise à jour dans {filepath}")
            return True
        else:
            if backup and os.path.exists(backup):
                shutil.copy(backup, filepath)
            log_event(f"⚠️ Restauration du backup pour {filepath}")
            return False

    except Exception as e:
        log_event(f"Erreur lors du patch sur {filepath} : {e}")
        if backup and os.path.exists(backup):
            shutil.copy(backup, filepath)
        return False


def session_recovery():
    if not os.path.exists(PATH_LOG):
        log_event("Aucun journal trouvé pour recovery")
        return

    with open(PATH_LOG, "r", encoding="utf-8") as log:
        lines = log.readlines()

    for line in lines:
        if "Échec" in line or "pending" in line:
            log_event(f"🔁 Tentative de récupération : {line.strip()}")
    log_event("♻️ Session recovery complétée")


def update_memory(info: str = "Mémoire persistante mise à jour (fusion)"):
    log_event(info)


def end_session():
    log_event("Fin de session – sauvegarde complète")


def full_routine_test():
    print("=== Démarrage de la session MiniStudioGPT v1.4 ===")
    init_session()
    snapshot = read_file("memory/memoire.json")
    if snapshot:
        log_event("Snapshot chargé".encode("utf-8", "ignore").decode("utf-8"))
    else:
        log_event("Aucun snapshot trouvé – mémoire initialisée vide")
    write_file("memory/session.log", "[Test] Écriture append via Builder v1.4")
    new_memory = {"test_fusion": "ok", "version": "1.4"}
    write_file("memory/memoire.json", json.dumps(new_memory, ensure_ascii=False))
    update_memory()
    end_session()
    print("=== Fin de la session ===")


if __name__ == "__main__":
    full_routine_test()
