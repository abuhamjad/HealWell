"""Specialist recommendation agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider
from app.ai.models import SpecialistRecommendation

logger = logging.getLogger(__name__)


class SpecialistAgent(BaseAgent):
    """Agent for specialist recommendation."""

    def __init__(self):
        """Initialize specialist agent."""
        super().__init__(name="SpecialistAgent")

    @staticmethod
    def _fallback_recommendation() -> SpecialistRecommendation:
        """Deterministic recommendation used only when the AI provider is unusable."""
        return SpecialistRecommendation(
            specialist="General Physician",
            reasoning="Moderate risk level with respiratory symptoms warrants physician consultation",
            urgency="24-48 hours",
        )

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Recommend specialist using AI provider and update workflow state.

        Always sets state["specialist_recommendation"] to a valid
        SpecialistRecommendation: the AI result on success, the deterministic
        fallback when the provider call fails, returns nothing, or returns
        unparseable JSON.
        """
        risk_assessment = state.get("risk_assessment", {})
        risk_level = getattr(risk_assessment, "risk_level", "moderate")

        analysis_input = state.get("analysis_input")
        symptoms = getattr(analysis_input, "symptoms", None) or state.get("user_input", "")

        try:
            provider = create_provider()
            await provider.initialize()

            specialist_result = await provider.recommend_specialist_structured(
                symptoms=symptoms,
                risk_level=risk_level,
            )

            state["specialist_recommendation"] = specialist_result

            logger.info(
                f"Specialist recommendation completed: specialist={specialist_result.specialist}, "
                f"urgency={specialist_result.urgency}"
            )

        except Exception as e:
            logger.exception("Specialist recommendation failed, using fallback recommendation")
            state["errors"] = state.get("errors", []) + [f"Specialist recommendation error: {str(e)}"]
            state["specialist_recommendation"] = self._fallback_recommendation()

        state["current_step"] = "specialist_recommendation"

        return state
