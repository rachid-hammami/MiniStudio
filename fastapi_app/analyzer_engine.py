import sqlite3
import json
from datetime import datetime
from pathlib import Path


class AnalyzerOrchestrator:
    """
    Moteur central MiniStudio (étape 5.5)
    - Collecte les données (logs, reports, backups)
    - Génère des signaux
    - Crée un rapport consolidé
    """

    def __init__(self, db_path: str = "memory/studio.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        """Crée la base et les tables si elles n'existent pas."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            filename TEXT,
            user TEXT,
            status TEXT
        );
        """
        )
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file TEXT,
            analysis TEXT,
            test_results TEXT,
            created_at TEXT
        );
        """
        )
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_file TEXT,
            backup_file TEXT,
            timestamp TEXT
        );
        """
        )
        conn.commit()
        conn.close()

    def collect_data(self) -> dict:
        """Récupère les données depuis SQLite."""
        try:
            conn = self._connect()
            cur = conn.cursor()
            logs = cur.execute("SELECT * FROM logs ORDER BY timestamp DESC").fetchall()
            reports = cur.execute(
                "SELECT * FROM reports ORDER BY created_at DESC"
            ).fetchall()
            backups = cur.execute(
                "SELECT * FROM backups ORDER BY timestamp DESC"
            ).fetchall()
            conn.close()
            return {"logs": logs, "reports": reports, "backups": backups}
        except Exception as e:
            return {"error": str(e)}

    def generate_signals(self, data: dict) -> list:
        """Analyse les données et génère des signaux internes."""
        signals = []
        if "error" in data:
            return [{"type": "system_error", "message": data["error"]}]

        for log in data.get("logs", []):
            log_id, timestamp, action, filename, user, status = log
            if status and ("error" in status.lower() or "fail" in status.lower()):
                signals.append(
                    {
                        "type": "error_detected",
                        "file": filename,
                        "message": f"Erreur détectée ({status})",
                        "timestamp": timestamp,
                    }
                )

        for rep in data.get("reports", []):
            _, file, analysis, test_results, created_at = rep
            if test_results and "failed" in test_results.lower():
                signals.append(
                    {
                        "type": "test_failure",
                        "file": file,
                        "message": "Échec détecté dans les tests",
                        "timestamp": created_at,
                    }
                )
        return signals

    def consolidate_reports(self, data: dict, signals: list) -> dict:
        """Crée un rapport global consolidé et le stocke en base."""
        summary = {
            "total_logs": len(data.get("logs", [])),
            "total_reports": len(data.get("reports", [])),
            "total_backups": len(data.get("backups", [])),
            "total_signals": len(signals),
        }

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "signals": signals,
        }

        try:
            conn = self._connect()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO reports (file, analysis, test_results, created_at)
                VALUES (?, ?, ?, ?)
            """,
                ("__consolidated__", json.dumps(report), None, report["timestamp"]),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            report["db_error"] = str(e)

        return report
