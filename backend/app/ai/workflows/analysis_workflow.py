"""Health analysis workflow orchestration using LangGraph."""

import uuid
from typing import Any
from app.ai.models import AnalysisInput, AnalysisResult
from app.ai.graphs.langgraph_builder import compile_health_analysis_graph
from app.ai.state import HealthAnalysisState


class AnalysisWorkflow:
    """Orchestrates the health analysis workflow using LangGraph."""

    def __init__(self):
        """Initialize analysis workflow with compiled LangGraph."""
        self.compiled_graph = compile_health_analysis_graph()

    async def execute(self, input_data: AnalysisInput) -> AnalysisResult:
        """Execute the analysis workflow with LangGraph orchestration."""
        session_id = str(uuid.uuid4())

        initial_state: HealthAnalysisState = {
            "session_id": session_id,
            "user_input": input_data.symptoms,
            "analysis_input": input_data,
            "symptom_analysis": {},
            "risk_assessment": None,
            "specialist_recommendation": None,
            "health_report": None,
            "doctor_recommendations": [],
            "workflow_status": "started",
            "current_step": "initialization",
            "errors": [],
            "metadata": {
                "user_id": input_data.user_id,
                "medical_history": input_data.medical_history,
                "medications": input_data.medications,
                "allergies": input_data.allergies,
            },
        }

        final_state = await self.compiled_graph.ainvoke(initial_state)

        risk_assessment = final_state.get("risk_assessment")
        specialist_recommendation = final_state.get("specialist_recommendation")
        health_report = final_state.get("health_report")

        from app.ai.providers.mock_provider import MockProvider
        mock_provider = MockProvider()

        if not risk_assessment:
            symptom_analysis = final_state.get("symptom_analysis", {})
            if not symptom_analysis:
                symptom_analysis = (await mock_provider.analyze_symptoms_structured(input_data)).model_dump()
            risk_assessment = await mock_provider.analyze_risk_structured(symptom_analysis)

        if not specialist_recommendation:
            specialist_recommendation = await mock_provider.analyze_specialist_structured(risk_assessment)

        if not health_report:
            health_report = await mock_provider.generate_health_report_structured(
                symptom_analysis=final_state.get("symptom_analysis", {}),
                risk_assessment=risk_assessment,
                specialist_recommendation=specialist_recommendation,
            )

        risk_level_str = (risk_assessment.risk_level or "").upper() if risk_assessment else "LOW"
        is_emergency = (risk_level_str == "HIGH") or getattr(risk_assessment, "emergency_alert", False)

        return AnalysisResult(
            analysis_id=session_id,
            risk_assessment=risk_assessment,
            specialist_recommendation=specialist_recommendation,
            health_report=health_report,
            emergency_alert=is_emergency,
            provider_used=getattr(risk_assessment, "provider_used", "mock"),
        )

