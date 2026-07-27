"""Analysis service for health analysis operations."""

from app.ai.models import AnalysisInput, AnalysisResult
from app.ai.workflows.analysis_workflow import AnalysisWorkflow


class AnalysisService:
    """Service for health analysis using AI workflow."""

    def __init__(self):
        """Initialize analysis service with workflow."""
        self.workflow = AnalysisWorkflow()

    async def analyze(self, symptoms: str) -> AnalysisResult:
        """Perform health analysis.

        Args:
            symptoms: User's symptom description.

        Returns:
            AnalysisResult from AI workflow.
        """
        input_data = AnalysisInput(symptoms=symptoms)
        result = await self.workflow.execute(input_data)
        return result

