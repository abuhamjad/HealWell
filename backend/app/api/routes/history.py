from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.history import HistorySaveRequest
from app.schemas.response import ApiResponse, success_response
from app.core.constants import (
    SUCCESS_HISTORY_RETRIEVED,
    SUCCESS_HISTORY_SAVED,
    DEFAULT_HISTORY_LIMIT
)
from app.services.history_service import HistoryService
from app.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/history", tags=["history"])
history_service = HistoryService()


@router.get("", response_model=ApiResponse)
async def get_history(
    limit: int = DEFAULT_HISTORY_LIMIT,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve current user's analysis history.

    Protected endpoint - requires JWT authentication.
    Returns only the authenticated user's history.

    Delegates to HistoryService.
    """
    # Delegate to service layer with authenticated user's ID
    # Never trust client-supplied user_id parameter
    history_data = await history_service.get_user_history(str(current_user.id))

    # Mock return for now - will integrate with database
    history_data = {
        "analyses": [
            {
                "id": "analysis_001",
                "user_id": str(current_user.id),
                "date": "2026-07-18",
                "symptoms": "Headache with light sensitivity",
                "risk_level": "moderate",
                "specialist": "Neurologist"
            }
        ],
        "count": 1
    }
    return success_response(message=SUCCESS_HISTORY_RETRIEVED, data=history_data)


@router.post("", response_model=ApiResponse)
async def save_history(
    request: HistorySaveRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Save or update authenticated user's medical history.

    Protected endpoint - requires JWT authentication.
    Users can only update their own medical history.

    Delegates to HistoryService.
    """
    # Delegate to service layer with authenticated user's ID
    # Always use current_user.id - never trust client-supplied user_id
    result = await history_service.save_history(
        user_id=str(current_user.id),
        conditions=request.conditions,
        medications=request.medications,
        allergies=request.allergies,
    )

    history_data = {
        "history_id": "history_001",
        "user_id": str(current_user.id),
        "saved_at": "2026-07-20T10:30:00Z"
    }
    return success_response(message=SUCCESS_HISTORY_SAVED, data=history_data)
