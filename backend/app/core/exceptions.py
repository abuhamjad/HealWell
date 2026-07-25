"""Custom exception classes for HealWell domain.

Defines domain-specific exceptions for authentication and user operations.
These exceptions provide clear semantics for error handling and logging.
"""


class HealWellException(Exception):
    """Base exception for all HealWell domain errors.

    All domain-specific exceptions inherit from this base.
    """

    pass


class AuthenticationException(HealWellException):
    """Base exception for authentication-related errors."""

    pass


class EmailAlreadyExistsError(AuthenticationException):
    """Email address is already registered.

    Raised when attempting to register with an email that already exists.
    HTTP Status: 409 Conflict
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email '{email}' is already registered")


class UsernameAlreadyExistsError(AuthenticationException):
    """Username is already registered.

    Raised when attempting to register with a username that already exists.
    HTTP Status: 409 Conflict
    """

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username '{username}' is already taken")


class InvalidCredentialsError(AuthenticationException):
    """User credentials are invalid.

    Raised during login when credentials don't match.
    HTTP Status: 401 Unauthorized
    """

    pass


class TokenExpiredError(AuthenticationException):
    """JWT token has expired.

    Raised when attempting to use an expired token.
    HTTP Status: 401 Unauthorized
    """

    pass


class InvalidTokenError(AuthenticationException):
    """JWT token is invalid or corrupted.

    Raised when token signature or structure is invalid.
    HTTP Status: 401 Unauthorized
    """

    pass


class ResourceNotFoundError(HealWellException):
    """Requested resource was not found.

    Base exception for resource not found errors.
    HTTP Status: 404 Not Found
    """

    pass


class AnalysisNotFoundError(ResourceNotFoundError):
    """Analysis resource was not found or doesn't belong to user.

    Raised when attempting to access an analysis that:
    - Does not exist, OR
    - Does not belong to the requesting user

    Same error for both cases (no information leakage about existence).
    HTTP Status: 404 Not Found
    """

    pass


class ProfileNotFoundError(ResourceNotFoundError):
    """User profile was not found.

    Raised when attempting to access or modify a user profile that:
    - Does not exist

    HTTP Status: 404 Not Found
    """

    pass


class ProfileValidationError(HealWellException):
    """Profile update validation failed.

    Raised when profile update contains invalid values:
    - Height out of range
    - Weight out of range
    - Date of birth in future
    - etc.

    HTTP Status: 422 Unprocessable Entity
    """

    pass
