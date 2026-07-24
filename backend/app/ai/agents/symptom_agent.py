"""Symptom analysis agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider
from app.ai.models import AnalysisInput

logger = logging.getLogger(__name__)


class SymptomAgent(BaseAgent):
    """Agent for analyzing symptoms using AI provider."""

    def __init__(self):
        """Initialize symptom agent."""
        super().__init__(name="SymptomAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Analyze symptoms using AI provider and update workflow state.

        Extracts analysis input from state, calls provider for structured
        symptom analysis, and updates state with results.

        Args:
            state: HealthAnalysisState containing analysis_input and metadata

        Returns:
            Updated state with symptom_analysis results
        """
        try:
            analysis_input = state.get("analysis_input")

            if not analysis_input:
                logger.warning("No analysis_input in state, using user_input fallback")
                analysis_input = AnalysisInput(
                    symptoms=state.get("user_input", ""),
                    user_id=state.get("metadata", {}).get("user_id"),
                    medical_history=state.get("metadata", {}).get("medical_history"),
                    medications=state.get("metadata", {}).get("medications"),
                    allergies=state.get("metadata", {}).get("allergies"),
                )

            provider = create_provider()
            await provider.initialize()

            symptom_result = await provider.analyze_symptoms_structured(analysis_input)

            state["symptom_analysis"] = symptom_result.model_dump()
            state["current_step"] = "symptom_analysis"
            state["workflow_status"] = "symptom_analysis_complete"

            logger.info(
                f"Symptom analysis completed: {len(symptom_result.detected_symptoms)} symptoms detected, "
                f"confidence: {symptom_result.confidence}%"
            )

        except Exception as e:
            logger.error(f"Symptom analysis failed: {e}. Using MockProvider fallback.")
            state["errors"] = state.get("errors", []) + [f"Symptom analysis error: {str(e)}"]
            state["current_step"] = "symptom_analysis_fallback"
            from app.ai.providers.mock_provider import MockProvider
            mock_provider = MockProvider()
            symptom_result = await mock_provider.analyze_symptoms_structured(analysis_input)
            state["symptom_analysis"] = symptom_result.model_dump()

        return state

