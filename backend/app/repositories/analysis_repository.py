"""Analysis repository for analysis-specific database operations."""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.repositories.base_repository import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):
    """Analysis data access repository.

    Provides all analysis-specific database operations.
    Uses SQLAlchemy 2.x select() syntax with no raw SQL.
    """

    def __init__(self, session: Session):
        """Initialize analysis repository."""
        super().__init__(session, Analysis)

    def create_analysis(
        self,
        user_id: UUID,
        symptoms: dict,
        risk_level: Optional[str] = None,
        confidence: Optional[float] = None,
        specialist: Optional[str] = None,
        emergency: bool = False,
        risk_assessment: Optional[dict] = None,
        specialist_recommendation: Optional[dict] = None,
        health_report: Optional[dict] = None,
    ) -> Analysis:
        """Create new analysis without committing.

        Args:
            user_id: ID of user who owns this analysis.
            symptoms: Dict of reported symptoms (required).
            risk_level: Optional risk level string (e.g., 'low', 'medium', 'high').
            confidence: Optional confidence score (0.0-1.0).
            specialist: Optional recommended specialist name.
            emergency: Flag indicating emergency status (default False).
            risk_assessment: Optional dict with risk analysis details.
            specialist_recommendation: Optional dict with specialist recommendation.
            health_report: Optional dict with full health report.

        Returns:
            Created Analysis instance with generated id/timestamps.
        """
        return self.create(
            user_id=user_id,
            symptoms=symptoms,
            risk_level=risk_level,
            confidence=confidence,
            specialist=specialist,
            emergency=emergency,
            risk_assessment=risk_assessment,
            specialist_recommendation=specialist_recommendation,
            health_report=health_report,
        )

    def get_user_history(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Analysis]:
        """Get paginated analyses for a user, newest first.

        Pagination is performed entirely by the database.

        Args:
            user_id: ID of user.
            limit: Number of results to return (default 20).
            offset: Number of results to skip (default 0).

        Returns:
            List of Analysis instances ordered by created_at DESC,
            limited to the requested page.
        """
        stmt = (
            select(Analysis)
            .where(Analysis.user_id == user_id)
            .order_by(Analysis.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return self.session.execute(stmt).scalars().all()

    def get_recent(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Analysis]:
        """Get most recent analyses across all users, newest first.

        Pagination is performed entirely by the database.

        Args:
            limit: Number of results to return (default 10).
            offset: Number of results to skip (default 0).

        Returns:
            List of Analysis instances ordered by created_at DESC,
            limited to the requested page.
        """
        stmt = (
            select(Analysis)
            .order_by(Analysis.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return self.session.execute(stmt).scalars().all()

    def count_by_user(self, user_id: UUID) -> int:
        """Count total analyses for a user.

        Args:
            user_id: ID of user.

        Returns:
            Count of analyses belonging to user.
        """
        stmt = select(func.count()).select_from(Analysis).where(
            Analysis.user_id == user_id
        )
        result = self.session.execute(stmt).scalar()
        return result or 0

    def count_all(self) -> int:
        """Count total analyses across all users.

        Returns:
            Total count of all analyses in database.
        """
        stmt = select(func.count()).select_from(Analysis)
        result = self.session.execute(stmt).scalar()
        return result or 0
