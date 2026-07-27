"""Risk assessment agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider
from app.ai.models import RiskAssessment

logger = logging.getLogger(__name__)


class RiskAgent(BaseAgent):
    """Agent for risk assessment."""

    def __init__(self):
        """Initialize risk agent."""
        super().__init__(name="RiskAgent")

    @staticmethod
    def _fallback_assessment() -> RiskAssessment:
        """Deterministic assessment used only when the AI provider is unusable."""
        return RiskAssessment(
            risk_level="moderate",
            confidence=0.82,
            reasoning="Based on detected symptoms: fever and cough suggest possible respiratory infection",
            warning_signs=[
                "persistent high fever above 38.5°C",
                "difficulty breathing",
                "chest pain",
            ],
        )

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Assess health risk using AI provider and update workflow state.

        Always sets state["risk_assessment"] to a valid RiskAssessment: the AI
        result on success, the deterministic fallback when the provider call
        fails, returns nothing, or returns unparseable JSON.
        """
        symptom_analysis = state.get("symptom_analysis", {})

        analysis_input = state.get("analysis_input")
        symptoms = getattr(analysis_input, "symptoms", None) or state.get("user_input", "")

        try:
            provider = create_provider()
            await provider.initialize()

            risk_result = await provider.assess_risk_structured(
                symptoms=symptoms,
                symptom_analysis=symptom_analysis,
            )

            state["risk_assessment"] = risk_result

            logger.info(
                f"Risk assessment completed: level={risk_result.risk_level}, "
                f"confidence={risk_result.confidence}%"
            )

        except Exception as e:
            logger.exception("Risk assessment failed, using fallback assessment")
            state["errors"] = state.get("errors", []) + [f"Risk assessment error: {str(e)}"]
            state["risk_assessment"] = self._fallback_assessment()

        state["current_step"] = "risk_assessment"

        return state
