from fastapi import APIRouter
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
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

    # Convert to response format with all AI-generated content
    analysis_data = AnalysisResponse(
        analysis_id=result.analysis_id,
        risk_level=result.risk_assessment.risk_level,
        confidence=result.risk_assessment.confidence,
        confidence_explanation=result.risk_assessment.confidence_explanation,
        risk_explanation=result.risk_assessment.risk_explanation,
        specialist=result.specialist_recommendation.specialist,
        specialist_explanation=result.specialist_recommendation.specialist_explanation,
        emergency=result.emergency_alert,
        emergency_instructions=result.health_report.emergency_instructions,
        summary_explanation=result.health_report.summary_explanation,
        personalized_home_care=result.health_report.personalized_home_care,
        personalized_lifestyle=result.health_report.personalized_lifestyle,
        monitoring_guidance=result.health_report.monitoring_guidance,
    ).model_dump()
    return success_response(message=SUCCESS_ANALYSIS_CREATED, data=analysis_data)
