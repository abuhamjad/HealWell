"""Authentication schemas.

Defines Pydantic models for authentication-related request/response data.
"""

from typing import Optional
from pydantic import BaseModel, Field


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
