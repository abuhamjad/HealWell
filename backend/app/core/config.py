"""Application configuration and settings.

This module loads and manages all configuration from environment variables.
Settings are hierarchical: .env file → environment variables → defaults

Supports three environments:
- development: Local development with full debugging
- staging: Staging deployment with production-like settings
- production: Production deployment with strict security
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    """Production-ready settings with environment-specific configuration.

    Load order: .env file → environment variables → defaults
    """

    # ========== CORE CONFIGURATION ==========
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True
    API_TITLE: str = "HealWell API"
    API_VERSION: str = "0.6.0"

    # ========== DEPLOYMENT ==========
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ========== FRONTEND URLS ==========
    FRONTEND_URL: str = "http://localhost:5173"
    FRONTEND_STAGING_URL: str = "http://localhost:5173"
    FRONTEND_PRODUCTION_URL: str = "https://healwell.vercel.app"

    # ========== CORS CONFIGURATION ==========
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,http://192.168.1.6:5173"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # ========== API CONFIGURATION ==========
    API_HEALTH_CHECK_PATH: str = "/health"
    API_PREFIX: str = "/api/v1"

    # ========== AI/GEMINI CONFIGURATION (v0.7+) ==========
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    AI_TIMEOUT: int = 30
    AI_MAX_RETRIES: int = 3
    AI_TEMPERATURE: float = 0.7

    # ========== DATABASE CONFIGURATION (v0.9+) ==========
    DATABASE_URL: str = ""
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # ========== LOGGING CONFIGURATION ==========
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json | text

    # ========== PYDANTIC CONFIGURATION ==========
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",  # Allow extra fields for forward compatibility
        validate_default=True,
    )

    # ========== ENVIRONMENT PROPERTIES ==========
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging environment."""
        return self.ENVIRONMENT == "staging"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    # ========== FRONTEND URL SELECTION ==========
    @property
    def current_frontend_url(self) -> str:
        """Get frontend URL for current environment."""
        if self.is_production:
            return self.FRONTEND_PRODUCTION_URL
        elif self.is_staging:
            return self.FRONTEND_STAGING_URL
        else:
            return self.FRONTEND_URL

    # ========== CORS MANAGEMENT ==========
    @property
    def allowed_origins(self) -> List[str]:
        """Parse and validate CORS origins based on environment.

        Development: Allows localhost, 127.0.0.1, and private LAN addresses.
        Production: Only configured domains (no localhost/private IPs).
        """
        origins = [o.strip().rstrip("/") for o in self.CORS_ORIGINS.split(",") if o.strip()]

        # In production, filter to only configured domains (remove localhost/private)
        if self.is_production:
            origins = [
                o for o in origins
                if not any(
                    private in o
                    for private in ["localhost", "127.0.0.1", "192.168", "10.", "172."]
                )
            ]

        return origins

    @property
    def cors_allow_origin_regex(self) -> Optional[str]:
        """Return regex pattern for CORS allow_origin in development.

        In production, returns None (use strict allow_origins list instead).
        In development, allows:
        - localhost:port
        - 127.0.0.1:port
        - 192.168.x.x:port (private LAN)
        - 10.x.x.x:port (private network)
        """
        if self.is_production:
            return None  # Production uses strict allow_origins list only

        if self.is_development:
            # Allow localhost, 127.0.0.1, and private networks in development
            return (
                r"^https?://(localhost|127\.0\.0\.1|"
                r"192\.168\.\d{1,3}\.\d{1,3}|"
                r"10\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?/?$"
            )

        return None


# Load settings singleton at module import
settings = Settings()
