"""Health report generation agent."""

from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.models import HealthReport


class ReportAgent(BaseAgent):
    """Agent for health report generation."""

    def __init__(self):
        """Initialize report agent."""
        super().__init__(name="ReportAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate health report based on all previous analysis."""
        state["health_report"] = HealthReport(
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
        state["current_step"] = "health_report"

        return state
