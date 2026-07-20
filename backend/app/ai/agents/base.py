"""Base agent abstract class."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for AI agents."""

    def __init__(self, name: str):
        """Initialize agent with name."""
        self.name = name
        self.state = {}

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic."""
        pass

    def set_state(self, key: str, value: Any) -> None:
        """Set agent state."""
        self.state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get agent state."""
        return self.state.get(key, default)

    def reset_state(self) -> None:
        """Reset agent state."""
        self.state = {}
