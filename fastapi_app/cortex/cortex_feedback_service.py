from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from fastapi_app.cortex.cortex_feedback import CortexFeedback

router = APIRouter(prefix="/cortex/feedback", tags=["Cortex Feedback"])

# ------------------------- Models -------------------------
class FeedbackEvent(BaseModel):
    endpoint: str
    context: str
    status: str
    patterns: List[str]
    correction_applied: bool
    confidence_score: float
    tags: Optional[List[str]] = []

# ------------------------- Core -------------------------
cortex_feedback = CortexFeedback(memory_path="memory/cortex_feedback.json")

# ------------------------- Endpoints -------------------------
@router.post("/log")
def log_feedback(event: FeedbackEvent):
    try:
        result = cortex_feedback.log_event(
            endpoint=event.endpoint,
            context=event.context,
            status=event.status,
            patterns=event.patterns,
            correction_applied=event.correction_applied,
            confidence_score=event.confidence_score,
            tags=event.tags
        )
        return JSONResponse(content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement du feedback : {str(e)}")


@router.get("/stats")
def get_feedback_stats():
    try:
        stats = cortex_feedback.get_stats()
        return JSONResponse(content=jsonable_encoder(stats))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des statistiques : {str(e)}")


@router.get("/trends")
def get_feedback_trends():
    try:
        trends = cortex_feedback.get_trends()
        return JSONResponse(content=jsonable_encoder(trends))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des tendances : {str(e)}")


@router.get("/health")
def get_cortex_health():
    try:
        stats = cortex_feedback.get_stats()
        health_score = round((stats.get("avg_confidence", 0) + (stats.get("improvement_rate", 0) / 100)) / 2, 3)
        response = {
            "status": "ok" if health_score > 0.5 else "degraded",
            "health_score": health_score,
            "timestamp": cortex_feedback.feedback_data.get("timestamp"),
            "summary": stats
        }
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'évaluation de la santé cognitive : {str(e)}")


@router.delete("/clear")
def clear_feedback_data():
    try:
        cortex_feedback.clear_feedback()
        return {"message": "Feedback réinitialisé avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la réinitialisation du feedback : {str(e)}")


# ------------------------- Intégration -------------------------
# Ce routeur doit être inclus dans fastapi_app/main.py :
# app.include_router(fastapi_app.cortex.cortex_feedback_service.router)
