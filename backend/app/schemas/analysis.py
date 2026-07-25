from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.ai.models import RiskAssessment, SpecialistRecommendation, HealthReport


class AnalysisRequest(BaseModel):
    """Request to create a health analysis.

    User identity is derived from authentication context, never from client input.
    Ownership is always enforced - analysis is created for authenticated user.
    """

    symptoms: str


class AnalysisResponse(BaseModel):
    """Health analysis response.

    Combines AI-generated analysis with database persistence information.

    Includes:
    - analysis_id: Database ID (for history and detail queries)
    - Risk assessment from AI engine
    - Specialist recommendations from AI engine
    - Health report from AI engine
    - created_at: When analysis was persisted
    - status: Success indicator

    Never includes:
    - Internal AI prompts
    - Model configuration
    - Stack traces
    - User ID (client already knows their own ID)
    """

    analysis_id: str  # Database ID for tracking
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
    # Database persistence information
    created_at: datetime  # When analysis was persisted to database


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
