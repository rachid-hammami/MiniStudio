from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .analyzer_engine import AnalyzerOrchestrator

router = APIRouter()

@router.post("/generate-report")
def generate_report():
    """
    Endpoint principal de l'étape 5.5.
    Lance la collecte et la consolidation d'un rapport global.
    """
    orchestrator = AnalyzerOrchestrator("memory/studio.db")
    data = orchestrator.collect_data()
    signals = orchestrator.generate_signals(data)
    report = orchestrator.consolidate_reports(data, signals)
    return JSONResponse(content={"status": "ok", "report": report})
