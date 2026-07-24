"""AI Pydantic models for health analysis."""

# Import models in order to avoid circular imports
# Core models first
from app.ai.models.risk import RiskAssessment
from app.ai.models.specialist import SpecialistRecommendation
from app.ai.models.report import HealthReport
from app.ai.models.symptom import SymptomAnalysis

# Composite models that depend on core models
from app.ai.models.analysis import AnalysisInput, AnalysisResult

# Rebuild forward references
AnalysisResult.model_rebuild()

__all__ = [
    "AnalysisInput",
    "AnalysisResult",
    "RiskAssessment",
    "SpecialistRecommendation",
    "HealthReport",
    "SymptomAnalysis",
]
