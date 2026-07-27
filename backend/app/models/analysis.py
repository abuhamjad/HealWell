"""Analysis model for health assessments."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey, func, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Analysis(Base):
    """Health analysis model.

    Represents a single health analysis performed for a user, including
    symptom data, risk assessment, specialist recommendation, and health report.
    """

    __tablename__ = "analyses"

    # Primary Key
    id: Mapped[UUID] = mapped_column(primary_key=True)

    # Foreign Key to User
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Symptom and Assessment Data (JSONB for PostgreSQL, fallback to JSON)
    symptoms: Mapped[dict] = mapped_column(
        JSONB if JSONB is not None else JSON,
        nullable=False,
    )

    # Risk Assessment Results
    risk_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Specialist Information
    specialist: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Emergency Flag
    emergency: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Full AI Analysis Results (stored as JSONB)
    risk_assessment: Mapped[Optional[dict]] = mapped_column(
        JSONB if JSONB is not None else JSON,
        nullable=True,
    )
    specialist_recommendation: Mapped[Optional[dict]] = mapped_column(
        JSONB if JSONB is not None else JSON,
        nullable=True,
    )
    health_report: Mapped[Optional[dict]] = mapped_column(
        JSONB if JSONB is not None else JSON,
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="analyses",
        foreign_keys=[user_id],
    )

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"<Analysis(id={self.id}, user_id={self.user_id}, "
            f"risk_level={self.risk_level}, specialist={self.specialist})>"
        )
