from fastapi import APIRouter
from app.schemas.history import HistoryResponse, HistorySaveRequest

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=HistoryResponse)
async def get_history(user_id: str = None, limit: int = 20):
    """
    Retrieve user's analysis history.

    Placeholder endpoint - returns mock data.
    """
    return {
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


@router.post("", response_model=dict)
async def save_history(request: HistorySaveRequest):
    """
    Save or update user medical history.

    Placeholder endpoint - returns mock data.
    """
    return {
        "history_id": "history_001",
        "user_id": request.user_id,
        "saved_at": "2026-07-20T10:30:00Z",
        "status": "success"
    }
