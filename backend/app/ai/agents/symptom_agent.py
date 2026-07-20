"""Symptom analysis agent."""

from typing import Any
from app.ai.agents.base import BaseAgent


class SymptomAgent(BaseAgent):
    """Agent for analyzing symptoms."""

    def __init__(self):
        """Initialize symptom agent."""
        super().__init__(name="SymptomAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Analyze symptoms and update workflow state."""
        symptoms = state.get("user_input", "")

        state["symptom_analysis"] = {
            "detected_symptoms": [
                "fever",
                "cough",
                "fatigue",
            ],
            "confidence": 0.85,
            "summary": f"Analysis of reported symptoms: {symptoms}",
        }
        state["current_step"] = "symptom_analysis"

        return state
