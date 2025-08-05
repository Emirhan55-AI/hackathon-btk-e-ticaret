# AURA AI Configuration Management
# Centralized configuration management for all microservices

import os  # Operating system interface for environment variables
from typing import Optional, List, Dict, Any  # Type hints for better code documentation
from pydantic import BaseSettings, Field, validator  # Pydantic settings for configuration
from functools import lru_cache  # LRU cache for performance optimization

class DatabaseSettings(BaseSettings):
    """
    Database configuration settings.
    These settings control database connection and behavior across all services.
    """
    
    # PostgreSQL database connection URL
    database_url: str = Field(
        default="postgresql://aura:password@localhost:5432/aura_ai",
        description="PostgreSQL database connection URL",
        env="DATABASE_URL"  # Environment variable name
    )
    
    # Database connection pool settings
    db_pool_size: int = Field(
        default=10,
        description="Database connection pool size",
        env="DB_POOL_SIZE"
    )
    
    # Maximum overflow connections beyond pool size
    db_max_overflow: int = Field(
        default=20,
        description="Maximum overflow connections",
        env="DB_MAX_OVERFLOW"
    )
    
    # Database connection timeout in seconds
    db_timeout: int = Field(
        default=30,
        description="Database connection timeout in seconds",
        env="DB_TIMEOUT"
    )
    
    # Enable database query logging for debugging
    db_echo: bool = Field(
        default=False,
        description="Enable database query logging",
        env="DB_ECHO"
    )
    
    class Config:
        # Environment file to load settings from
        env_file = ".env"
        # Case sensitive environment variable matching
        case_sensitive = False

