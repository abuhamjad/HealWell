from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.constants import API_TITLE, API_VERSION
from app.api.router import api_router
from app.schemas.response import ApiResponse, success_response

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.get("/", response_model=ApiResponse)
async def root():
    """Root endpoint - API health check."""
    root_data = {
        "api": API_TITLE,
        "version": API_VERSION,
        "status": "running"
    }
    return success_response(message="HealWell API is running", data=root_data)


@app.get("/health", response_model=ApiResponse)
async def health_check():
    """Health check endpoint."""
    health_data = {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
    return success_response(message="API is healthy", data=health_data)
