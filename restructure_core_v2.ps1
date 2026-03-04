# ============================================================
# MiniStudio - Script de restructuration Core (Version 2)
# Objectif : Déplacer les modules vitaux vers fastapi_app/core/
#            et corriger automatiquement les imports.
# ============================================================

$projectRoot = Get-Location
$coreDir = Join-Path $projectRoot "fastapi_app\core"
$memoryDir = Join-Path $projectRoot "memory"
$reportFile = Join-Path $memoryDir "restructure_core_report_v2.txt"

# Création des dossiers si besoin
if (-not (Test-Path $coreDir)) { New-Item -ItemType Directory -Path $coreDir | Out-Null }
if (-not (Test-Path $memoryDir)) { New-Item -ItemType Directory -Path $memoryDir | Out-Null }

$coreFiles = @("builder_core.py", "controller_collab.py", "check_docker_health.py")

"MiniStudio - Rapport de restructuration Core (v2)" | Out-File $reportFile -Encoding UTF8
"Date : $(Get-Date)" | Out-File $reportFile -Append
"Projet : $projectRoot" | Out-File $reportFile -Append
"------------------------------------------------------------" | Out-File $reportFile -Append

# Étape 1 : Recherche et déplacement global
foreach ($file in $coreFiles) {
    $found = Get-ChildItem -Path $projectRoot -Recurse -Filter $file -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $dest = Join-Path $coreDir $file
        Move-Item $found.FullName $dest -Force
        "[MOVED] $file -> fastapi_app/core/" | Out-File $reportFile -Append
    } else {
        "[NOT FOUND] $file" | Out-File $reportFile -Append
    }
}

"------------------------------------------------------------" | Out-File $reportFile -Append
"Step 2: scanning and updating imports..." | Out-File $reportFile -Append

$pattern = '^(from|import)\s+(builder_core|controller_collab|check_docker_health)'
$filesToCheck = Get-ChildItem -Path "$projectRoot" -Recurse -Include *.py

foreach ($file in $filesToCheck) {
    $content = Get-Content $file.FullName
    $modified = $false

    # Sauvegarde avant modification
    $backup = "$($file.FullName).bak"
    Copy-Item $file.FullName $backup -Force

    $newContent = @()
    foreach ($line in $content) {
        if ($line -match $pattern) {
            $modified = $true
            $originalLine = $line

            $line = $line -replace 'from\s+builder_core', 'from fastapi_app.core.builder_core'
            $line = $line -replace 'from\s+controller_collab', 'from fastapi_app.core.controller_collab'
            $line = $line -replace 'from\s+check_docker_health', 'from fastapi_app.core.check_docker_health'
            $line = $line -replace 'import\s+builder_core', 'from fastapi_app.core import builder_core'
            $line = $line -replace 'import\s+controller_collab', 'from fastapi_app.core import controller_collab'
            $line = $line -replace 'import\s+check_docker_health', 'from fastapi_app.core import check_docker_health'

            "[MODIFIED] $($file.FullName)" | Out-File $reportFile -Append
            "   OLD: $originalLine" | Out-File $reportFile -Append
            "   NEW: $line" | Out-File $reportFile -Append
        }
        $newContent += $line
    }

    if ($modified) {
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
    } else {
        "[UNCHANGED] $($file.FullName)" | Out-File $reportFile -Append
    }
}

"------------------------------------------------------------" | Out-File $reportFile -Append
"Script finished successfully." | Out-File $reportFile -Append
"Report generated: $reportFile" | Out-File $reportFile -Append
"============================================================" | Out-File $reportFile -Append

Write-Host ""
Write-Host "Restructuration terminée avec succès (v2)."
Write-Host "Rapport généré : $reportFile"
Write-Host "Fichiers déplacés dans : fastapi_app/core/"
