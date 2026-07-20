"""LangGraph workflow builder for health analysis."""

import uuid
from typing import Any
from langgraph.graph import StateGraph
from app.ai.state import HealthAnalysisState
from app.ai.agents import (
    SymptomAgent,
    RiskAgent,
    SpecialistAgent,
    ReportAgent,
)


def build_health_analysis_graph() -> StateGraph:
    """Build the health analysis workflow graph using LangGraph."""
    workflow = StateGraph(HealthAnalysisState)

    symptom_agent = SymptomAgent()
    risk_agent = RiskAgent()
    specialist_agent = SpecialistAgent()
    report_agent = ReportAgent()

    async def symptom_node(state: dict[str, Any]) -> dict[str, Any]:
        """Symptom analysis node."""
        return await symptom_agent.execute(state)

    async def risk_node(state: dict[str, Any]) -> dict[str, Any]:
        """Risk assessment node."""
        return await risk_agent.execute(state)

    async def specialist_node(state: dict[str, Any]) -> dict[str, Any]:
        """Specialist recommendation node."""
        return await specialist_agent.execute(state)

    async def report_node(state: dict[str, Any]) -> dict[str, Any]:
        """Health report generation node."""
        return await report_agent.execute(state)

    workflow.add_node("symptom_agent", symptom_node)
    workflow.add_node("risk_agent", risk_node)
    workflow.add_node("specialist_agent", specialist_node)
    workflow.add_node("report_agent", report_node)

    workflow.set_entry_point("symptom_agent")
    workflow.add_edge("symptom_agent", "risk_agent")
    workflow.add_edge("risk_agent", "specialist_agent")
    workflow.add_edge("specialist_agent", "report_agent")
    workflow.set_finish_point("report_agent")

    return workflow


def compile_health_analysis_graph() -> Any:
    """Compile the health analysis workflow graph."""
    graph = build_health_analysis_graph()
    return graph.compile()
