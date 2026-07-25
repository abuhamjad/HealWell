"""User profile schemas."""

from typing import Optional
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field


class UserProfileResponse(BaseModel):
    """User profile response - safe fields only.

    Never includes:
    - password
    - hashed_password
    - JWT tokens
    """

    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
    full_name: Optional[str] = Field(None, description="Full legal name")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    height_cm: Optional[float] = Field(None, description="Height in centimeters")
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class UserProfileUpdateRequest(BaseModel):
    """User profile update request.

    PATCH semantics: All fields are optional.
    Only supplied fields are updated.
    Omitted fields remain unchanged.

    Never allows modification of:
    - id
    - email
    - username
    - created_at
    - password
    """

    full_name: Optional[str] = Field(
        None,
        description="Full legal name",
        max_length=255,
    )
    date_of_birth: Optional[date] = Field(
        None,
        description="Date of birth (cannot be in future)",
    )
    gender: Optional[str] = Field(
        None,
        description="Gender",
        max_length=20,
    )
    height_cm: Optional[float] = Field(
        None,
        description="Height in centimeters (50-300)",
        ge=50,
        le=300,
    )
    weight_kg: Optional[float] = Field(
        None,
        description="Weight in kilograms (10-500)",
        ge=10,
        le=500,
    )
