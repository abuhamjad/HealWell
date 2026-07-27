"""Base provider abstract interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ai.models import AnalysisInput, AnalysisResult


class BaseProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, api_key: str = None):
        """Initialize provider with optional API key."""
        self.api_key = api_key
        self.is_initialized = False

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the provider."""
        pass

    @abstractmethod
    async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
        """Analyze symptoms and return assessment."""
        pass

    @abstractmethod
    async def generate_report(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """Generate a detailed health report."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if provider is healthy and accessible."""
        pass

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass
