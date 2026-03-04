"""
Module : report_generator.py
Emplacement : fastapi_app/cortex/
Objectif : Génère automatiquement les rapports cognitifs du CORTEX.

───────────────────────────────
🧭 Guide interne (Développeurs)
───────────────────────────────
- Génération manuelle :
    from fastapi_app.cortex.report_generator import CortexReportGenerator
    generator = CortexReportGenerator()
    generator.generate_all_reports()

- Emplacement des rapports :
    /reports/Cortex_History_Report.md
    /reports/Cortex_Feedback_Stats.md

- Utilisation CI/CD :
    Automatiquement déclenchée par .github/workflows/cortex_feedback.yml

───────────────────────────────
"""

import json
from datetime import datetime
from pathlib import Path

class CortexReportGenerator:
    def __init__(self, feedback_path: str = "memory/cortex_feedback.json", reports_root: str = "reports"):
        self.feedback_path = Path(feedback_path)
        self.reports_root = Path(reports_root)
        self.history_report = self.reports_root / "Cortex_History_Report.md"
        self.stats_report = self.reports_root / "Cortex_Feedback_Stats.md"
        self.feedback_data = self._load_feedback()

    # ------------------------- Chargement -------------------------
    def _load_feedback(self):
        if not self.feedback_path.exists():
            return {"feedback_events": [], "patterns_summary": {}}
        with open(self.feedback_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # ------------------------- Génération du rapport principal -------------------------
    def generate_history_report(self):
        feedback_events = self.feedback_data.get("feedback_events", [])
        summary = self.feedback_data.get("patterns_summary", {})

        header = f"""# 🧠 Cortex History Report
**Généré le :** {datetime.utcnow().isoformat()}Z
**Total d'événements :** {len(feedback_events)}

---

## 📊 Résumé Cognitif
- **Taux d'amélioration global :** {summary.get('improvement_rate', 0)}%
- **Score de confiance moyen :** {summary.get('avg_confidence', 0)}
- **Problèmes récurrents :** {', '.join(summary.get('recurring_issues', [])) or 'Aucun'}

---

## 🧩 Détails des Événements
"""

        event_lines = []
        for ev in feedback_events[-20:]:  # derniers 20 événements
            event_lines.append(f"### ➤ {ev.get('endpoint')}")
            event_lines.append(f"- **Contexte :** {ev.get('context')}")
            event_lines.append(f"- **Statut :** {ev.get('status')}")
            event_lines.append(f"- **Correction appliquée :** {ev.get('correction_applied')}")
            event_lines.append(f"- **Score de confiance :** {ev.get('confidence_score')}")
            event_lines.append(f"- **Patterns détectés :** {', '.join(ev.get('patterns_detected', []))}")
            event_lines.append(f"- **Tags :** {', '.join(ev.get('tags', []))}")
            event_lines.append(f"- **Horodatage :** {ev.get('timestamp')}\n")

        self.reports_root.mkdir(parents=True, exist_ok=True)
        with open(self.history_report, 'w', encoding='utf-8') as f:
            f.write(header + "\n".join(event_lines))

        return f"Rapport historique généré avec succès : {self.history_report}"

    # ------------------------- Génération du rapport de statistiques -------------------------
    def generate_stats_report(self):
        summary = self.feedback_data.get("patterns_summary", {})
        avg_conf = summary.get("avg_confidence", 0)
        improv = summary.get("improvement_rate", 0)
        recurring = summary.get("recurring_issues", [])

        stats_content = f"""# 📈 Cortex Feedback Stats
**Généré le :** {datetime.utcnow().isoformat()}Z

| Indicateur | Valeur |
|-------------|--------|
| Taux d'amélioration | {improv}% |
| Score de confiance moyen | {avg_conf} |
| Nombre de patterns récurrents | {len(recurring)} |

---

## 🔁 Patterns Récurrents
{chr(10).join(['- ' + r for r in recurring]) if recurring else 'Aucun pattern détecté.'}
"""

        self.reports_root.mkdir(parents=True, exist_ok=True)
        with open(self.stats_report, 'w', encoding='utf-8') as f:
            f.write(stats_content)

        return f"Rapport de statistiques généré avec succès : {self.stats_report}"

    # ------------------------- Génération complète -------------------------
    def generate_all_reports(self):
        res1 = self.generate_history_report()
        res2 = self.generate_stats_report()
        return f"{res1}\n{res2}"


if __name__ == "__main__":
    report_gen = CortexReportGenerator(
        feedback_path="memory/cortex_feedback.json",
        reports_root="reports"
    )
    print(report_gen.generate_all_reports())