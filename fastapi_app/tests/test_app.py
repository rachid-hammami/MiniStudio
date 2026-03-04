# ==============================================
# 🧪 Fichier de tests unitaires MiniStudioGPT v1.4.5
# Objectif : Vérifier la stabilité des endpoints principaux
# Auteur : PulsR / CodeGPT / MiniStudioGPT
# Date : 03/11/2025
# ==============================================

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi_app.main import app
from pathlib import Path

# Transport compatible HTTPX >= 0.24
transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_ping_endpoint():
    """Vérifie que le backend répond correctement sur /project/ping"""
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/project/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "MiniStudioGPT" in data["message"]


@pytest.mark.asyncio
async def test_read_main_py():
    """Teste lecture/écriture/suppression de fichier projet avec log automatique"""
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1️⃣ Lecture du fichier principal
        response = await client.post(
            "/project/read", json={"filename": "fastapi_app/main.py"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "FastAPI" in data["content"]

        # 2️⃣ Écriture d’un fichier temporaire
        test_filename = "memory/test_write_check.txt"
        write_resp = await client.post(
            "/project/write",
            json={"filename": test_filename, "content": "MiniStudioGPT Write Test OK"},
        )
        assert write_resp.status_code == 200
        assert write_resp.json()["status"] == "ok"

        # 3️⃣ Lecture du fichier temporaire
        read_resp = await client.post("/project/read", json={"filename": test_filename})
        assert read_resp.status_code == 200
        assert "MiniStudioGPT Write Test OK" in read_resp.json()["content"]

        # 4️⃣ Suppression du fichier temporaire
        del_resp = await client.post(
            "/project/delete", json={"filename": test_filename}
        )
        assert del_resp.status_code == 200
        assert del_resp.json()["status"] == "ok"

        # 5️⃣ Log automatique dans memory/session.log
        log_entry = f"[TEST] Lecture/écriture/suppression réussie ({test_filename})\n"
        session_log_path = Path("memory/session.log")
        session_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(session_log_path, "a", encoding="utf-8") as log:
            log.write(log_entry)


@pytest.mark.asyncio
async def test_apply_code_security():
    """Vérifie le refus d’un fichier non Python"""
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/project/apply-code",
            json={"filename": "README.md", "content": "def fake(): pass"},
        )
    assert response.status_code == 400


# ==============================================
# 🧪 Tests additionnels : FastAPI Notes
# Objectif : Vérifier les routes /notes
# ==============================================

from fastapi.testclient import TestClient

client = TestClient(app)


def test_add_note():
    response = client.post(
        "/notes", json={"id": 0, "title": "Test Note", "content": "Contenu de test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Contenu de test"


def test_list_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(note["title"] == "Test Note" for note in data)


def test_delete_note():
    response = client.get("/notes")
    notes = response.json()
    if notes:
        note_id = notes[0]["id"]
        delete_response = client.delete(f"/notes/{note_id}")
        assert delete_response.status_code == 200
        assert f"Note {note_id} supprimée" in delete_response.json()["message"]
    else:
        assert True
