"""Base agent abstract class."""

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract base class for AI agents."""

    def __init__(self, name: str):
        """Initialize agent with name."""
        self.name = name

    @abstractmethod
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute agent logic with shared workflow state."""
        pass
