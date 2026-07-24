"""Risk assessment model."""

from pydantic import BaseModel
from typing import List


class RiskAssessment(BaseModel):
    """Risk assessment result."""
    risk_level: str  # LOW, MODERATE, HIGH
    confidence: float  # 0.0-1.0
    emergency_alert: bool
    red_flags_detected: List[str] = []
    recommended_specialist: str
    reasoning: str
    instructions: str
