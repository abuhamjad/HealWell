"""Authentication service.

RESPONSIBILITY: Authentication business logic only.

This service orchestrates security module functions for authentication operations.
It does NOT contain cryptographic logic - that belongs in app/core/security.py.

Future implementations of register, login, token refresh, and password change
will be added to this service as new methods.

Current state: Helper methods only, no endpoints implemented.

RESPONSIBILITY SPLIT:
- app/core/security.py: Password hashing, JWT creation/validation, OAuth2 config
- app/services/auth_service.py: Authentication business logic (orchestration)

DO NOT duplicate security module functionality in this service.
"""

from typing import Optional
from uuid import UUID

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)


class AuthService:
    """Authentication service orchestrating security operations.

    This service contains authentication business logic.
    It uses security module functions (hash_password, verify_password, etc.)
    but does NOT implement cryptography itself.

    Future methods in this service:
    - register_user(): User registration business logic
    - login_user(): User login business logic
    - authenticate_user(): Validate credentials
    - change_password(): Password change business logic

    Current helper methods are wrappers for security module functions.
    They prepare data and types for future business logic methods.
    """

    @staticmethod
    def hash_user_password(password: str) -> str:
        """Hash a user password for secure storage.

        Orchestrates app/core/security.hash_password() for registration.

        Args:
            password: Plain text password from user input

        Returns:
            Hashed password safe for database storage

        Used by: register_user() (future implementation)
        """
        return hash_password(password)

    @staticmethod
    def verify_user_password(password: str, hashed_password: str) -> bool:
        """Verify a user's password against stored hash.

        Orchestrates app/core/security.verify_password() for authentication.

        Args:
            password: Plain text password from user input
            hashed_password: Previously hashed password from database

        Returns:
            True if password matches, False otherwise

        Used by: authenticate_user() (future implementation)
        """
        return verify_password(password, hashed_password)

    @staticmethod
    def generate_access_token(user_id: UUID) -> str:
        """Generate an access token for a user.

        Orchestrates app/core/security.create_access_token() after successful login.

        Args:
            user_id: UUID of the authenticated user

        Returns:
            JWT access token as string

        Used by: login_user() (future implementation)
        """
        return create_access_token(subject=str(user_id))

    @staticmethod
    def validate_access_token(token: str) -> Optional[UUID]:
        """Validate an access token and extract user ID.

        Orchestrates app/core/security.verify_access_token() for protected routes.

        Args:
            token: JWT access token to validate

        Returns:
            UUID of the token's subject if valid, None if invalid or expired

        Used by: get_current_user() dependency (future implementation)
        """
        subject = verify_access_token(token)
        if subject is None:
            return None
        try:
            return UUID(subject)
        except ValueError:
            return None

    @staticmethod
    def extract_token_subject(token: str) -> Optional[str]:
        """Extract the subject claim from a token without validation.

        Orchestrates app/core/security.verify_access_token() for debugging and logging.
        Used to extract user_id from tokens for logging purposes.

        Args:
            token: JWT token to extract subject from

        Returns:
            Subject claim value if present, None otherwise

        Used by: Logging and debugging utilities
        """
        subject = verify_access_token(token)
        return subject
