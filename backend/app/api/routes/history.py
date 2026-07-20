from fastapi import APIRouter
from app.schemas.history import HistorySaveRequest
from app.schemas.response import ApiResponse, success_response
from app.core.constants import (
    SUCCESS_HISTORY_RETRIEVED,
    SUCCESS_HISTORY_SAVED,
    DEFAULT_HISTORY_LIMIT
)
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["history"])
history_service = HistoryService()


@router.get("", response_model=ApiResponse)
async def get_history(user_id: str = None, limit: int = DEFAULT_HISTORY_LIMIT):
    """
    Retrieve user's analysis history.

    Delegates to HistoryService.
    """
    # Delegate to service layer
    history_data = await history_service.get_user_history(user_id or "user_default")

    # Mock return for now - will integrate with database
    history_data = {
        "analyses": [
            {
                "id": "analysis_001",
                "user_id": user_id or "user_123",
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
async def save_history(request: HistorySaveRequest):
    """
    Save or update user medical history.

    Delegates to HistoryService.
    """
    # Delegate to service layer
    result = await history_service.save_history(
        user_id=request.user_id,
        conditions=request.conditions,
        medications=request.medications,
        allergies=request.allergies,
    )

    history_data = {
        "history_id": "history_001",
        "user_id": request.user_id,
        "saved_at": "2026-07-20T10:30:00Z"
    }
    return success_response(message=SUCCESS_HISTORY_SAVED, data=history_data)
