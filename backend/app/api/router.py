from fastapi import APIRouter
from app.api.routes import analysis

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(analysis.router)
