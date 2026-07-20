"""Risk assessment agent."""

from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.models import RiskAssessment


class RiskAgent(BaseAgent):
    """Agent for risk assessment."""

    def __init__(self):
        """Initialize risk agent."""
        super().__init__(name="RiskAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Assess health risk and update workflow state."""
        symptom_analysis = state.get("symptom_analysis", {})

        state["risk_assessment"] = RiskAssessment(
            risk_level="moderate",
            confidence=0.82,
            reasoning="Based on detected symptoms: fever and cough suggest possible respiratory infection",
            warning_signs=[
                "persistent high fever above 38.5°C",
                "difficulty breathing",
                "chest pain",
            ],
        )
        state["current_step"] = "risk_assessment"

        return state
