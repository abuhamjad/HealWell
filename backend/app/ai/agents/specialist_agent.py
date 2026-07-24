"""Specialist recommendation agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider

logger = logging.getLogger(__name__)


class SpecialistAgent(BaseAgent):
    """Agent for specialist recommendation using AI provider."""

    def __init__(self):
        """Initialize specialist agent."""
        super().__init__(name="SpecialistAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Recommend specialist based on risk assessment and update workflow state.

        Reads risk_assessment from state, calls provider for structured
        specialist recommendation, and updates state with results.

        Args:
            state: HealthAnalysisState containing risk_assessment

        Returns:
            Updated state with specialist_recommendation results
        """
        try:
            risk_assessment = state.get("risk_assessment")

            if not risk_assessment:
                logger.warning("No risk_assessment in state, using default fallback")
                raise ValueError("risk_assessment required for specialist recommendation")

            provider = create_provider()
            await provider.initialize()

            specialist_result = await provider.analyze_specialist_structured(risk_assessment)

            state["specialist_recommendation"] = specialist_result
            state["current_step"] = "specialist_recommendation"
            state["workflow_status"] = "specialist_recommendation_complete"

            logger.info(
                f"Specialist recommendation completed: specialist={specialist_result.specialist}, "
                f"urgency={specialist_result.urgency}"
            )

        except Exception as e:
            logger.error(f"Specialist recommendation failed: {e}")
            state["errors"] = state.get("errors", []) + [f"Specialist recommendation error: {str(e)}"]
            state["current_step"] = "specialist_recommendation_failed"

        return state
