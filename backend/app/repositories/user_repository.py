"""User repository for user-specific database operations."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """User data access repository.

    Provides all user-specific database operations.
    Uses SQLAlchemy 2.x select() syntax with no raw SQL.
    """

    def __init__(self, session: Session):
        """Initialize user repository."""
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address.

        Args:
            email: User's email address (case-sensitive).

        Returns:
            User instance or None if not found.
        """
        return self.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: User's username (case-sensitive).

        Returns:
            User instance or None if not found.
        """
        return self.session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()

    def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email.

        Args:
            email: User's email address.

        Returns:
            True if email is registered, False otherwise.
        """
        result = self.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
        return result is not None

    def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username.

        Args:
            username: User's username.

        Returns:
            True if username is registered, False otherwise.
        """
        result = self.session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        return result is not None

    def create_user(
        self,
        email: str,
        username: str,
        hashed_password: str,
    ) -> User:
        """Create new user without committing.

        Args:
            email: User's email address (must be unique).
            username: User's username (must be unique).
            hashed_password: Bcrypt hashed password.

        Returns:
            Created User instance with generated id/timestamps.
        """
        return self.create(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
