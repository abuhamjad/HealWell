"""Analysis input and result models."""

from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.ai.models.risk import RiskAssessment
    from app.ai.models.specialist import SpecialistRecommendation
    from app.ai.models.report import HealthReport


class AnalysisInput(BaseModel):
    """Input data for health analysis."""
    symptoms: str
    user_id: Optional[str] = None
    medical_history: Optional[str] = None
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None


# Use string forward references to avoid circular imports
class AnalysisResult(BaseModel):
    """Complete analysis result."""
    analysis_id: str
    risk_assessment: Optional["RiskAssessment"] = None  # type: ignore
    specialist_recommendation: Optional["SpecialistRecommendation"] = None  # type: ignore
    health_report: Optional["HealthReport"] = None  # type: ignore
    emergency_alert: bool = False
    emergency_message: Optional[str] = None


# Update forward references after all models are loaded
def _setup_forward_refs():
    from app.ai.models.risk import RiskAssessment
    from app.ai.models.specialist import SpecialistRecommendation
    from app.ai.models.report import HealthReport

    AnalysisResult.model_rebuild()