class RedisSettings(BaseSettings):
    """
    Redis cache configuration settings.
    These settings control Redis connection and caching behavior.
    """
    
    # Redis connection URL
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
        env="REDIS_URL"
    )
    
    # Redis connection timeout in seconds
    redis_timeout: int = Field(
        default=10,
        description="Redis connection timeout in seconds",
        env="REDIS_TIMEOUT"
    )
    
    # Maximum number of Redis connections
    redis_max_connections: int = Field(
        default=50,
        description="Maximum Redis connections",
        env="REDIS_MAX_CONNECTIONS"
    )
    
    # Default cache expiration time in seconds
    cache_ttl: int = Field(
        default=3600,  # 1 hour
        description="Default cache TTL in seconds",
        env="CACHE_TTL"
    )
    
    # Enable Redis clustering support
    redis_cluster: bool = Field(
        default=False,
        description="Enable Redis clustering",
        env="REDIS_CLUSTER"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class APISettings(BaseSettings):
    """
    API configuration settings.
    These settings control API behavior and external service integration.
    """
    
    # OpenAI API key for AI model access
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key",
        env="OPENAI_API_KEY"
    )
    
    # Hugging Face API key for model access
    huggingface_api_key: Optional[str] = Field(
        default=None,
        description="Hugging Face API key",
        env="HUGGINGFACE_API_KEY"
    )
    
    # External fashion API endpoint
    fashion_api_url: Optional[str] = Field(
        default=None,
        description="External fashion API URL",
        env="FASHION_API_URL"
    )
    
    # Weather API key for weather-based recommendations
    weather_api_key: Optional[str] = Field(
        default=None,
        description="Weather API key",
        env="WEATHER_API_KEY"
    )
    
    # API rate limiting settings
    api_rate_limit: int = Field(
        default=1000,  # Requests per hour
        description="API rate limit per hour",
        env="API_RATE_LIMIT"
    )
    
    # API request timeout in seconds
    api_timeout: int = Field(
        default=30,
        description="API request timeout in seconds",
        env="API_TIMEOUT"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class SecuritySettings(BaseSettings):
    """
    Security configuration settings.
    These settings control authentication, encryption, and security features.
    """
    
    # JWT secret key for token signing
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT secret key",
        env="JWT_SECRET_KEY"
    )
    
    # JWT token expiration time in seconds
    jwt_expiration: int = Field(
        default=3600,  # 1 hour
        description="JWT token expiration in seconds",
        env="JWT_EXPIRATION"
    )
    
    # JWT algorithm for token signing
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm",
        env="JWT_ALGORITHM"
    )
    
    # Encryption key for sensitive data
    encryption_key: Optional[str] = Field(
        default=None,
        description="Encryption key for sensitive data",
        env="ENCRYPTION_KEY"
    )
    
    # Password hashing algorithm
    password_hash_algorithm: str = Field(
        default="bcrypt",
        description="Password hashing algorithm",
        env="PASSWORD_HASH_ALGORITHM"
    )
    
    # CORS allowed origins
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins",
        env="CORS_ORIGINS"
    )
    
    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        """
        Parse CORS origins from string or list.
        This validator handles both environment variable string and list inputs.
        """
        if isinstance(v, str):
            # Split comma-separated string into list
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class LoggingSettings(BaseSettings):
    """
    Logging configuration settings.
    These settings control application logging behavior.
    """
    
    # Log level for application logging
    log_level: str = Field(
        default="INFO",
        description="Application log level",
        env="LOG_LEVEL"
    )
    
    # Log format string
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string",
        env="LOG_FORMAT"
    )
    
    # Enable JSON structured logging
    log_json: bool = Field(
        default=False,
        description="Enable JSON structured logging",
        env="LOG_JSON"
    )
    
    # Log file path for file logging
    log_file: Optional[str] = Field(
        default=None,
        description="Log file path",
        env="LOG_FILE"
    )
    
    # Maximum log file size in MB
    log_file_max_size: int = Field(
        default=100,
        description="Maximum log file size in MB",
        env="LOG_FILE_MAX_SIZE"
    )
    
    # Number of log file backups to keep
    log_file_backup_count: int = Field(
        default=5,
        description="Number of log file backups",
        env="LOG_FILE_BACKUP_COUNT"
    )
    
    @validator('log_level', pre=True)
    def validate_log_level(cls, v):
        """
        Validate that log level is valid.
        This ensures only valid log levels are used.
        """
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v.upper()
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class MonitoringSettings(BaseSettings):
    """
    Monitoring and metrics configuration settings.
    These settings control application monitoring and observability.
    """
    
    # Enable metrics collection
    enable_metrics: bool = Field(
        default=True,
        description="Enable metrics collection",
        env="ENABLE_METRICS"
    )
    
    # Metrics export endpoint
    metrics_endpoint: str = Field(
        default="/metrics",
        description="Metrics export endpoint",
        env="METRICS_ENDPOINT"
    )
    
    # Health check endpoint
    health_endpoint: str = Field(
        default="/health",
        description="Health check endpoint",
        env="HEALTH_ENDPOINT"
    )
    
    # Enable distributed tracing
    enable_tracing: bool = Field(
        default=False,
        description="Enable distributed tracing",
        env="ENABLE_TRACING"
    )
    
    # Jaeger tracing endpoint
    jaeger_endpoint: Optional[str] = Field(
        default=None,
        description="Jaeger tracing endpoint",
        env="JAEGER_ENDPOINT"
    )
    
    # Performance monitoring sample rate
    trace_sample_rate: float = Field(
        default=0.1,  # 10% sampling
        description="Trace sampling rate",
        env="TRACE_SAMPLE_RATE"
    )
    
    @validator('trace_sample_rate', pre=True)
    def validate_sample_rate(cls, v):
        """
        Validate that trace sample rate is between 0 and 1.
        This ensures valid sampling rate for performance monitoring.
        """
        rate = float(v)
        if not 0 <= rate <= 1:
            raise ValueError("Trace sample rate must be between 0 and 1")
        return rate
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class AppSettings(BaseSettings):
    """
    Main application configuration that combines all setting categories.
    This class provides a unified interface to all configuration settings.
    """
    
    # Application name and version
    app_name: str = Field(
        default="AURA AI",
        description="Application name",
        env="APP_NAME"
    )
    
    app_version: str = Field(
        default="1.0.0",
        description="Application version",
        env="APP_VERSION"
    )
    
    # Environment (development, staging, production)
    environment: str = Field(
        default="development",
        description="Application environment",
        env="ENVIRONMENT"
    )
    
    # Debug mode flag
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
        env="DEBUG"
    )
    
    # Testing mode flag
    testing: bool = Field(
        default=False,
        description="Enable testing mode",
        env="TESTING"
    )
    
    # Server host and port settings
    host: str = Field(
        default="0.0.0.0",
        description="Server host",
        env="HOST"
    )
    
    port: int = Field(
        default=8000,
        description="Server port",
        env="PORT"
    )
    
    # Worker configuration for production
    workers: int = Field(
        default=1,
        description="Number of worker processes",
        env="WORKERS"
    )
    
    # Include nested settings
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    api: APISettings = APISettings()
    security: SecuritySettings = SecuritySettings()
    logging: LoggingSettings = LoggingSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    
    @validator('environment', pre=True)
    def validate_environment(cls, v):
        """
        Validate that environment is valid.
        This ensures only valid environments are used.
        """
        valid_envs = ['development', 'staging', 'production', 'testing']
        if v.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of: {', '.join(valid_envs)}")
        return v.lower()
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == "testing" or self.testing
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow nested models to use their own env_file
        env_nested_delimiter = "__"

