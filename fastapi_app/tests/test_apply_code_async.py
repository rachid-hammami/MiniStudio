"""
MiniStudioGPT v1.4.4 — Test Apply-Code (Async)
----------------------------------------------
Test direct via FastAPI sans dépendance réseau :
✅ Validation complète des endpoints
✅ Création automatique / rollback / sécurité
✅ Compatible httpx>=0.28 et pytest+anyio
"""

import pytest
from httpx import AsyncClient, ASGITransport
import importlib.util, pathlib, sys, os, time

pytestmark = pytest.mark.anyio("asyncio")

# =====================================================
# 🔧 Chargement dynamique de main.py (FastAPI)
# =====================================================
root = pathlib.Path(__file__).parent.resolve()
main_path = root / "fastapi_app" / "main.py"

spec = importlib.util.spec_from_file_location("main", main_path)
main = importlib.util.module_from_spec(spec)
sys.modules["main"] = main
spec.loader.exec_module(main)

app = main.app

# =====================================================
# 🔬 Fichier cible de test
# =====================================================
TEST_FILE = "./fastapi_app/test_apply_target_async.py"


@pytest.mark.anyio
async def test_apply_code_async_v144():
    # =====================================================
    # 1️⃣ Préparation du fichier cible
    # =====================================================
    os.makedirs("./fastapi_app", exist_ok=True)
    if not os.path.exists(TEST_FILE):
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            f.write("def dummy():\n    return 'old version'\n")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # --- Lecture étendue ---
        payload = {"filename": TEST_FILE}
        r = await ac.post("/project/read", json=payload)
        assert r.status_code == 200
        print("✅ Lecture étendue réussie (async)")
        assert "content" in r.json()

        # --- Patch fonction existante ---
        new_code = """\
def dummy():
    print("✅ Async Apply-Code Function – MiniStudioGPT v1.4.4")
    return "patched version"
"""
        payload = {"filename": TEST_FILE, "content": new_code}
        r = await ac.post("/project/apply-code", json=payload)
        resp = r.json()
        print("Response:", resp)
        assert r.status_code == 200, "❌ Apply-code a échoué (patch)"
        assert resp.get("server_version") == "v1.4.4"
        assert "patched version" in open(TEST_FILE, encoding="utf-8").read()
        print("✅ Fonction existante patchée avec succès")

        # --- Création automatique de fonction absente ---
        missing_func = """\
def async_autocreate():
    print("✨ Fonction absente créée automatiquement")
    return "created"
"""
        payload = {"filename": TEST_FILE, "content": missing_func}
        r = await ac.post("/project/apply-code", json=payload)
        resp = r.json()
        print("Response (create):", resp)
        assert r.status_code == 200
        assert "async_autocreate" in open(TEST_FILE, encoding="utf-8").read()
        print("✅ Création automatique de fonction absente validée")

        # --- Test rollback (erreur syntaxe volontaire) ---
        bad_code = "def bad_func(:\n    return 'oops'"
        backup = open(TEST_FILE, encoding="utf-8").read()
        payload = {"filename": TEST_FILE, "content": bad_code}
        r = await ac.post("/project/apply-code", json=payload)
        print("Rollback test status:", r.status_code)
        assert r.status_code == 500, "❌ Erreur syntaxe non détectée"
        time.sleep(0.5)
        after = open(TEST_FILE, encoding="utf-8").read()
        assert backup == after, "❌ Rollback non effectué correctement"
        print("✅ Rollback validé après erreur de syntaxe")

        # --- Sécurité /project/read sur .env ---
        payload = {"filename": ".env"}
        r = await ac.post("/project/read", json=payload)
        assert r.status_code == 403
        print("✅ Sécurité active : fichier .env refusé")

    print("\n=== ✅ Tous les tests async Apply-Code v1.4.4 terminés avec succès ===")
