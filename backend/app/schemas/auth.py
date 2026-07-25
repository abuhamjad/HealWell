"""Authentication schemas.

Defines Pydantic models for authentication-related request/response data.
"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """User registration request.

    Contains credentials for new user account creation.
    """

    email: EmailStr = Field(
        ...,
        description="Valid email address (must be unique)",
        min_length=5,
        max_length=255,
    )
    username: str = Field(
        ...,
        description="Username (must be unique)",
        min_length=3,
        max_length=50,
    )
    password: str = Field(
        ...,
        description="Password (min 8 chars, uppercase, lowercase, digit, special char)",
        min_length=8,
        max_length=128,
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate and normalize username."""
        v = v.strip()
        if not v:
            raise ValueError("Username cannot be empty")
        if not v.isascii():
            raise ValueError("Username must contain ASCII characters only")
        if not (v[0].isalpha()):
            raise ValueError("Username must start with a letter")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength requirements."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserRegisterResponse(BaseModel):
    """User registration response.

    Contains only safe user information. Never includes password or hash.
    """

    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT access token response.

    Returned after successful authentication.
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")


class TokenData(BaseModel):
    """Decoded JWT token data.

    Contains claims extracted from a valid JWT token.
    """

    subject: Optional[str] = Field(
        None,
        description="User ID from 'sub' claim",
        alias="sub",
    )

    class Config:
        populate_by_name = True
