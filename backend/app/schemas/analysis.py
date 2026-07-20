from pydantic import BaseModel
from typing import Optional


class AnalysisRequest(BaseModel):
    symptoms: str
    user_id: Optional[str] = None


class AnalysisResponse(BaseModel):
    analysis_id: str
    risk_level: str
    confidence: float
    specialist: str
    emergency: bool
    status: str = "success"
