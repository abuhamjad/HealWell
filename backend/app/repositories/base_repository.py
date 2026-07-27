"""Generic repository base class for reusable CRUD operations."""

from typing import Generic, TypeVar, Optional, List, Type
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Generic repository for common CRUD operations.

    Provides transaction-safe database access without committing.
    All operations use SQLAlchemy 2.x select() syntax.
    """

    def __init__(self, session: Session, model: Type[T]):
        """Initialize repository with session and model class."""
        self.session = session
        self.model = model

    def get_by_id(self, id: UUID) -> Optional[T]:
        """Get record by primary key ID."""
        return self.session.execute(
            select(self.model).where(self.model.id == id)
        ).scalar_one_or_none()

    def get_all(self) -> List[T]:
        """Get all records."""
        return self.session.execute(select(self.model)).scalars().all()

    def create(self, **kwargs) -> T:
        """Create new record without committing.

        Returns the created model instance with generated fields populated.
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        return instance

    def update(self, id: UUID, **kwargs) -> Optional[T]:
        """Update record by ID without committing.

        Returns updated instance or None if not found.
        """
        instance = self.get_by_id(id)
        if instance is None:
            return None

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        return instance

    def delete(self, id: UUID) -> bool:
        """Delete record by ID without committing.

        Returns True if record existed and was deleted, False otherwise.
        """
        instance = self.get_by_id(id)
        if instance is None:
            return False

        self.session.delete(instance)
        return True

    def delete_all(self) -> int:
        """Delete all records without committing.

        Returns count of deleted records.
        """
        stmt = delete(self.model)
        result = self.session.execute(stmt)
        return result.rowcount
