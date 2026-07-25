"""User model for authentication and account management."""

from datetime import datetime, date
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import String, DateTime, Float, Date, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.analysis import Analysis


class User(Base):
    """User account model with authentication and health profile."""

    __tablename__ = "users"

    # Primary Key
    id: Mapped[UUID] = mapped_column(primary_key=True)

    # Authentication Fields
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Patient Profile Fields (v0.10.1+)
    # Full legal name and preferred display name
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    preferred_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # Date of birth is the single source of truth; age is calculated dynamically
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    height_cm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Medical Information Fields (v0.10.1+)
    allergies: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    existing_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    current_medications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medical_history: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    analyses: Mapped[list["Analysis"]] = relationship(
        "Analysis",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Analysis.user_id",
    )

    def __repr__(self) -> str:
        """Return string representation."""
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
