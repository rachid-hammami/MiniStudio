"""
MiniStudio System Orchestrator
==============================
Démarre, arrête ou redémarre tous les services :
- FastAPI (via uvicorn)
- ngrok (tunnel public)
- Gestion simple depuis VS Code ou console
"""

import subprocess
import psutil
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def run_command(cmd: list[str], title: str):
    """Exécute une commande dans une nouvelle console Windows."""
    print(f"🟢 Lancement de {title}...")
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=BASE_DIR)


def stop_process(name: str):
    """Arrête tous les processus contenant le nom donné."""
    print(f"🛑 Arrêt de {name}...")
    for proc in psutil.process_iter(["pid", "name"]):
        if name.lower() in proc.info["name"].lower():
            try:
                proc.terminate()
                print(f"   → PID {proc.pid} arrêté ({proc.info['name']}).")
            except Exception:
                pass


def start_all():
    """Démarre FastAPI + ngrok."""
    python_exe = sys.executable

    # 1️⃣ FastAPI (port 8888)
    run_command(
        [
            python_exe,
            "-m",
            "uvicorn",
            "fastapi_app.main:app",
            "--reload",
            "--port",
            "8888",
        ],
        "FastAPI",
    )

    # 2️⃣ ngrok
    run_command(["ngrok", "http", "8888"], "ngrok")

    print("\n🚀 MiniStudio est lancé !")
    print("   🌐 Dashboard : http://localhost:8888/dashboard")
    print("   ⚙️  Panneau : http://localhost:8888/control")
    print("   🧠 ngrok UI : http://127.0.0.1:4040\n")


def stop_all():
    """Arrête FastAPI + ngrok."""
    stop_process("uvicorn")
    stop_process("ngrok")
    print("\n🛑 Tous les services MiniStudio ont été arrêtés.\n")


def restart_all():
    stop_all()
    start_all()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Utilisation : python fastapi_app/system_orchestrator.py [start|stop|restart]"
        )
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "start":
        start_all()
    elif command == "stop":
        stop_all()
    elif command == "restart":
        restart_all()
    else:
        print("Commande inconnue. Utilisez : start / stop / restart.")
