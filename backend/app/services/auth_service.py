"""Authentication service.

RESPONSIBILITY: Authentication business logic only.

This service orchestrates security module functions for authentication operations.
It does NOT contain cryptographic logic - that belongs in app/core/security.py.

Future implementations of login, token refresh, and password change
will be added to this service as new methods.

Current state: User registration implemented, other endpoints in future milestones.

RESPONSIBILITY SPLIT:
- app/core/security.py: Password hashing, JWT creation/validation, OAuth2 config
- app/services/auth_service.py: Authentication business logic (orchestration)

DO NOT duplicate security module functionality in this service.
"""

from typing import Optional
from uuid import UUID
import logging
from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)
from app.core.config import settings
from app.core.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError, InvalidCredentialsError
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service orchestrating security operations.

    This service contains authentication business logic.
    It uses security module functions (hash_password, verify_password, etc.)
    but does NOT implement cryptography itself.

    Implemented methods:
    - register_user(): User registration business logic

    Future methods in this service:
    - login_user(): User login business logic
    - authenticate_user(): Validate credentials
    - change_password(): Password change business logic

    Current helper methods are wrappers for security module functions.
    They prepare data and types for business logic methods.
    """

    def __init__(self, session: Session):
        """Initialize AuthService with database session.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.user_repository = UserRepository(session)

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

    def register_user(self, request: UserRegisterRequest) -> UserRegisterResponse:
        """Register a new user account.

        Email normalization:
        - Trimmed of leading/trailing whitespace
        - Converted to lowercase
        - Checked for uniqueness (case-insensitive)

        Username normalization:
        - Trimmed of leading/trailing whitespace
        - Checked for uniqueness (case-sensitive per policy)

        Password is hashed using security module.
        User is persisted to database, then returned safely.

        Args:
            request: User registration request with email, username, password

        Returns:
            UserRegisterResponse with user id, email, username, created_at

        Raises:
            EmailAlreadyExistsError: If email already registered
            UsernameAlreadyExistsError: If username already taken
        """
        # Normalize email: trim whitespace and convert to lowercase
        normalized_email = request.email.strip().lower()

        # Normalize username: trim whitespace only (preserve case)
        normalized_username = request.username.strip()

        # Check email uniqueness (case-insensitive due to normalization)
        if self.user_repository.exists_by_email(normalized_email):
            logger.warning(f"Registration attempt with duplicate email: {normalized_email}")
            raise EmailAlreadyExistsError(normalized_email)

        # Check username uniqueness
        if self.user_repository.exists_by_username(normalized_username):
            logger.warning(f"Registration attempt with duplicate username: {normalized_username}")
            raise UsernameAlreadyExistsError(normalized_username)

        # Hash password using security module
        hashed_password = self.hash_user_password(request.password)

        # Create user in database with normalized values
        user = self.user_repository.create_user(
            email=normalized_email,
            username=normalized_username,
            hashed_password=hashed_password,
        )

        # Commit transaction to generate id and timestamps
        self.session.commit()
        self.session.refresh(user)

        logger.info(f"New user registered: {user.id} ({normalized_email})")

        # Return safe response without password or hash
        return UserRegisterResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
        )

    def login_user(self, request: UserLoginRequest) -> UserLoginResponse:
        """Authenticate user and return JWT access token.

        Email normalization:
        - Trimmed of leading/trailing whitespace
        - Converted to lowercase

        Password verification:
        - Uses security module's verify_password()
        - Constant-time comparison (no timing attacks)

        Token generation:
        - Uses security module's create_access_token()
        - Payload includes sub (user_id), iat, exp

        Security:
        - Never reveals if email exists or password incorrect
        - Always returns same error message for auth failures
        - Prevents user enumeration attacks

        Args:
            request: User login request with email and password

        Returns:
            UserLoginResponse with access_token, token_type, expires_in, user

        Raises:
            InvalidCredentialsError: If email not found or password incorrect
        """
        # Normalize email: trim whitespace and convert to lowercase
        normalized_email = request.email.strip().lower()

        # Find user by normalized email
        user = self.user_repository.get_by_email(normalized_email)

        # Verify user exists and password matches
        # Use same error for both cases to prevent user enumeration
        if not user or not self.verify_user_password(request.password, user.hashed_password):
            logger.warning(f"Failed login attempt: {normalized_email}")
            raise InvalidCredentialsError("Invalid email or password")

        # Generate JWT access token
        access_token = self.generate_access_token(user.id)

        # Calculate token expiration in seconds
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

        logger.info(f"User logged in: {user.id} ({normalized_email})")

        # Return login response with token and user information
        user_response = UserRegisterResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
        )

        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
            user=user_response,
        )
