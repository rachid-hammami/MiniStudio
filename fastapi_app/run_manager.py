import os
import subprocess
import sys
import psutil


def stop_fastapi():
    for proc in psutil.process_iter(["pid", "name"]):
        if "uvicorn" in proc.info["name"].lower():
            proc.terminate()
    print("✅ FastAPI arrêté.")


def start_fastapi():
    python_exe = sys.executable
    subprocess.Popen(
        [
            python_exe,
            "-m",
            "uvicorn",
            "fastapi_app.main:app",
            "--reload",
            "--port",
            "8888",
        ]
    )
    print("🚀 FastAPI démarré.")


def restart_fastapi():
    stop_fastapi()
    start_fastapi()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "restart"
    if cmd == "start":
        start_fastapi()
    elif cmd == "stop":
        stop_fastapi()
    else:
        restart_fastapi()
