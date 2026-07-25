"""Security utilities for authentication.

Single source of truth for all cryptographic operations:
- Password hashing (Argon2)
- JWT token creation and validation (HS256)
- OAuth2 scheme configuration

Provides reusable functions for password hashing and JWT management.
Uses modern cryptography standards (Argon2 for passwords, HS256 for tokens).

RESPONSIBILITY SPLIT:
- app/core/security.py: Cryptography, hashing, token creation/validation
- app/services/auth_service.py: Authentication business logic (register, login, etc.)

This module MUST NOT contain business logic.
This module MUST be the sole source of all cryptographic functions.
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from pwdlib import PasswordHash
from pwdlib.argon2 import Argon2
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

# Password hashing using Argon2
pwd_context = PasswordHash(Argon2())

# OAuth2 scheme for FastAPI dependency injection
# Points to the actual login endpoint for OpenAPI documentation accuracy
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    """Hash a password using Argon2.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string safe for database storage
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        password: Plain text password to verify
        hashed_password: Previously hashed password from database

    Returns:
        True if password matches hash, False otherwise
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token.

    Args:
        subject: Subject claim (typically user_id as string)
        expires_delta: Optional custom expiration time. Defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES

    Returns:
        Encoded JWT token string
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Dictionary containing decoded token claims

    Raises:
        JWTError: If token is invalid, expired, or signature verification fails
    """
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    return payload


def verify_access_token(token: str) -> Optional[str]:
    """Verify a JWT access token and extract the subject.

    Args:
        token: JWT token string to verify

    Returns:
        Subject claim (user_id) if token is valid, None otherwise
    """
    try:
        payload = decode_access_token(token)
        subject: str = payload.get("sub")
        if subject is None:
            return None
        return subject
    except JWTError:
        return None
