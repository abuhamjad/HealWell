from pydantic import BaseModel
from typing import Optional
from app.ai.models import RiskAssessment, SpecialistRecommendation, HealthReport


class AnalysisRequest(BaseModel):
    symptoms: str


class AnalysisResponse(BaseModel):
    analysis_id: str
    risk_level: str
    confidence: float
    specialist: str
    emergency: bool
    status: str = "success"
    risk_assessment: RiskAssessment
    specialist_recommendation: SpecialistRecommendation
    health_report: HealthReport
    emergency_message: Optional[str] = None

