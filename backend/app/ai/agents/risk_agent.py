"""Risk assessment agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider

logger = logging.getLogger(__name__)


class RiskAgent(BaseAgent):
    """Agent for risk assessment using AI provider."""

    def __init__(self):
        """Initialize risk agent."""
        super().__init__(name="RiskAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Assess health risk using AI provider and update workflow state.

        Reads symptom_analysis from state, calls provider for structured
        risk assessment, and updates state with results.

        Args:
            state: HealthAnalysisState containing symptom_analysis

        Returns:
            Updated state with risk_assessment results
        """
        try:
            symptom_analysis = state.get("symptom_analysis", {})

            if not symptom_analysis:
                logger.warning("No symptom_analysis in state, using empty fallback")
                symptom_analysis = {
                    "detected_symptoms": [],
                    "summary": "No symptom analysis available",
                    "severity_indicators": [],
                    "affected_systems": [],
                }

            provider = create_provider()
            await provider.initialize()

            risk_result = await provider.analyze_risk_structured(symptom_analysis)

            state["risk_assessment"] = risk_result
            state["current_step"] = "risk_assessment"
            state["workflow_status"] = "risk_assessment_complete"

            logger.info(
                f"Risk assessment completed: risk_level={risk_result.risk_level}, "
                f"confidence={risk_result.confidence}%"
            )

        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            state["errors"] = state.get("errors", []) + [f"Risk assessment error: {str(e)}"]
            state["current_step"] = "risk_assessment_failed"

        return state
