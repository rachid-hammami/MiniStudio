
Write-Host "🚀 Démarrage des tests du Cortex Feedback Loop v1.6..." -ForegroundColor Cyan

# 1️⃣ Test: POST /cortex/feedback/log
Write-Host "`n🧩 Test 1 - Enregistrement d'un feedback" -ForegroundColor Yellow
$response1 = Invoke-RestMethod -Uri "http://127.0.0.1:8100/cortex/feedback/log" `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{
    "endpoint": "/cortex/analyze",
    "context": "fastapi_app/cortex/cortex_feedback.py",
    "status": "success",
    "patterns": ["test-pattern", "validation"],
    "correction_applied": true,
    "confidence_score": 0.9,
    "tags": ["[TEST]", "[AUTO]"]
  }'
$response1 | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green

# 2️⃣ Test: GET /cortex/feedback/stats
Write-Host "`n📊 Test 2 - Statistiques globales" -ForegroundColor Yellow
$response2 = Invoke-RestMethod -Uri "http://127.0.0.1:8100/cortex/feedback/stats" -Method GET
$response2 | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green

# 3️⃣ Test: GET /cortex/feedback/trends
Write-Host "`n📈 Test 3 - Tendances temporelles" -ForegroundColor Yellow
$response3 = Invoke-RestMethod -Uri "http://127.0.0.1:8100/cortex/feedback/trends" -Method GET
$response3 | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green

# 4️⃣ Test: GET /cortex/feedback/health
Write-Host "`n❤️ Test 4 - Santé cognitive" -ForegroundColor Yellow
$response4 = Invoke-RestMethod -Uri "http://127.0.0.1:8100/cortex/feedback/health" -Method GET
$response4 | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green

# 5️⃣ Test: DELETE /cortex/feedback/clear
Write-Host "`n🧹 Test 5 - Réinitialisation du feedback" -ForegroundColor Yellow
$response5 = Invoke-RestMethod -Uri "http://127.0.0.1:8100/cortex/feedback/clear" -Method DELETE
$response5 | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green

Write-Host "`n✅ Tous les tests du Cortex Feedback Loop ont été exécutés." -ForegroundColor Cyan
