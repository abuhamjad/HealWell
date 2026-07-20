"""Shared AI Pydantic models."""

from pydantic import BaseModel
from typing import List, Optional


class AnalysisInput(BaseModel):
    """Input data for health analysis."""
    symptoms: str
    user_id: Optional[str] = None
    medical_history: Optional[str] = None
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None


class RiskAssessment(BaseModel):
    """Risk assessment result."""
    risk_level: str  # low, moderate, high
    confidence: float  # 0-100
    reasoning: str
    warning_signs: List[str] = []


class SpecialistRecommendation(BaseModel):
    """Specialist recommendation."""
    specialist: str
    reasoning: str
    urgency: str  # immediate, 24-48 hours, 1-2 weeks


class HealthReport(BaseModel):
    """Health report output."""
    summary: str
    home_care: List[str] = []
    lifestyle: List[str] = []
    monitoring: List[str] = []
    references: List[str] = []


class AnalysisResult(BaseModel):
    """Complete analysis result."""
    analysis_id: str
    risk_assessment: RiskAssessment
    specialist_recommendation: SpecialistRecommendation
    health_report: HealthReport
    emergency_alert: bool = False
    emergency_message: Optional[str] = None
