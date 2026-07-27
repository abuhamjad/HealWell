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

        return AnalysisResult(
            analysis_id=session_id,
            risk_assessment=final_state.get("risk_assessment"),
            specialist_recommendation=final_state.get("specialist_recommendation"),
            health_report=final_state.get("health_report"),
            emergency_alert=False,
        )
