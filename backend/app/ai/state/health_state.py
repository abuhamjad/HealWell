"""Shared workflow state for health analysis."""

from typing import TypedDict, Optional, List, Any
from app.ai.models import (
    AnalysisInput,
    RiskAssessment,
    SpecialistRecommendation,
    HealthReport,
)


class HealthAnalysisState(TypedDict, total=False):
    """Shared workflow state for health analysis workflow."""

    session_id: str
    user_input: str
    analysis_input: AnalysisInput
    symptom_analysis: dict[str, Any]
    risk_assessment: RiskAssessment
    specialist_recommendation: SpecialistRecommendation
    health_report: HealthReport
    workflow_status: str
    current_step: str
    errors: List[str]
    metadata: dict[str, Any]
