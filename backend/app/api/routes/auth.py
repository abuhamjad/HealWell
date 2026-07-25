"""Authentication routes.

Handles user registration, login, token refresh, and related auth operations.

Exception Handling:
Routes delegate to services which raise domain exceptions.
Global exception handlers in app/core/exception_handlers.py
convert domain exceptions to HTTP responses.
Routes should NOT catch exceptions - let them bubble.
"""

import logging
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.schemas.auth import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse
from app.schemas.response import ApiResponse, success_response
from app.services.auth_service import AuthService
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=ApiResponse, status_code=201)
async def register_user(
    request: UserRegisterRequest,
    response: Response,
    session: Session = Depends(get_db),
) -> ApiResponse:
    """Register a new user account.

    Delegates to AuthService which handles business logic.
    If registration fails (duplicate email/username), AuthService raises
    domain exceptions that are handled by global exception handlers.

    Email Normalization:
    - Trimmed of whitespace
    - Converted to lowercase
    - Checked for uniqueness (case-insensitive)

    Username Normalization:
    - Trimmed of whitespace
    - Case preserved (case-sensitive check)

    Password is hashed before storage using Argon2.

    Success Response:
    - HTTP 201 Created
    - Location header: /api/v1/users/{user_id}
    - Body: UserRegisterResponse (safe, no password/hash)

    Args:
        request: User registration request (email, username, password)
        response: FastAPI Response object for adding headers
        session: Database session (dependency-injected)

    Returns:
        ApiResponse with UserRegisterResponse containing user id, email, username, created_at

    Raises:
        EmailAlreadyExistsError: Caught by global handler → HTTP 409
        UsernameAlreadyExistsError: Caught by global handler → HTTP 409
        Unexpected Exception: Caught by global handler → HTTP 500
    """
    # Initialize service with dependency-injected session
    auth_service = AuthService(session=session)

    # Delegate to service layer for registration business logic.
    # If email/username already exists, service raises domain exceptions.
    # Global exception handlers convert exceptions to HTTP responses.
    user_response = auth_service.register_user(request)

    # Add Location header for REST compliance (points to future user resource)
    response.headers["Location"] = f"/api/v1/users/{user_response.id}"

    # Return successful response with 201 status
    return success_response(
        data=user_response,
        message="User registered successfully",
    )


@router.post("/login", response_model=ApiResponse, status_code=200)
async def login_user(
    request: UserLoginRequest,
    session: Session = Depends(get_db),
) -> ApiResponse:
    """Authenticate user and return JWT access token.

    Email Normalization:
    - Trimmed of whitespace
    - Converted to lowercase

    Password Verification:
    - Uses Argon2 constant-time comparison
    - Prevents timing attacks

    Security:
    - Never reveals if email exists or password incorrect
    - Always returns same error message
    - Prevents user enumeration

    Success Response:
    - HTTP 200 OK
    - Body: UserLoginResponse with access_token, token_type, expires_in, user

    Args:
        request: User login request (email, password)
        session: Database session (dependency-injected)

    Returns:
        ApiResponse with UserLoginResponse containing JWT and user info

    Raises:
        InvalidCredentialsError: Caught by global handler → HTTP 401
        Unexpected Exception: Caught by global handler → HTTP 500
    """
    # Initialize service with dependency-injected session
    auth_service = AuthService(session=session)

    # Delegate to service layer for login business logic.
    # If authentication fails, service raises InvalidCredentialsError.
    # Global exception handlers convert to HTTP 401.
    login_response = auth_service.login_user(request)

    # Return successful response with 200 status
    return success_response(
        data=login_response,
        message="Login successful",
    )
