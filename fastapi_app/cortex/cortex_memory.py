import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class CortexMemory:
    """
    Module : cortex_memory.py
    Rôle : Gérer la mémoire persistante du CORTEX et y intégrer les événements de feedback vectorisés.
    Fichier à placer dans : fastapi_app/cortex/cortex_memory.py
    """

    def __init__(self, memory_path: str = "memory/memoire.json", feedback_path: str = "memory/cortex_feedback.json"):
        self.memory_path = memory_path
        self.feedback_path = feedback_path
        self.memory_data = self._load_memory()
        self.feedback_data = self._load_feedback()

    # ------------------------- Chargement / Sauvegarde -------------------------
    def _load_memory(self) -> Dict[str, Any]:
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"sessions": [], "knowledge_vectors": [], "last_update": None}

    def _load_feedback(self) -> Dict[str, Any]:
        if os.path.exists(self.feedback_path):
            with open(self.feedback_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"feedback_events": []}

    def _save_memory(self):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        self.memory_data["last_update"] = datetime.utcnow().isoformat() + "Z"
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory_data, f, indent=4, ensure_ascii=False)

    # ------------------------- Intégration des Feedbacks -------------------------
    def integrate_feedback(self):
        feedback_events = self.feedback_data.get("feedback_events", [])
        if not feedback_events:
            return {"message": "Aucun feedback à intégrer."}

        for event in feedback_events:
            vector_entry = self._vectorize_feedback(event)
            self.memory_data["knowledge_vectors"].append(vector_entry)

        self._save_memory()
        return {"message": f"{len(feedback_events)} feedbacks intégrés à la mémoire."}

    def _vectorize_feedback(self, event: Dict[str, Any]) -> Dict[str, Any]:
        # Simulation de vectorisation sémantique (préparation FAISS/Chroma pour v1.7)
        vector_representation = {
            "endpoint": event.get("endpoint"),
            "patterns": event.get("patterns_detected", []),
            "confidence_score": event.get("confidence_score", 0),
            "timestamp": event.get("timestamp"),
            "vector": [round(hash(p) % 1000 / 1000, 3) for p in event.get("patterns_detected", [])]
        }
        return vector_representation

    # ------------------------- Requêtes sémantiques -------------------------
    def query_memory(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        for entry in self.memory_data.get("knowledge_vectors", []):
            if any(keyword.lower() in p.lower() for p in entry.get("patterns", [])):
                results.append(entry)
        return results

    # ------------------------- Nettoyage -------------------------
    def clear_memory(self):
        self.memory_data = {"sessions": [], "knowledge_vectors": [], "last_update": None}
        self._save_memory()


# ------------------------- Exécution locale (debug/test) -------------------------
if __name__ == "__main__":
    cortex_mem = CortexMemory(memory_path="fastapi_app/memory/memoire.json", feedback_path="fastapi_app/memory/cortex_feedback.json")
    print(cortex_mem.integrate_feedback())
    print(cortex_mem.query_memory("docker"))
