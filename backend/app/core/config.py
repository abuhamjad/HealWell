from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_TITLE: str = "HealWell API"
    API_VERSION: str = "0.1.0"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def allowed_origins(self) -> List[str]:
        return self.CORS_ORIGINS.split(",")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
