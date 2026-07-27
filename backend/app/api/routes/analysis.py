from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisHistoryItem,
    AnalysisDetailResponse,
    AnalysisHistoryResponse,
)
from app.schemas.response import ApiResponse, success_response
from app.core.constants import (
    SUCCESS_ANALYSIS_CREATED,
    SUCCESS_HISTORY_RETRIEVED,
    PLACEHOLDER_USER_ID,
)
from app.services.analysis_service import AnalysisService
from app.database import get_db

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=ApiResponse)
async def create_analysis(request: AnalysisRequest, session: Session = Depends(get_db)):
    """
    Create a new health analysis from symptoms.

    Delegates to AnalysisService which orchestrates AI workflow and persists to database.
    """
    # Initialize service with dependency-injected session
    analysis_service = AnalysisService(session=session)

    # Delegate to service layer
    result = await analysis_service.analyze(
        symptoms=request.symptoms,
        user_id=request.user_id,
    )

    # Convert to response format, serializing the existing AI models as-is
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


@router.get("/history", response_model=ApiResponse)
async def get_analysis_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_db),
):
    """Get user's analysis history, newest first.

    Supports pagination via limit and offset parameters.
    Returns summary data (no full JSON blobs) for efficient list display.

    User context is currently injected from PLACEHOLDER_USER_ID.
    Once JWT authentication is implemented, replace the injected value
    with current_user.id from the authenticated token.

    Args:
        limit: Number of results to return (1-100, default 20).
        offset: Number of results to skip (default 0).

    Returns:
        Paginated list of analyses with summary information.
    """
    # TODO: Replace with current_user.id from JWT token once authentication is implemented
    # For now, use placeholder UUID for all unauthenticated requests
    user_id = UUID(PLACEHOLDER_USER_ID)

    analysis_service = AnalysisService(session=session)

    history = analysis_service.get_history(
        user_id=user_id,
        limit=limit,
        offset=offset,
    )

    # Convert Analysis model instances to AnalysisHistoryItem schema
    history_items = [
        AnalysisHistoryItem(
            analysis_id=str(item.id),
            created_at=item.created_at,
            risk_level=item.risk_level,
            confidence=item.confidence,
            specialist=item.specialist,
            emergency=item.emergency,
        )
        for item in history["items"]
    ]

    history_response = AnalysisHistoryResponse(
        items=history_items,
        total=history["total"],
        limit=history["limit"],
        offset=history["offset"],
    )

    return success_response(
        message=SUCCESS_HISTORY_RETRIEVED, data=history_response
    )


@router.get("/{analysis_id}", response_model=ApiResponse)
async def get_analysis_detail(
    analysis_id: str, session: Session = Depends(get_db)
):
    """Get complete analysis details by ID.

    Returns full analysis including all risk assessment, specialist
    recommendation, and health report data stored as JSON.

    Args:
        analysis_id: UUID of the analysis to retrieve.

    Returns:
        Complete analysis with all stored AI-generated data.

    Raises:
        HTTPException: 404 if analysis not found.
    """
    analysis_service = AnalysisService(session=session)

    analysis = analysis_service.get_analysis_by_id(analysis_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    # Convert Analysis model instance to AnalysisDetailResponse schema
    analysis_detail = AnalysisDetailResponse(
        analysis_id=str(analysis.id),
        created_at=analysis.created_at,
        risk_level=analysis.risk_level,
        confidence=analysis.confidence,
        specialist=analysis.specialist,
        emergency=analysis.emergency,
        risk_assessment=analysis.risk_assessment,
        specialist_recommendation=analysis.specialist_recommendation,
        health_report=analysis.health_report,
    )

    return success_response(
        message=SUCCESS_HISTORY_RETRIEVED, data=analysis_detail
    )
