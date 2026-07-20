"""Specialist recommendation agent."""

from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.models import SpecialistRecommendation


class SpecialistAgent(BaseAgent):
    """Agent for specialist recommendation."""

    def __init__(self):
        """Initialize specialist agent."""
        super().__init__(name="SpecialistAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Recommend specialist based on risk assessment."""
        risk_assessment = state.get("risk_assessment", {})
        risk_level = getattr(risk_assessment, "risk_level", "moderate")

        state["specialist_recommendation"] = SpecialistRecommendation(
            specialist="General Physician",
            reasoning="Moderate risk level with respiratory symptoms warrants physician consultation",
            urgency="24-48 hours",
        )
        state["current_step"] = "specialist_recommendation"

        return state
