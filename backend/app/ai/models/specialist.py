"""Specialist recommendation model."""

from pydantic import BaseModel


class SpecialistRecommendation(BaseModel):
    """Specialist recommendation."""
    specialist: str
    reasoning: str
    urgency: str  # immediate, 24-48 hours, 1-2 weeks
