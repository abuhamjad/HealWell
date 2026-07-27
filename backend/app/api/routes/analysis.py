from fastapi import APIRouter
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
)
from app.schemas.response import ApiResponse, success_response
from app.core.constants import SUCCESS_ANALYSIS_CREATED
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=ApiResponse)
async def create_analysis(request: AnalysisRequest):
    """Create a new health analysis from symptoms.

    Executes AI workflow and returns analysis result.
    """
    analysis_service = AnalysisService()
    result = await analysis_service.analyze(symptoms=request.symptoms)

    analysis_data = AnalysisResponse(
        analysis_id=result.analysis_id,
        risk_level=result.risk_assessment.risk_level,
        confidence=result.risk_assessment.confidence,
        specialist=result.specialist_recommendation.specialist,
        emergency=result.emergency_alert,
        risk_assessment=result.risk_assessment,
        specialist_recommendation=result.specialist_recommendation,
        health_report=result.health_report,
        emergency_message=result.emergency_message,
    )
    return success_response(message=SUCCESS_ANALYSIS_CREATED, data=analysis_data)

