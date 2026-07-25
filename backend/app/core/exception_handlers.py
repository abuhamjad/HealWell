"""Global exception handlers for HealWell.

Centralizes all exception handling for the entire application.
Routes raise domain exceptions; handlers convert to HTTP responses.

This module defines exception handlers that are registered with FastAPI
at application startup. Handlers provide consistent error response format
across all endpoints.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    InvalidCredentialsError,
    TokenExpiredError,
    InvalidTokenError,
    AuthenticationException,
    ResourceNotFoundError,
    AnalysisNotFoundError,
    ProfileNotFoundError,
    ProfileValidationError,
    HealWellException,
)

logger = logging.getLogger(__name__)


def create_error_response(
    success: bool = False,
    code: str = "ERROR",
    message: str = "An error occurred",
) -> dict:
    """Create a standardized error response.

    Args:
        success: Whether the request succeeded (always False for errors)
        code: Error code for client-side handling
        message: Human-readable error message

    Returns:
        Dictionary with standardized error format
    """
    return {
        "success": success,
        "error": {
            "code": code,
            "message": message,
        },
    }


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with FastAPI application.

    Called during application startup to configure global exception handling.

    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(EmailAlreadyExistsError)
    async def handle_email_already_exists(
        request: Request,
        exc: EmailAlreadyExistsError,
    ) -> JSONResponse:
        """Handle email already registered errors (HTTP 409)."""
        logger.warning(f"Email registration conflict: {exc.email}")
        return JSONResponse(
            status_code=409,
            content=create_error_response(
                code="EMAIL_ALREADY_EXISTS",
                message=str(exc),
            ),
        )

    @app.exception_handler(UsernameAlreadyExistsError)
    async def handle_username_already_exists(
        request: Request,
        exc: UsernameAlreadyExistsError,
    ) -> JSONResponse:
        """Handle username already taken errors (HTTP 409)."""
        logger.warning(f"Username registration conflict: {exc.username}")
        return JSONResponse(
            status_code=409,
            content=create_error_response(
                code="USERNAME_ALREADY_EXISTS",
                message=str(exc),
            ),
        )

    @app.exception_handler(InvalidCredentialsError)
    async def handle_invalid_credentials(
        request: Request,
        exc: InvalidCredentialsError,
    ) -> JSONResponse:
        """Handle invalid login credentials (HTTP 401)."""
        logger.warning(f"Invalid credentials attempt for: {request.url.path}")
        return JSONResponse(
            status_code=401,
            content=create_error_response(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
            ),
        )

    @app.exception_handler(TokenExpiredError)
    async def handle_token_expired(
        request: Request,
        exc: TokenExpiredError,
    ) -> JSONResponse:
        """Handle expired token errors (HTTP 401)."""
        logger.warning("Access attempt with expired token")
        return JSONResponse(
            status_code=401,
            content=create_error_response(
                code="TOKEN_EXPIRED",
                message="Your session has expired. Please log in again.",
            ),
        )

    @app.exception_handler(InvalidTokenError)
    async def handle_invalid_token(
        request: Request,
        exc: InvalidTokenError,
    ) -> JSONResponse:
        """Handle invalid token errors (HTTP 401)."""
        logger.warning("Access attempt with invalid token")
        return JSONResponse(
            status_code=401,
            content=create_error_response(
                code="INVALID_TOKEN",
                message="Invalid authentication token",
            ),
        )

    @app.exception_handler(AuthenticationException)
    async def handle_authentication_exception(
        request: Request,
        exc: AuthenticationException,
    ) -> JSONResponse:
        """Handle generic authentication errors (HTTP 401)."""
        logger.warning(f"Authentication error: {str(exc)}")
        return JSONResponse(
            status_code=401,
            content=create_error_response(
                code="AUTHENTICATION_ERROR",
                message="Authentication failed",
            ),
        )

    @app.exception_handler(ProfileValidationError)
    async def handle_profile_validation_error(
        request: Request,
        exc: ProfileValidationError,
    ) -> JSONResponse:
        """Handle profile validation errors (HTTP 422).

        Invalid profile data (height, weight, date of birth, etc.).
        """
        logger.warning(f"Profile validation error: {str(exc)}")
        return JSONResponse(
            status_code=422,
            content=create_error_response(
                code="PROFILE_VALIDATION_ERROR",
                message=str(exc),
            ),
        )

    @app.exception_handler(ProfileNotFoundError)
    async def handle_profile_not_found(
        request: Request,
        exc: ProfileNotFoundError,
    ) -> JSONResponse:
        """Handle profile not found errors (HTTP 404)."""
        logger.warning(f"Profile not found: {request.url.path}")
        return JSONResponse(
            status_code=404,
            content=create_error_response(
                code="PROFILE_NOT_FOUND",
                message="Profile not found",
            ),
        )

    @app.exception_handler(AnalysisNotFoundError)
    async def handle_analysis_not_found(
        request: Request,
        exc: AnalysisNotFoundError,
    ) -> JSONResponse:
        """Handle analysis not found errors (HTTP 404).

        Covers both:
        - Analysis doesn't exist
        - Analysis doesn't belong to authenticated user

        Same error for both cases (no information leakage about existence).
        """
        logger.warning(f"Analysis not found or unauthorized access: {request.url.path}")
        return JSONResponse(
            status_code=404,
            content=create_error_response(
                code="ANALYSIS_NOT_FOUND",
                message="Analysis not found",
            ),
        )

    @app.exception_handler(ResourceNotFoundError)
    async def handle_resource_not_found(
        request: Request,
        exc: ResourceNotFoundError,
    ) -> JSONResponse:
        """Handle generic resource not found errors (HTTP 404)."""
        logger.warning(f"Resource not found: {request.url.path}")
        return JSONResponse(
            status_code=404,
            content=create_error_response(
                code="NOT_FOUND",
                message="Resource not found",
            ),
        )

    @app.exception_handler(HealWellException)
    async def handle_domain_exception(
        request: Request,
        exc: HealWellException,
    ) -> JSONResponse:
        """Handle generic domain errors (HTTP 400)."""
        logger.warning(f"Domain error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content=create_error_response(
                code="DOMAIN_ERROR",
                message=str(exc),
            ),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle all unexpected exceptions (HTTP 500).

        Logs full stack trace for debugging but does not expose details to client.
        """
        logger.exception(f"Unexpected exception at {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content=create_error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred. Please try again later.",
            ),
        )
