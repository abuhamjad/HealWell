"""Analysis service for health analysis operations."""

import logging
from typing import Optional, NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.ai.models import AnalysisInput, AnalysisResult
from app.ai.workflows.analysis_workflow import AnalysisWorkflow
from app.ai.providers.factory import create_provider
from app.repositories.analysis_repository import AnalysisRepository
from app.models.analysis import Analysis

logger = logging.getLogger(__name__)


class AnalysisOutput(NamedTuple):
    """Combined AI analysis result and persisted database record.

    Provides both AI-generated analysis and database persistence information.
    """

    ai_result: AnalysisResult
    analysis: Optional[Analysis]


class AnalysisService:
    """Service for health analysis.

    Orchestrates AI workflow and database persistence.
    """

    def __init__(self, session: Session, ai_provider=None):
        """Initialize analysis service with dependency-injected session."""
        self.session = session
        self.ai_provider = ai_provider or create_provider()
        self.workflow = AnalysisWorkflow()
        self.analysis_repo = AnalysisRepository(session)

    async def analyze(self, symptoms: str, user_id: Optional[str] = None) -> AnalysisResult:
        """Perform health analysis and persist to database.

        Executes AI workflow and automatically saves results to PostgreSQL.
        If persistence fails, logs the error but still returns the analysis result.

        Args:
            symptoms: User's symptom description.
            user_id: Optional user ID (uses placeholder UUID if not provided).

        Returns:
            AnalysisResult from AI workflow (guaranteed, even if DB save fails).
        """
        input_data = AnalysisInput(
            symptoms=symptoms,
            user_id=user_id,
        )

        # Execute workflow via LangGraph
        result = await self.workflow.execute(input_data)

        # Persist result to database (best-effort, never fails the analysis)
        try:
            self._persist_analysis(result, symptoms, user_id)
        except Exception as e:
            self.session.rollback()
            logger.exception(f"Failed to persist analysis to database: {str(e)}")

        return result

    def _persist_analysis(
        self,
        result: AnalysisResult,
        symptoms: str,
        user_id: Optional[str] = None,
    ) -> None:
        """Persist analysis result to database.

        Args:
            result: AnalysisResult from AI workflow.
            symptoms: Original symptom input string.
            user_id: Optional user ID (uses placeholder UUID if not provided).

        Raises:
            Any exception from database operations (caller handles with try/except).
        """
        # Use provided user_id or generate placeholder UUID for anonymous analyses
        analysis_user_id = (
            UUID(user_id) if user_id else uuid4()
        )

        # Convert Pydantic models to dicts for JSONB storage
        risk_assessment_dict = result.risk_assessment.model_dump() if result.risk_assessment else None
        specialist_recommendation_dict = (
            result.specialist_recommendation.model_dump() if result.specialist_recommendation else None
        )
        health_report_dict = result.health_report.model_dump() if result.health_report else None

        # Create analysis record
        analysis = self.analysis_repo.create_analysis(
            user_id=analysis_user_id,
            symptoms={"input": symptoms},  # Store as dict for JSONB
            risk_level=result.risk_assessment.risk_level if result.risk_assessment else None,
            confidence=result.risk_assessment.confidence if result.risk_assessment else None,
            specialist=result.specialist_recommendation.specialist if result.specialist_recommendation else None,
            emergency=result.emergency_alert,
            risk_assessment=risk_assessment_dict,
            specialist_recommendation=specialist_recommendation_dict,
            health_report=health_report_dict,
        )

        # Commit transaction
        self.session.commit()

        # Refresh to populate auto-generated fields (id, created_at)
        self.session.refresh(analysis)

        logger.info(
            f"Analysis persisted: id={analysis.id}, user_id={analysis_user_id}, "
            f"risk_level={analysis.risk_level}"
        )

    def get_history(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> dict:
        """Get user's analysis history, newest first.

        Pagination is performed entirely by the database.
        User context is injected by the route layer.

        Args:
            user_id: ID of the user (injected by route/authentication layer).
            limit: Number of results to return (default 20).
            offset: Number of results to skip (default 0).

        Returns:
            Dict with items, total count, limit, and offset.
        """
        # Get paginated analyses for this user (database performs pagination)
        items = self.analysis_repo.get_user_history(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )

        # Get total count for this user (single COUNT(*) query with WHERE clause)
        total = self.analysis_repo.count_by_user(user_id)

        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get_analysis_by_id(self, analysis_id: str, user_id: UUID):
        """Get complete analysis by ID with ownership verification.

        SERVICE RESPONSIBILITY: Enforce ownership authorization.

        Routes should call this instead of accessing repository directly.
        Service guarantees returned analysis belongs to the user.

        Args:
            analysis_id: UUID of the analysis to retrieve.
            user_id: UUID of the requesting user (for ownership check).

        Returns:
            Analysis model instance.

        Raises:
            ValueError: If analysis_id is not a valid UUID.
            AnalysisNotFoundError: If analysis not found OR doesn't belong to user.
        """
        try:
            analysis_uuid = UUID(analysis_id)
        except (ValueError, TypeError):
            logger.warning(f"Invalid analysis_id format: {analysis_id}")
            raise ValueError("Invalid analysis ID format")

        analysis = self.analysis_repo.get_by_id(analysis_uuid)

        # Return 404 for both "not found" and "not owned" (no info leakage)
        if analysis is None or analysis.user_id != user_id:
            logger.warning(
                f"Unauthorized access attempt: user={user_id}, analysis={analysis_uuid}"
            )
            from app.core.exceptions import AnalysisNotFoundError
            raise AnalysisNotFoundError("Analysis not found")

        logger.debug(f"Analysis retrieved: id={analysis_uuid}, user={user_id}")
        return analysis
