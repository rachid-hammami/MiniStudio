@echo off
echo 🚀 Restarting MiniStudio stack...
docker compose down
docker compose up -d
timeout /t 5 >nul
docker ps
echo ✅ Done! Containers are running.
pause
