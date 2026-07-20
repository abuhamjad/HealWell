from fastapi import APIRouter
from app.schemas.analysis import AnalysisRequest
from app.schemas.response import ApiResponse, success_response
from app.core.constants import SUCCESS_ANALYSIS_CREATED
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])
analysis_service = AnalysisService()


@router.post("", response_model=ApiResponse)
async def create_analysis(request: AnalysisRequest):
    """
    Create a new health analysis from symptoms.

    Delegates to AnalysisService which orchestrates AI workflow.
    """
    # Delegate to service layer
    result = await analysis_service.analyze(
        symptoms=request.symptoms,
        user_id=request.user_id,
    )

    # Convert to response format
    analysis_data = {
        "analysis_id": result.analysis_id,
        "risk_level": result.risk_assessment.risk_level,
        "confidence": result.risk_assessment.confidence,
        "specialist": result.specialist_recommendation.specialist,
        "emergency": result.emergency_alert
    }
    return success_response(message=SUCCESS_ANALYSIS_CREATED, data=analysis_data)
