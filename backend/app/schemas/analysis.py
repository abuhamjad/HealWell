from pydantic import BaseModel
from typing import Optional, List


class AnalysisRequest(BaseModel):
    symptoms: str
    user_id: Optional[str] = None


class AnalysisResponse(BaseModel):
    analysis_id: str
    risk_level: str
    confidence: float
    confidence_explanation: str
    risk_explanation: str
    specialist: str
    specialist_explanation: str
    emergency: bool
    emergency_instructions: Optional[str] = None
    status: str = "success"

    # Full report content
    summary_explanation: str
    personalized_home_care: List[str] = []
    personalized_lifestyle: List[str] = []
    monitoring_guidance: List[str] = []
