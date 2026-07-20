"""Health report model."""

from pydantic import BaseModel
from typing import List


class HealthReport(BaseModel):
    """Health report output."""
    summary: str
    home_care: List[str] = []
    lifestyle: List[str] = []
    monitoring: List[str] = []
    references: List[str] = []
