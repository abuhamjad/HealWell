from fastapi import APIRouter
from app.api.routes import analysis, history, doctors, auth

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(analysis.router)
api_router.include_router(history.router)
api_router.include_router(doctors.router)
