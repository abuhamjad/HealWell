"""Risk assessment model."""

from pydantic import BaseModel
from typing import List


class RiskAssessment(BaseModel):
    """Risk assessment result."""
    risk_level: str  # low, moderate, high
    confidence: float  # 0-100
    reasoning: str
    risk_explanation: str
    confidence_explanation: str
    warning_signs: List[str] = []
