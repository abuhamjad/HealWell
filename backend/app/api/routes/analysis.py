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

    risk_assessment = result.risk_assessment
    specialist_recommendation = result.specialist_recommendation
    health_report = result.health_report

    analysis_data = AnalysisResponse(
        analysis_id=result.analysis_id,
        risk_level=risk_assessment.risk_level if risk_assessment else "MODERATE",
        confidence=risk_assessment.confidence if risk_assessment else 0.5,
        reasoning=risk_assessment.reasoning if risk_assessment else "Assessment completed.",
        specialist=specialist_recommendation.specialist if specialist_recommendation else "General Practitioner",
        specialist_explanation=specialist_recommendation.specialist_explanation if specialist_recommendation else "Evaluation recommended.",
        emergency=result.emergency_alert or (risk_assessment.emergency_alert if risk_assessment else False),
        needs_followup=getattr(risk_assessment, 'needs_followup', False) if risk_assessment else False,
        instructions=(risk_assessment.instructions if risk_assessment else None) or (health_report.emergency_instructions if health_report else None),
        provider_used=result.provider_used or (risk_assessment.provider_used if risk_assessment else "mock"),
        summary_explanation=health_report.summary_explanation if health_report else "Health evaluation summary.",
        personalized_home_care=health_report.personalized_home_care if health_report else [],
        personalized_lifestyle=health_report.personalized_lifestyle if health_report else [],
        monitoring_guidance=health_report.monitoring_guidance if health_report else [],
    ).model_dump()
    return success_response(message=SUCCESS_ANALYSIS_CREATED, data=analysis_data)
