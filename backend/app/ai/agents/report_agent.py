"""Health report generation agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider
from app.ai.models import HealthReport

logger = logging.getLogger(__name__)


class ReportAgent(BaseAgent):
    """Agent for health report generation."""

    def __init__(self):
        """Initialize report agent."""
        super().__init__(name="ReportAgent")

    @staticmethod
    def _fallback_report() -> HealthReport:
        """Deterministic report used only when the AI provider is unusable."""
        return HealthReport(
            summary="Based on symptom analysis and risk assessment, you show signs of possible respiratory infection.",
            home_care=[
                "Get plenty of rest",
                "Stay hydrated with water and warm liquids",
                "Use honey to soothe throat",
                "Gargle with salt water",
            ],
            lifestyle=[
                "Avoid strenuous activities",
                "Stay in well-ventilated areas",
                "Maintain good hygiene and wash hands regularly",
                "Wear a mask when around others",
            ],
            monitoring=[
                "Monitor temperature daily",
                "Track symptom progression",
                "Note any red flag symptoms",
                "Keep records for your doctor visit",
            ],
            references=[
                "WHO guidelines for respiratory infections",
                "CDC common cold and flu information",
                "Medical reference materials",
            ],
        )

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate health report using AI provider and update workflow state.

        Always sets state["health_report"] to a valid HealthReport: the AI
        result on success, the deterministic fallback when the provider call
        fails, returns nothing, or returns unparseable JSON.
        """
        risk_assessment = state.get("risk_assessment", {})
        risk_level = getattr(risk_assessment, "risk_level", "moderate")

        specialist_recommendation = state.get("specialist_recommendation", {})
        specialist = getattr(specialist_recommendation, "specialist", None)

        analysis_input = state.get("analysis_input")
        symptoms = getattr(analysis_input, "symptoms", None) or state.get("user_input", "")

        try:
            provider = create_provider()
            await provider.initialize()

            report_result = await provider.generate_report_structured(
                symptoms=symptoms,
                risk_level=risk_level,
                specialist=specialist,
            )

            state["health_report"] = report_result

            logger.info(
                f"Health report completed: home_care={len(report_result.home_care)}, "
                f"lifestyle={len(report_result.lifestyle)}, "
                f"monitoring={len(report_result.monitoring)}"
            )

        except Exception as e:
            logger.exception("Health report generation failed, using fallback report")
            state["errors"] = state.get("errors", []) + [f"Health report error: {str(e)}"]
            state["health_report"] = self._fallback_report()

        state["current_step"] = "health_report"

        return state
