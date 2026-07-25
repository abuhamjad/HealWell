"""Profile routes for authenticated user profile management."""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserProfileResponse, UserProfileUpdateRequest
from app.schemas.response import ApiResponse, success_response
from app.services.profile_service import ProfileService
from app.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ApiResponse)
async def get_profile(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """Get authenticated user's profile.

    Protected endpoint - requires JWT authentication.
    Returns only the authenticated user's profile.

    Returns:
        User profile with safe fields (no password/hash).

    Raises:
        ProfileNotFoundError: If profile not found (shouldn't happen with valid JWT).
    """
    profile_service = ProfileService(session=session)

    # Service loads and returns authenticated user's profile
    user = profile_service.get_profile(current_user.id)

    # Convert to response schema (excludes sensitive fields)
    profile_response = UserProfileResponse.model_validate(user)

    return success_response(
        data=profile_response,
        message="Profile retrieved successfully",
    )


@router.patch("", response_model=ApiResponse)
async def update_profile(
    request: UserProfileUpdateRequest,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """Update authenticated user's profile.

    Protected endpoint - requires JWT authentication.
    Users can only update their own profile.

    PATCH semantics:
    - Only supplied fields are updated
    - Omitted fields remain unchanged
    - Cannot modify: id, email, username, password, created_at

    Validation:
    - Height: 50-300 cm
    - Weight: 10-500 kg
    - Date of birth: Cannot be in future

    Args:
        request: Profile update with optional fields.

    Returns:
        Updated user profile with all fields.

    Raises:
        ProfileValidationError: If update validation fails.
        ProfileNotFoundError: If profile not found.
    """
    profile_service = ProfileService(session=session)

    # Service validates and applies updates
    # Only supplied fields in request are updated
    user = profile_service.update_profile(current_user.id, request)

    # Convert to response schema
    profile_response = UserProfileResponse.model_validate(user)

    return success_response(
        data=profile_response,
        message="Profile updated successfully",
    )
