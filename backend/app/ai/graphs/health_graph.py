"""Health analysis graph structure for visualization."""

from typing import Any, Dict, List


class HealthGraph:
    """Graph structure for health analysis workflow visualization.

    This class provides visualization support for the LangGraph workflow.
    The actual workflow execution uses LangGraph (see langgraph_builder.py).

    Workflow Structure:
    - User Input
      ↓
    - SymptomAgent (Analyzes reported symptoms)
      ↓
    - RiskAgent (Assesses health risk level)
      ↓
    - SpecialistAgent (Recommends appropriate specialist)
      ↓
    - ReportAgent (Generates health report)
      ↓
    - Final HealthAnalysisState
    """

    def __init__(self):
        """Initialize health graph for visualization."""
        self.nodes = self._initialize_nodes()
        self.edges = self._initialize_edges()

    def _initialize_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize workflow nodes."""
        return {
            "input": {
                "id": "input",
                "type": "data",
                "label": "User Input",
                "description": "Patient symptoms and medical history",
            },
            "symptom_analysis": {
                "id": "symptom_analysis",
                "type": "agent",
                "label": "Symptom Analysis",
                "description": "SymptomAgent - Analyzes reported symptoms",
                "agent": "SymptomAgent",
            },
            "risk_assessment": {
                "id": "risk_assessment",
                "type": "agent",
                "label": "Risk Assessment",
                "description": "RiskAgent - Evaluates health risk level",
                "agent": "RiskAgent",
            },
            "specialist_recommendation": {
                "id": "specialist_recommendation",
                "type": "agent",
                "label": "Specialist Recommendation",
                "description": "SpecialistAgent - Recommends specialist type",
                "agent": "SpecialistAgent",
            },
            "health_report": {
                "id": "health_report",
                "type": "agent",
                "label": "Health Report",
                "description": "ReportAgent - Generates comprehensive health report",
                "agent": "ReportAgent",
            },
            "output": {
                "id": "output",
                "type": "data",
                "label": "Analysis Result",
                "description": "Final HealthAnalysisState with all results",
            },
        }

    def _initialize_edges(self) -> List[Dict[str, str]]:
        """Initialize workflow edges."""
        return [
            {"from": "input", "to": "symptom_analysis", "label": "start"},
            {"from": "symptom_analysis", "to": "risk_assessment", "label": "analyze"},
            {"from": "risk_assessment", "to": "specialist_recommendation", "label": "assess"},
            {"from": "specialist_recommendation", "to": "health_report", "label": "recommend"},
            {"from": "health_report", "to": "output", "label": "complete"},
        ]

    def add_node(self, node_id: str, node_type: str, data: Dict[str, Any] = None) -> None:
        """Add node to graph."""
        self.nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "data": data or {},
        }

    def add_edge(self, from_node: str, to_node: str, label: str = None) -> None:
        """Add edge to graph."""
        self.edges.append({
            "from": from_node,
            "to": to_node,
            "label": label,
        })

    def get_workflow_sequence(self) -> List[str]:
        """Get sequence of agent nodes for workflow execution."""
        return [
            "symptom_analysis",
            "risk_assessment",
            "specialist_recommendation",
            "health_report",
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation for visualization."""
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
        }
