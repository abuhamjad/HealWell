from pydantic import BaseModel
from typing import List


class Doctor(BaseModel):
    id: str
    name: str
    specialty: str
    hospital: str
    distance: str
    rating: float
    available: bool


class DoctorsResponse(BaseModel):
    doctors: List[Doctor]
    count: int
