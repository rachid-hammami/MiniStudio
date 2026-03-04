"""
MiniStudioGPT v1.4.4 — Test Apply-Code Endpoint
------------------------------------------------
Ce test vérifie :
1. L’accès sécurisé à /project/read
2. Le bon fonctionnement de /project/apply-code (création et patch)
3. La gestion des erreurs et rollback
4. Le champ server_version=v1.4.4 dans toutes les réponses
"""

import requests
import json
import os
import time

BASE_URL = "https://ministudio.store/project"
TEST_FILE = "./fastapi_app/test_apply_target.py"

# --- Préparation du fichier cible ---
os.makedirs("./fastapi_app", exist_ok=True)
if not os.path.exists(TEST_FILE):
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("def dummy():\n    return 'old version'\n")

# =====================================================
# 1️⃣ TEST /project/read — lecture étendue sécurisée
# =====================================================
print("\n=== TEST 1 : Lecture étendue ===")
payload = {"filename": TEST_FILE}
r = requests.post(f"{BASE_URL}/read", json=payload)
print("Status:", r.status_code)
print("Server version:", r.json().get("server_version", "non précisé"))
print("Extrait du contenu:", r.json().get("content", "")[:100], "...")
assert r.status_code == 200, "❌ Lecture échouée"
print("✅ Lecture sécurisée OK")

# =====================================================
# 2️⃣ TEST /project/apply-code — patch d’une fonction existante
# =====================================================
print("\n=== TEST 2 : Apply-code (patch fonction existante) ===")
new_function_code = """\
def dummy():
    print("✅ Function patched by MiniStudioGPT v1.4.4")
    return "patched version"
"""
payload = {"filename": TEST_FILE, "content": new_function_code}
r = requests.post(f"{BASE_URL}/apply-code", json=payload)
print("Status:", r.status_code)
print("Response:", r.json())
assert r.status_code == 200, "❌ Apply-code a échoué"
assert (
    "patched version" in open(TEST_FILE, encoding="utf-8").read()
), "❌ Patch non détecté"
print("✅ Patch confirmé")

# =====================================================
# 3️⃣ TEST création automatique de fonction absente
# =====================================================
print("\n=== TEST 3 : Création automatique de fonction absente ===")
missing_func_code = """\
def brand_new_feature():
    print('✨ Nouvelle fonction créée automatiquement')
    return 'ok'
"""
payload = {"filename": TEST_FILE, "content": missing_func_code}
r = requests.post(f"{BASE_URL}/apply-code", json=payload)
resp = r.json()
print("Status:", r.status_code)
print("Response:", resp)
assert r.status_code == 200, "❌ Apply-code a échoué pour création automatique"
assert (
    "brand_new_feature" in open(TEST_FILE, encoding="utf-8").read()
), "❌ Fonction non créée"
assert resp.get("server_version") == "v1.4.4", "❌ Mauvaise version serveur"
print("✅ Création automatique OK")

# =====================================================
# 4️⃣ TEST rollback sur code erroné
# =====================================================
print("\n=== TEST 4 : Rollback sur erreur de syntaxe ===")
bad_code = "def bad_func(:\n    return 'oops'"
backup = open(TEST_FILE, encoding="utf-8").read()
payload = {"filename": TEST_FILE, "content": bad_code}
r = requests.post(f"{BASE_URL}/apply-code", json=payload)
print("Status:", r.status_code)
print("Response:", r.json())
time.sleep(1)  # Laisse le temps au rollback
after = open(TEST_FILE, encoding="utf-8").read()
assert backup == after, "❌ Rollback non appliqué après erreur de syntaxe"
print("✅ Rollback validé")

# =====================================================
# 5️⃣ TEST accès refusé
# =====================================================
print("\n=== TEST 5 : Sécurité (accès refusé) ===")
forbidden_file = ".env"
payload = {"filename": forbidden_file}
r = requests.post(f"{BASE_URL}/apply-code", json=payload)
print("Status attendu 400 →", r.status_code)
if r.status_code == 400:
    print("✅ Accès refusé confirmé (sécurité active)")
else:
    print("⚠️ Sécurité potentiellement défaillante !")

print("\n=== ✅ Tous les tests Apply-Code v1.4.4 terminés avec succès ===")
