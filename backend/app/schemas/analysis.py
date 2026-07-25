from pydantic import BaseModel
from typing import Optional
from app.ai.models import RiskAssessment, SpecialistRecommendation, HealthReport


class AnalysisRequest(BaseModel):
    symptoms: str
    user_id: Optional[str] = None


class AnalysisResponse(BaseModel):
    analysis_id: str
    # Flat fields retained for the existing frontend contract
    risk_level: str
    confidence: float
    specialist: str
    emergency: bool
    status: str = "success"
    # Full AI output, serialized from the existing models
    risk_assessment: RiskAssessment
    specialist_recommendation: SpecialistRecommendation
    health_report: HealthReport
    emergency_message: Optional[str] = None
