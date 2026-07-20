from fastapi import APIRouter
from app.schemas.doctor import DoctorsResponse

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("", response_model=DoctorsResponse)
async def get_nearby_doctors(
    latitude: float = None,
    longitude: float = None,
    specialty: str = None,
    radius_km: float = 5.0
):
    """
    Find nearby healthcare providers.

    Placeholder endpoint - returns mock data.
    """
    return {
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
