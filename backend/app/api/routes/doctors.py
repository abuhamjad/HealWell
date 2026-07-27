from fastapi import APIRouter
from app.schemas.response import ApiResponse, success_response
from app.core.constants import SUCCESS_DOCTORS_FOUND, DEFAULT_DOCTOR_RADIUS
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["doctors"])
doctor_service = DoctorService()


@router.get("", response_model=ApiResponse)
async def get_nearby_doctors(
    latitude: float = None,
    longitude: float = None,
    specialty: str = None,
    radius_km: float = DEFAULT_DOCTOR_RADIUS
):
    """
    Find nearby healthcare providers.

    Delegates to DoctorService.
    """
    # Delegate to service layer
    result = await doctor_service.find_nearby(
        latitude=latitude,
        longitude=longitude,
        specialty=specialty,
        radius_km=radius_km,
    )

    # Mock return for now - will integrate with database and geolocation
    doctors_data = {
        "doctors": [
            {
                "id": "doctor_001",
                "name": "Dr. Sarah Chen",
                "specialty": "General Physician",
                "hospital": "Apollo Hospitals",
                "distance": "0.8 km",
                "rating": 4.9,
                "available": True
            },
            {
                "id": "doctor_002",
                "name": "Dr. Rajesh Kumar",
                "specialty": "Internal Medicine",
                "hospital": "Fortis Healthcare",
                "distance": "1.4 km",
                "rating": 4.7,
                "available": True
            }
        ],
        "count": 2
    }
    return success_response(message=SUCCESS_DOCTORS_FOUND, data=doctors_data)
