"""
Configuration management for CareCompanion AI.
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Environment
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "CareCompanion AI"
    version: str = "1.0.0"
    
    # CORS Configuration
    allowed_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # File Upload Configuration
    max_file_size_mb: int = 10
    allowed_extensions: List[str] = [
        "jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"
    ]
    
    # External APIs (for future implementation)
    google_vision_api_key: str = ""
    gemini_api_key: str = ""
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
