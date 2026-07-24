"""Symptom analysis model."""

from pydantic import BaseModel
from typing import List


class SymptomAnalysis(BaseModel):
    """Symptom analysis result from AI model."""
    detected_symptoms: List[str]
    confidence: float  # 0-100
    summary: str
    severity_indicators: List[str] = []
    affected_systems: List[str] = []
