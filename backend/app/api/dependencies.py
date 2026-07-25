"""FastAPI dependency functions for authentication.

Provides reusable dependencies for extracting and validating authenticated users.
Dependencies integrate JWT validation, user lookup, and exception handling.

RESPONSIBILITY SPLIT:
- app/core/security.py: JWT encoding/decoding, token creation
- app/api/dependencies.py: Authentication dependency injection
- Route handlers: Use dependencies to access authenticated user

Future dependencies can be added here for:
- Role-based access control
- Permission checking
- Email verification status
- Account status validation
"""

import logging
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from jose import JWTError
from jose.exceptions import ExpiredSignatureError

from app.core.security import oauth2_scheme, decode_access_token
from app.core.exceptions import (
    TokenExpiredError,
    InvalidTokenError,
    InvalidCredentialsError,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.database import get_db

logger = logging.getLogger(__name__)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> User:
    """Extract authenticated user from JWT access token.

    Validates JWT token, extracts user ID, and loads user from database.
    Raises domain exceptions on authentication failure (caught by global handlers).

    Authentication Flow:
    1. OAuth2PasswordBearer extracts Bearer token from Authorization header
    2. JWT signature is verified using SECRET_KEY and ALGORITHM
    3. Token expiration is checked
    4. Subject claim (user_id) is extracted
    5. User is loaded from database by ID
    6. User is returned to route handler

    Args:
        token: JWT access token from Authorization header (injected by oauth2_scheme)
        session: Database session for user lookup (dependency-injected)

    Returns:
        Authenticated User model with all user data

    Raises:
        TokenExpiredError: If token has expired (caught by handler → HTTP 401)
        InvalidTokenError: If token is invalid, corrupted, or has invalid format (→ HTTP 401)
        InvalidCredentialsError: If user not found in database for valid token (→ HTTP 401)

    Examples:
        In a protected route:

            @router.get("/profile")
            async def get_profile(current_user: User = Depends(get_current_user)):
                return {"user_id": current_user.id, "email": current_user.email}

        The dependency automatically validates the token and loads the user.
        If authentication fails at any step, an exception is raised and handled
        globally, returning a consistent error response.
    """

    # Decode and validate JWT token
    # Raises ExpiredSignatureError if token has expired
    # Raises JWTError if signature is invalid or structure is corrupted
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError:
        logger.warning("Access attempt with expired token")
        raise TokenExpiredError()
    except JWTError:
        logger.warning("Access attempt with invalid token signature")
        raise InvalidTokenError()

    # Extract user ID from token subject claim
    # Subject should be UUID as string
    subject: str = payload.get("sub")
    if subject is None:
        logger.warning("Token missing required 'sub' claim")
        raise InvalidTokenError()

    # Convert subject to UUID
    # If subject is not a valid UUID, token is malformed
    try:
        user_id = UUID(subject)
    except ValueError:
        logger.warning(f"Token subject is not a valid UUID: {subject}")
        raise InvalidTokenError()

    # Load user from database
    # Token is valid but user may have been deleted
    user_repository = UserRepository(session)
    user = user_repository.get_by_id(user_id)

    if user is None:
        logger.warning(f"Valid token but user not found: {user_id}")
        raise InvalidCredentialsError("User not found")

    logger.debug(f"User authenticated: {user_id}")
    return user
