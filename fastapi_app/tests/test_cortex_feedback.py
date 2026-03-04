import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Import des modules CORTEX
from fastapi_app.cortex.cortex_feedback import CortexFeedback
from fastapi_app.cortex.cortex_feedback_service import router as feedback_router
from fastapi_app.cortex.cortex_memory import CortexMemory
from fastapi_app.docs.Cortex_History_Report import CortexReportGenerator

# ------------------------- Configuration de l'app FastAPI -------------------------
@pytest.fixture(scope="module")
def test_app():
    app = FastAPI()
    app.include_router(feedback_router)
    return app

@pytest.fixture(scope="module")
def client(test_app):
    return TestClient(test_app)

# ------------------------- Tests de base du Feedback Loop -------------------------
def test_feedback_log_and_stats(client):
    payload = {
        "endpoint": "/cortex/analyze",
        "context": "fastapi_app/endpoints/endpoints_cortex.py",
        "status": "success",
        "patterns": ["Dockerfile naming issue", "Empty file"],
        "correction_applied": True,
        "confidence_score": 0.95,
        "tags": ["[TEST]", "[UNIT]"]
    }

    response = client.post("/cortex/feedback/log", json=payload)
    assert response.status_code == 200

    stats = client.get("/cortex/feedback/stats")
    assert stats.status_code == 200
    data = stats.json()
    assert "avg_confidence" in data
    assert data["avg_confidence"] >= 0.9


def test_feedback_trends(client):
    response = client.get("/cortex/feedback/trends")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_cortex_memory_integration():
    cortex_mem = CortexMemory(memory_path="memory/memoire.json", feedback_path="memory/cortex_feedback.json")
    result = cortex_mem.integrate_feedback()
    assert "feedbacks intégrés" in result["message"]


def test_generate_report():
    report_gen = CortexReportGenerator(feedback_path="memory/cortex_feedback.json", report_path="docs/Cortex_History_Report.md")
    result = report_gen.generate_report()
    assert "Rapport généré avec succès" in result


def test_health_endpoint(client):
    response = client.get("/cortex/feedback/health")
    assert response.status_code == 200
    data = response.json()
    assert "health_score" in data
    assert 0 <= data["health_score"] <= 1


def test_clear_feedback(client):
    response = client.delete("/cortex/feedback/clear")
    assert response.status_code == 200
    assert "Feedback réinitialisé" in response.json()["message"]
