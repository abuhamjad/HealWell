"""Health report model."""

from pydantic import BaseModel
from typing import List, Optional


class HealthReport(BaseModel):
    """Health report output."""
    summary: str
    home_care: List[str] = []
    lifestyle: List[str] = []
    monitoring: List[str] = []
    references: List[str] = []

    # v0.8 AI-generated explanations
    summary_explanation: str
    specialist_explanation: str
    personalized_home_care: List[str] = []
    personalized_lifestyle: List[str] = []
    monitoring_guidance: List[str] = []
    emergency_instructions: Optional[str] = None
