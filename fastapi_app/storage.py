import json
import os
from typing import List, Dict

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.json")


def load_notes() -> List[Dict]:
    """Charge les notes depuis le fichier JSON, ou renvoie une liste vide si le fichier n'existe pas."""
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_notes(notes: List[Dict]) -> None:
    """Sauvegarde la liste des notes dans le fichier JSON."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def add_note(title: str, content: str) -> Dict:
    """Ajoute une nouvelle note avec id auto-incrémenté."""
    notes = load_notes()
    new_id = max([note["id"] for note in notes], default=0) + 1
    new_note = {"id": new_id, "title": title, "content": content}
    notes.append(new_note)
    save_notes(notes)
    return new_note


def delete_note(note_id: int) -> bool:
    """Supprime une note par ID et renvoie True si elle a été supprimée."""
    notes = load_notes()
    updated_notes = [n for n in notes if n["id"] != note_id]
    if len(updated_notes) == len(notes):
        return False
    save_notes(updated_notes)
    return True
