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
