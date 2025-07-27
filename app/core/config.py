from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="Aura Backend API", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    
    # Database
    database_url: str = Field(alias="DATABASE_URL")
    
    # Security
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS
    allowed_origins: Union[List[str], str] = Field(
        default=["http://localhost:3000"],
        alias="ALLOWED_ORIGINS"
    )
    
    # External Services
    ai_service_url: str = Field(default="http://localhost:8001", alias="AI_SERVICE_URL")
    ai_service_api_key: str = Field(default="dev_key", alias="AI_SERVICE_API_KEY")
    
    # E-commerce Integration
    ecommerce_api_url: str = Field(default="http://localhost:8005", alias="ECOMMERCE_API_URL")
    ecommerce_api_key: str = Field(default="dev_ecommerce_key", alias="ECOMMERCE_API_KEY")
    
    # Environment
    environment: str = Field(default="development", alias="ENVIRONMENT")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")
    
    @field_validator('allowed_origins')
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return v.split(',')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
