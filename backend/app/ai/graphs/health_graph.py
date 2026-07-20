"""Health analysis graph structure."""

from typing import Any, Dict, List


class HealthGraph:
    """Graph structure for health analysis workflow."""

    def __init__(self):
        """Initialize health graph."""
        self.nodes = {}
        self.edges = []

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
        """
        Get sequence of nodes for workflow execution.

        TODO: Implement graph traversal for workflow sequence.
        """
        return list(self.nodes.keys())

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation."""
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
        }
