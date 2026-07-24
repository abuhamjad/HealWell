"""Health report generation agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider

logger = logging.getLogger(__name__)


class ReportAgent(BaseAgent):
    """Agent for health report generation using AI provider synthesis."""

    def __init__(self):
        """Initialize report agent."""
        super().__init__(name="ReportAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate comprehensive health report synthesizing all previous analysis.

        Reads symptom_analysis, risk_assessment, and specialist_recommendation
        from state, calls provider to synthesize into a patient-friendly report,
        and updates state with results.

        Args:
            state: HealthAnalysisState containing all previous analysis results

        Returns:
            Updated state with health_report results
        """
        try:
            from app.ai.models import HealthReport

            symptom_analysis = state.get("symptom_analysis", {})
            risk_assessment = state.get("risk_assessment")
            specialist_recommendation = state.get("specialist_recommendation")

            # Validate all inputs exist
            if not all([symptom_analysis, risk_assessment, specialist_recommendation]):
                logger.error("Missing required analysis results for report generation")
                raise ValueError("All previous analysis results required for report generation")

            provider = create_provider()
            await provider.initialize()

            report_result = await provider.generate_health_report_structured(
                symptom_analysis=symptom_analysis,
                risk_assessment=risk_assessment,
                specialist_recommendation=specialist_recommendation,
            )

            if report_result is None:
                logger.error("Provider returned None for health report")
                raise ValueError("Health report generation returned None")

            # Combine report fields with explanation fields from earlier agents
            combined_report = HealthReport(
                summary=report_result.summary,
                summary_explanation=report_result.summary_explanation,
                specialist_explanation=specialist_recommendation.specialist_explanation,
                home_care=report_result.home_care,
                personalized_home_care=report_result.personalized_home_care,
                lifestyle=report_result.lifestyle,
                personalized_lifestyle=report_result.personalized_lifestyle,
                monitoring=report_result.monitoring,
                monitoring_guidance=report_result.monitoring_guidance,
                emergency_instructions=report_result.emergency_instructions,
                references=report_result.references,
            )

            state["health_report"] = combined_report
            state["current_step"] = "health_report"
            state["workflow_status"] = "analysis_complete"

            logger.info(
                f"Health report generated: {len(combined_report.personalized_home_care)} personalized home care, "
                f"{len(combined_report.monitoring_guidance)} monitoring items, "
                f"emergency_instructions: {bool(combined_report.emergency_instructions)}"
            )

        except Exception as e:
            logger.error(f"Report generation failed: {e}. Using MockProvider fallback.")
            state["errors"] = state.get("errors", []) + [f"Report generation error: {str(e)}"]
            state["current_step"] = "health_report_fallback"
            from app.ai.providers.mock_provider import MockProvider
            mock_provider = MockProvider()
            symptom_analysis = state.get("symptom_analysis", {})
            risk_assessment = state.get("risk_assessment")
            specialist_recommendation = state.get("specialist_recommendation")
            if not risk_assessment:
                risk_assessment = await mock_provider.analyze_risk_structured(symptom_analysis)
                state["risk_assessment"] = risk_assessment
            if not specialist_recommendation:
                specialist_recommendation = await mock_provider.analyze_specialist_structured(risk_assessment)
                state["specialist_recommendation"] = specialist_recommendation
            report_result = await mock_provider.generate_health_report_structured(
                symptom_analysis=symptom_analysis,
                risk_assessment=risk_assessment,
                specialist_recommendation=specialist_recommendation,
            )
            state["health_report"] = report_result

        return state

