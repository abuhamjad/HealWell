from pydantic import BaseModel
from typing import List, Optional


class HistoryItem(BaseModel):
    id: str
    user_id: str
    date: str
    symptoms: str
    risk_level: str
    specialist: str


class HistoryResponse(BaseModel):
    analyses: List[HistoryItem]
    count: int


class HistorySaveRequest(BaseModel):
    user_id: str
    conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
