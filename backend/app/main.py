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

# Configure CORS with environment-specific settings
cors_config = dict(
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Use regex pattern for development, strict list for production
if settings.cors_allow_origin_regex:
    cors_config["allow_origin_regex"] = settings.cors_allow_origin_regex
else:
    cors_config["allow_origins"] = settings.allowed_origins

app.add_middleware(CORSMiddleware, **cors_config)

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
