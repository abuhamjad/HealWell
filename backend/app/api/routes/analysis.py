from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, Query
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
)
from app.services.analysis_service import AnalysisService
from app.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=ApiResponse)
async def create_analysis(
    request: AnalysisRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new health analysis from symptoms.

    Protected endpoint - requires JWT authentication.
    Analysis is automatically associated with the authenticated user.

    INTEGRATION FLOW:
    1. Validate authentication (dependency)
    2. Delegate to AnalysisService
    3. Service orchestrates AI analysis
    4. Service persists to database
    5. Return response with AI results and database info

    Never exposes:
    - User ID (client already knows theirs)
    - Internal AI prompts
    - Model configuration
    - Stack traces
    """
    # Initialize service with dependency-injected session
    analysis_service = AnalysisService(session=session)

    # Delegate to service layer
    # Service orchestrates: AI execution → Persistence → Response
    # Always use current_user.id - never trust client-supplied user_id
    output = await analysis_service.analyze(
        symptoms=request.symptoms,
        user_id=str(current_user.id),
    )

    # Use database-persisted analysis for response (if persisted)
    # Otherwise use AI result with placeholder timestamp
    analysis_id_for_response = str(output.analysis.id) if output.analysis else output.ai_result.analysis_id
    created_at_for_response = output.analysis.created_at if output.analysis else datetime.utcnow()

    # Convert to response format, combining AI results with database information
    analysis_data = AnalysisResponse(
        analysis_id=analysis_id_for_response,
        risk_level=output.ai_result.risk_assessment.risk_level,
        confidence=output.ai_result.risk_assessment.confidence,
        specialist=output.ai_result.specialist_recommendation.specialist,
        emergency=output.ai_result.emergency_alert,
        risk_assessment=output.ai_result.risk_assessment,
        specialist_recommendation=output.ai_result.specialist_recommendation,
        health_report=output.ai_result.health_report,
        emergency_message=output.ai_result.emergency_message,
        created_at=created_at_for_response,
    )
    return success_response(message=SUCCESS_ANALYSIS_CREATED, data=analysis_data)


@router.get("/history", response_model=ApiResponse)
async def get_analysis_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's analysis history, newest first.

    Protected endpoint - requires JWT authentication.
    Returns only the authenticated user's analyses.

    Supports pagination via limit and offset parameters.
    Returns summary data (no full JSON blobs) for efficient list display.

    Args:
        limit: Number of results to return (1-100, default 20).
        offset: Number of results to skip (default 0).
        current_user: Authenticated user (injected by dependency).

    Returns:
        Paginated list of authenticated user's analyses with summary information.
    """
    # Use authenticated user's ID - never trust client-supplied parameters
    user_id = current_user.id

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
    analysis_id: str,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get complete analysis details by ID.

    Protected endpoint - requires JWT authentication.
    Users can only access their own analyses.

    AUTHORIZATION: Enforced by service layer.
    Ownership check happens in AnalysisService.get_analysis_by_id().
    Routes must never duplicate authorization logic.

    Returns full analysis including all risk assessment, specialist
    recommendation, and health report data stored as JSON.

    Args:
        analysis_id: UUID of the analysis to retrieve.
        current_user: Authenticated user (injected by dependency).

    Returns:
        Complete analysis with all stored AI-generated data.

    Raises:
        AnalysisNotFoundError: If analysis not found or doesn't belong to user
        (caught by global handler → HTTP 404).
    """
    analysis_service = AnalysisService(session=session)

    # Service enforces ownership - raises exception if not found or not owned
    analysis = analysis_service.get_analysis_by_id(analysis_id, current_user.id)

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
