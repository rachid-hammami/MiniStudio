# ==============================================================
# 📘 FastAPI Notes v1.0 - Module annexe pour MiniStudioGPT
# ==============================================================
# Gère les notes locales (ajout, lecture, suppression)
# Stockage dans fastapi_app/notes.json
# Auteur : Code GPT / PulsR
# Date : 2025-11-01
# ==============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json, os
from typing import List, Dict

router = APIRouter(prefix="", tags=["Notes"])

# --------------------------------------------------------------
# 🧱 Modèle Pydantic
# --------------------------------------------------------------
class Note(BaseModel):
    title: str
    content: str

# --------------------------------------------------------------
# 📂 Fichier de stockage
# --------------------------------------------------------------
NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.json")

def _load_notes() -> List[Dict]:
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_notes(notes: List[Dict]) -> None:
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

# --------------------------------------------------------------
# 🔹 GET /notes - Liste toutes les notes
# --------------------------------------------------------------
@router.get("/notes")
async def get_notes():
    """Récupère la liste complète des notes."""
    return _load_notes()

# --------------------------------------------------------------
# 🔹 POST /notes - Ajoute une nouvelle note
# --------------------------------------------------------------
@router.post("/notes")
async def add_note(note: Note):
    """Ajoute une nouvelle note au fichier JSON."""
    notes = _load_notes()
    next_id = max((n["id"] for n in notes), default=0) + 1
    new_note = {"id": next_id, "title": note.title, "content": note.content}
    notes.append(new_note)
    _save_notes(notes)
    return new_note

# --------------------------------------------------------------
# 🔹 DELETE /notes/{id} - Supprime une note
# --------------------------------------------------------------
@router.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    """Supprime une note via son ID."""
    notes = _load_notes()
    filtered = [n for n in notes if n["id"] != note_id]
    if len(filtered) == len(notes):
        raise HTTPException(status_code=404, detail=f"Note {note_id} introuvable")
    _save_notes(filtered)
    return {"message": f"Note {note_id} supprimée avec succès"}

# --------------------------------------------------------------
# ✅ Healthcheck du module
# --------------------------------------------------------------
@router.get("/notes/ping", include_in_schema=False)
async def notes_ping():
    """Ping simple pour vérifier la disponibilité du module Notes."""
    return {"status": "ok", "module": "FastAPI Notes", "file": "notes.json"}
