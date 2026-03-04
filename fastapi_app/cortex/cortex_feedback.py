import json
import os
from datetime import datetime
from typing import List, Dict, Any


class CortexFeedback:
    """
    Module central du CORTEX Feedback Loop.
    Gère la collecte, l'analyse et la mise à jour des événements de feedback.
    Fichier à placer dans : fastapi_app/cortex/cortex_feedback.py
    """

    def __init__(self, memory_path: str = "memory/cortex_feedback.json"):
        self.memory_path = memory_path
        self.feedback_data = self._load_feedback()

    # ------------------------- Chargement & Sauvegarde -------------------------
    def _load_feedback(self) -> Dict[str, Any]:
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "version": "1.6",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "feedback_events": [],
            "patterns_summary": {
                "recurring_issues": [],
                "improvement_rate": 0.0,
                "avg_confidence": 0.0
            }
        }

    def _save_feedback(self):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        self.feedback_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.feedback_data, f, indent=4, ensure_ascii=False)

    # ------------------------- Journalisation d'événements -------------------------
    def log_event(self, endpoint: str, context: str, status: str, patterns: List[str],
                  correction_applied: bool, confidence_score: float, tags: List[str] = None):
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "endpoint": endpoint,
            "context": context,
            "status": status,
            "patterns_detected": patterns,
            "correction_applied": correction_applied,
            "confidence_score": confidence_score,
            "tags": tags or []
        }
        self.feedback_data["feedback_events"].append(event)
        self._update_summary()
        self._save_feedback()
        return event

    # ------------------------- Analyse & Résumé -------------------------
    def _update_summary(self):
        events = self.feedback_data["feedback_events"]
        if not events:
            return

        recurring = {}
        confidence_sum = 0.0

        for ev in events:
            confidence_sum += ev.get("confidence_score", 0)
            for pattern in ev.get("patterns_detected", []):
                recurring[pattern] = recurring.get(pattern, 0) + 1

        recurring_sorted = sorted(recurring, key=recurring.get, reverse=True)
        avg_conf = confidence_sum / len(events)

        improvement_rate = self._calculate_improvement_rate(events)

        self.feedback_data["patterns_summary"] = {
            "recurring_issues": recurring_sorted[:10],
            "improvement_rate": improvement_rate,
            "avg_confidence": round(avg_conf, 3)
        }

    def _calculate_improvement_rate(self, events: List[Dict[str, Any]]) -> float:
        success = sum(1 for e in events if e.get("status") == "success" and e.get("correction_applied"))
        total = len(events)
        if total == 0:
            return 0.0
        return round((success / total) * 100, 2)

    # ------------------------- Lecture publique -------------------------
    def get_stats(self) -> Dict[str, Any]:
        return self.feedback_data.get("patterns_summary", {})

    def get_trends(self) -> Dict[str, Any]:
        events = self.feedback_data.get("feedback_events", [])
        trends = {}
        for e in events:
            day = e["timestamp"].split("T")[0]
            trends[day] = trends.get(day, 0) + 1
        return trends

    def clear_feedback(self):
        self.feedback_data = self._load_feedback()
        self._save_feedback()


# ------------------------- Exécution locale (debug/test) -------------------------
if __name__ == "__main__":
    cortex = CortexFeedback(memory_path="fastapi_app/memory/cortex_feedback.json")
    cortex.log_event(
        endpoint="/cortex/analyze",
        context="fastapi_app/endpoints/endpoints_cortex.py",
        status="success",
        patterns=["Docker naming issue", "Empty file"],
        correction_applied=True,
        confidence_score=0.91,
        tags=["[FEEDBACK]", "[LEARNING]"]
    )
    print(json.dumps(cortex.get_stats(), indent=4, ensure_ascii=False))
