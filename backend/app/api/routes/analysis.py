from fastapi import APIRouter
from app.schemas.analysis import AnalysisRequest, AnalysisResponse

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalysisResponse)
async def create_analysis(request: AnalysisRequest):
    """
    Create a new health analysis from symptoms.

    Placeholder endpoint - returns mock data.
    """
    return {
        "analysis_id": "analysis_001",
        "risk_level": "moderate",
        "confidence": 87.5,
        "specialist": "General Practitioner",
        "emergency": False,
        "status": "success"
    }
