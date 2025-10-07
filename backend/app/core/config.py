"""
Application configuration using environment variables
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Fintech Intelligence Platform"
    VERSION: str = "0.1.0"

    # API Keys (from .env)
    FINPREP_API_KEY: str
    ALPHAVANTAGE_API_KEY: str
    MARKETAUX_API_KEY: str

    # Database
    DATABASE_URL: str = "postgresql://localhost:5432/fintech_tracker"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://fintech-tracker.vercel.app"
    ]

    # Redis (for caching and task queue)
    REDIS_URL: str = "redis://localhost:6379"

    # API Settings
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = "../.env"
        case_sensitive = True


settings = Settings()
