"""MiniStudioGPT v1.4.4 - Controller Collaboratif IA ↔ API
-------------------------------------------------------
Ajout : détection automatique de port (8000 / 8100 / 8080)
"""

import json, os, datetime, requests, time

POSSIBLE_BASES = [
    "http://127.0.0.1:8000/project",
    "http://127.0.0.1:8100/project",
    "http://127.0.0.1:8080/project",
    "http://localhost:8000/project",
    "http://localhost:8100/project",
]

MEMORY_PATH = "./memory/memoire.json"
DRAFTS_PATH = "./memory/drafts/"
SESSION_LOG = "./memory/session.log"

def auto_detect_base_url():
    print("[MiniStudioGPT] 🔍 Détection du port FastAPI en cours...")
    for base in POSSIBLE_BASES:
        try:
            res = requests.get(f"{base.replace('/project', '')}/project/ping", timeout=1)
            if res.status_code == 200:
                print(f"[MiniStudioGPT] ✅ Port détecté : {base}")
                return base
        except requests.exceptions.RequestException:
            continue
    print("[MiniStudioGPT] 🚨 Aucun serveur FastAPI détecté sur les ports habituels (8000/8100/8080).")
    return None

BASE_URL = auto_detect_base_url() or "http://127.0.0.1:8000/project"

class MiniStudioController:
    def __init__(self, mode="review"):
        self.mode = mode
        os.makedirs(DRAFTS_PATH, exist_ok=True)
        print(f"[MiniStudioGPT] 🎮 Mode collaboratif initialisé → {self.mode.upper()}")
        print(f"[MiniStudioGPT] 🌐 API connectée sur : {BASE_URL}")

    def propose_change(self, filepath: str, func_name: str, new_code: str, mode=None):
        mode = mode or self.mode
        payload = {
            "filepath": filepath,
            "func_name": func_name,
            "new_code": new_code,
            "mode": mode
        }

        if not BASE_URL:
            print("🚨 Aucun serveur FastAPI disponible.")
            return

        try:
            res = requests.post(f"{BASE_URL}/propose", json=payload)
            if res.status_code == 200:
                data = res.json()
                print(f"✅ Proposition enregistrée → {data}")
                if mode == "auto":
                    print("⚡ Application immédiate du patch...")
                    self.apply_last_proposal(data.get('draft'))
            else:
                print(f"❌ Erreur : {res.status_code} → {res.text}")
        except requests.exceptions.ConnectionError as e:
            print(f"🚨 Erreur de connexion à l'API FastAPI : {e}")

    def apply_last_proposal(self, draft_file=None):
        if not BASE_URL:
            print("🚨 Aucun serveur FastAPI disponible.")
            return
        if not draft_file:
            drafts = sorted(os.listdir(DRAFTS_PATH))
            if not drafts:
                print("⚠️ Aucun draft disponible.")
                return
            draft_file = drafts[-1]
        try:
            with open(os.path.join(DRAFTS_PATH, draft_file), "r", encoding="utf-8") as f:
                draft_data = json.load(f)
            filepath = draft_data["filepath"]
            func_name = draft_data["func_name"]
            res = requests.post(
                f"{BASE_URL}/apply",
                params={"filepath": filepath, "func_name": func_name, "draft_file": draft_file}
            )
            print(f"⚙️ Résultat apply → {res.json()}")
        except Exception as e:
            print(f"🚨 Erreur d’application du patch : {e}")

    def list_drafts(self):
        drafts = []
        for file in os.listdir(DRAFTS_PATH):
            path = os.path.join(DRAFTS_PATH, file)
            ts = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            age = (datetime.datetime.now() - ts).total_seconds() / 3600
            drafts.append({"file": file, "age_h": round(age, 2)})
        return drafts

    def purge_old_drafts(self):
        count = 0
        for file in os.listdir(DRAFTS_PATH):
            path = os.path.join(DRAFTS_PATH, file)
            ts = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            if (datetime.datetime.now() - ts).total_seconds() > 86400:
                os.remove(path)
                count += 1
        print(f"🧹 {count} draft(s) supprimé(s) (plus de 24h).")

    def status(self):
        memory = {}
        if os.path.exists(MEMORY_PATH):
            try:
                memory = json.load(open(MEMORY_PATH, "r", encoding="utf-8"))
            except Exception:
                pass

        last_logs = []
        if os.path.exists(SESSION_LOG):
            with open(SESSION_LOG, "r", encoding="utf-8") as f:
                last_logs = f.readlines()[-5:]

        print("\n=== STATUT MINI-STUDIO ===")
        print(f"Mode actuel : {self.mode}")
        print(f"Drafts présents : {len(os.listdir(DRAFTS_PATH))}")
        print(f"Derniers logs :")
        for l in last_logs:
            print(f"   {l.strip()}")
        print("===========================\n")


if __name__ == "__main__":
    ctrl = MiniStudioController(mode="review")
    ctrl.status()
