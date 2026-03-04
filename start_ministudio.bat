@echo off
:: ===============================================================
:: 🚀 MiniStudio Launcher — Docker + Ngrok
:: Auteur : Code GPT
:: Objectif : Démarrer automatiquement MiniStudio et exposer son API
:: ===============================================================

:: Aller dans le dossier du projet MiniStudio
cd /d "C:\Users\Dell\Documents\Developpement\GitHub\MiniStudio"

echo.
echo ==========================================================
echo 🧩 LANCEMENT DE MINISTUDIO - Docker + Ngrok
echo ==========================================================
echo.

:: Vérifier que Docker est installé et actif
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR : Docker n'est pas installé ou non détecté dans le PATH.
    echo Veuillez installer Docker Desktop avant de continuer.
    pause
    exit /b
)

:: Vérifier si le démon Docker tourne
docker info >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Docker Desktop n'est pas encore lancé.
    echo Merci de le démarrer, puis relancer ce script.
    pause
    exit /b
)

:: Étape 1 — Lancer MiniStudio dans Docker
echo 🐳 Démarrage du conteneur Docker "ministudio"...
start cmd /k "docker-compose up"

:: Attendre 10 secondes que le serveur FastAPI démarre
echo 🕐 Attente de 10 secondes le temps que le serveur démarre...
timeout /t 10 /nobreak >nul

:: Étape 2 — Lancer Ngrok sur le port 8888
echo 🌐 Lancement du tunnel Ngrok vers MiniStudio...
start cmd /k "ngrok http 8888"

:: Étape 3 — Instructions finales
echo.
echo ==========================================================
echo ✅ MiniStudio est en cours d'exécution.
echo - Accès local  : http://localhost:8888/docs
echo - Accès distant: (voir URL affichée par Ngrok)
echo ==========================================================
echo.

pause
exit
