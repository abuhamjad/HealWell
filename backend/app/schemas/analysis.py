from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
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


class AnalysisHistoryItem(BaseModel):
    """Summary of an analysis for history list (no full JSON blobs)."""
    analysis_id: str
    created_at: datetime
    risk_level: Optional[str]
    confidence: Optional[float]
    specialist: Optional[str]
    emergency: bool


class AnalysisDetailResponse(BaseModel):
    """Complete analysis with all stored data (for detail endpoint)."""
    analysis_id: str
    created_at: datetime
    risk_level: Optional[str]
    confidence: Optional[float]
    specialist: Optional[str]
    emergency: bool
    # Full AI output as stored in database
    risk_assessment: Optional[dict]
    specialist_recommendation: Optional[dict]
    health_report: Optional[dict]


class AnalysisHistoryResponse(BaseModel):
    """Paginated history response."""
    items: List[AnalysisHistoryItem]
    total: int
    limit: int
    offset: int
