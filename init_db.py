import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
import os

# --- Définition de la base ---
Base = declarative_base()
DB_PATH = "memory/studio.db"
os.makedirs("memory", exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# --- Table principale des actions (déjà utilisée par FastAPI) ---
class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action_type = Column(String(50), nullable=False)
    details = Column(Text, nullable=True)

# --- Table des logs ---
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String(100))
    filename = Column(String(200))
    user = Column(String(100))
    status = Column(String(200))

# --- Table des rapports ---
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    file = Column(String(200))
    analysis = Column(Text)
    test_results = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Table des sauvegardes ---
class Backup(Base):
    __tablename__ = "backups"
    id = Column(Integer, primary_key=True)
    file = Column(String(200))
    timestamp = Column(DateTime, default=datetime.utcnow)
    checksum = Column(String(64))

# --- Création effective de la base ---
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Base SQLite initialisée avec tables : actions, logs, reports, backups")
