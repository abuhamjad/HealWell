"""Profile service for user profile management."""

import logging
from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ProfileValidationError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserProfileUpdateRequest

logger = logging.getLogger(__name__)


class ProfileService:
    """Service for authenticated user profile management.

    RESPONSIBILITY: Profile business logic and validation.

    Services enforce:
    - Field validation (height, weight, date of birth, etc.)
    - Immutable field protection
    - Data persistence via repository
    - Logging of profile changes

    Services do NOT:
    - Accept or validate authentication (dependency handles this)
    - Accept user_id from client (always from authenticated context)
    - Return sensitive fields (password, hash)
    """

    def __init__(self, session: Session):
        """Initialize profile service with database session.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.user_repository = UserRepository(session)

    def get_profile(self, user_id: UUID) -> User:
        """Get authenticated user's profile.

        SERVICE RESPONSIBILITY: Load profile for authenticated user.

        Args:
            user_id: UUID of authenticated user (from JWT).

        Returns:
            User model with all profile fields.

        Raises:
            ProfileNotFoundError: If user not found (shouldn't happen if JWT valid).
        """
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            logger.error(f"User not found for valid JWT: {user_id}")
            from app.core.exceptions import ProfileNotFoundError
            raise ProfileNotFoundError("Profile not found")

        logger.debug(f"Profile retrieved: {user_id}")
        return user

    def update_profile(
        self,
        user_id: UUID,
        request: UserProfileUpdateRequest,
    ) -> User:
        """Update authenticated user's profile.

        SERVICE RESPONSIBILITY: Validate and persist profile updates.

        PATCH semantics: Only supplied fields are updated.
        Omitted fields are left unchanged.

        Validation rules:
        - Height: 50-300 cm (if provided)
        - Weight: 10-500 kg (if provided)
        - Date of birth: Cannot be in future (if provided)

        Args:
            user_id: UUID of authenticated user (from JWT).
            request: Profile update request with optional fields.

        Returns:
            Updated User model.

        Raises:
            ProfileNotFoundError: If user not found.
            ProfileValidationError: If update validation fails.
        """
        # Load user
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            logger.error(f"User not found for update: {user_id}")
            from app.core.exceptions import ProfileNotFoundError
            raise ProfileNotFoundError("Profile not found")

        # Validate and apply updates only for supplied fields
        updated_fields = []

        if request.full_name is not None:
            user.full_name = request.full_name
            updated_fields.append("full_name")

        if request.date_of_birth is not None:
            self._validate_date_of_birth(request.date_of_birth)
            user.date_of_birth = request.date_of_birth
            updated_fields.append("date_of_birth")

        if request.gender is not None:
            user.gender = request.gender
            updated_fields.append("gender")

        if request.height_cm is not None:
            self._validate_height(request.height_cm)
            user.height_cm = request.height_cm
            updated_fields.append("height_cm")

        if request.weight_kg is not None:
            self._validate_weight(request.weight_kg)
            user.weight_kg = request.weight_kg
            updated_fields.append("weight_kg")

        # Commit changes
        self.session.commit()
        self.session.refresh(user)

        logger.info(
            f"Profile updated: user={user_id}, fields={updated_fields}"
        )

        return user

    @staticmethod
    def _validate_height(height_cm: float) -> None:
        """Validate height in centimeters.

        Args:
            height_cm: Height in centimeters.

        Raises:
            ProfileValidationError: If height is invalid.
        """
        if height_cm < 50 or height_cm > 300:
            logger.warning(f"Invalid height: {height_cm}")
            raise ProfileValidationError("Height must be between 50 cm and 300 cm")

    @staticmethod
    def _validate_weight(weight_kg: float) -> None:
        """Validate weight in kilograms.

        Args:
            weight_kg: Weight in kilograms.

        Raises:
            ProfileValidationError: If weight is invalid.
        """
        if weight_kg < 10 or weight_kg > 500:
            logger.warning(f"Invalid weight: {weight_kg}")
            raise ProfileValidationError("Weight must be between 10 kg and 500 kg")

    @staticmethod
    def _validate_date_of_birth(birth_date: date) -> None:
        """Validate date of birth.

        Args:
            birth_date: Date of birth.

        Raises:
            ProfileValidationError: If date of birth is invalid.
        """
        if birth_date > date.today():
            logger.warning(f"Invalid date of birth (future): {birth_date}")
            raise ProfileValidationError("Date of birth cannot be in the future")
