"""SQLAlchemy declarative base for all ORM models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    All model classes inherit from this to participate in the
    declarative mapping system and gain access to the declarative
    table generation and metadata tracking.
    """
    pass
