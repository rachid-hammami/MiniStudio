# fastapi_app/database.py
# ==============================================================
# Gestion de la base SQLite utilisée par l'IA proactive
# ==============================================================

import sqlite3
import os

DB_PATH = "memory/studio.db"


def get_db_connection():
    """
    Retourne une connexion SQLite configurée avec row_factory dict.
    Crée les tables si elles n'existent pas.
    """
    os.makedirs("memory", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("""
    CREATE TABLE IF NOT EXISTS ai_suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file TEXT,
        line INTEGER,
        type TEXT,
        message TEXT,
        suggestion TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS ai_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suggestion_id INTEGER,
        action TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    return conn