@lru_cache()
def get_settings() -> AppSettings:
    """
    Get application settings with caching.
    This function returns a cached instance of settings for performance.
    The @lru_cache decorator ensures settings are loaded only once.
    """
    # Create and return cached settings instance
    return AppSettings()

def get_database_url() -> str:
    """
    Get database URL from settings.
    This is a convenience function for quick database URL access.
    """
    # Get settings and return database URL
    settings = get_settings()
    return settings.database.database_url

def get_redis_url() -> str:
    """
    Get Redis URL from settings.
    This is a convenience function for quick Redis URL access.
    """
    # Get settings and return Redis URL
    settings = get_settings()
    return settings.redis.redis_url

def is_development() -> bool:
    """
    Check if application is running in development mode.
    This is a convenience function for environment checking.
    """
    # Get settings and check environment
    settings = get_settings()
    return settings.is_development

def is_production() -> bool:
    """
    Check if application is running in production mode.
    This is a convenience function for environment checking.
    """
    # Get settings and check environment
    settings = get_settings()
    return settings.is_production

def is_testing() -> bool:
    """
    Check if application is running in testing mode.
    This is a convenience function for environment checking.
    """
    # Get settings and check environment
    settings = get_settings()
    return settings.is_testing

# Environment-specific configuration overrides
def load_environment_config(env: str = None) -> Dict[str, Any]:
    """
    Load environment-specific configuration overrides.
    This function allows for environment-specific customizations.
    """
    # Use provided environment or get from settings
    if env is None:
        env = get_settings().environment
    
    # Define environment-specific overrides
    config_overrides = {
        "development": {
            "debug": True,
            "log_level": "DEBUG",
            "db_echo": True,
            "enable_metrics": True
        },
        "staging": {
            "debug": False,
            "log_level": "INFO",
            "db_echo": False,
            "enable_metrics": True,
            "enable_tracing": True
        },
        "production": {
            "debug": False,
            "log_level": "WARNING",
            "db_echo": False,
            "enable_metrics": True,
            "enable_tracing": True,
            "log_json": True
        },
        "testing": {
            "debug": True,
            "log_level": "WARNING",
            "db_echo": False,
            "enable_metrics": False,
            "testing": True
        }
    }
    
    # Return overrides for the specified environment
    return config_overrides.get(env, {})
