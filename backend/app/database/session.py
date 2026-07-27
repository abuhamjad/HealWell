"""Database session management and configuration."""

from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Lazy-load engine to allow app startup even if DATABASE_URL is not configured
_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Get or create the SQLAlchemy engine.

    Returns:
        SQLAlchemy Engine with connection pooling configured.

    Raises:
        ValueError: If DATABASE_URL is not configured.
    """
    global _engine

    if _engine is None:
        if not settings.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL is not configured. "
                "Set DATABASE_URL in .env file to enable database functionality."
            )

        _engine = create_engine(
            settings.DATABASE_URL,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            echo=False,
        )

    return _engine


def get_session_factory() -> sessionmaker:
    """Get or create the SQLAlchemy session factory.

    Returns:
        Session factory bound to the application's engine.
    """
    engine = get_engine()
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


# Lazy session factory - created only when first accessed
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=None,  # Will be set when get_db() is first called
)


def get_db() -> Generator[Session, None, None]:
    """Dependency to provide database session to FastAPI routes.

    Lazily initializes the database engine on first use. This allows the
    application to start even if DATABASE_URL is not configured, and only
    raises an error when database access is actually attempted.

    Yields:
        SQLAlchemy Session for the current request.

    Example:
        @app.get("/items")
        async def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    Raises:
        ValueError: If DATABASE_URL is not configured when database access is attempted.
    """
    # Ensure engine is initialized and SessionLocal is bound to it
    engine = get_engine()
    if SessionLocal.kw["bind"] is None:
        SessionLocal.configure(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
