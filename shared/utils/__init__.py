# AURA AI Shared Utilities Package
# This module contains utility functions shared across all microservices

"""
Shared utility functions for AURA AI system.
These utilities provide common functionality needed across multiple microservices.
"""

# Import all utility modules to make them available when importing this package
from .logging import *  # Logging utilities and configuration
from .validation import *  # Data validation and sanitization functions
from .image_processing import *  # Image processing and manipulation utilities
from .text_processing import *  # Text processing and NLP utilities
from .date_utils import *  # Date and time manipulation utilities
from .security import *  # Security and encryption utilities

# Define what gets exported when using "from shared.utils import *"
__all__ = [
    # Logging utilities
    "get_logger",
    "setup_logging",
    "log_execution_time",
    "log_api_request",
    
    # Validation utilities
    "validate_email",
    "validate_phone",
    "validate_image",
    "validate_url",
    "sanitize_input",
    
    # Image processing utilities
    "resize_image",
    "crop_image",
    "extract_colors",
    "normalize_image",
    "image_to_base64",
    "base64_to_image",
    
    # Text processing utilities
    "clean_text",
    "extract_keywords",
    "detect_language",
    "translate_text",
    "normalize_turkish",
    
    # Date utilities
    "format_datetime",
    "parse_datetime",
    "get_timezone",
    "calculate_age",
    "time_ago",
    
    # Security utilities
    "hash_password",
    "verify_password",
    "generate_token",
    "verify_token",
    "encrypt_data",
    "decrypt_data"
]

# Package version for tracking utility changes
__version__ = "1.0.0"

# Utility category registry for organization
UTILITY_CATEGORIES = {
    "logging": ["get_logger", "setup_logging", "log_execution_time", "log_api_request"],
    "validation": ["validate_email", "validate_phone", "validate_image", "validate_url", "sanitize_input"],
    "image": ["resize_image", "crop_image", "extract_colors", "normalize_image", "image_to_base64", "base64_to_image"],
    "text": ["clean_text", "extract_keywords", "detect_language", "translate_text", "normalize_turkish"],
    "date": ["format_datetime", "parse_datetime", "get_timezone", "calculate_age", "time_ago"],
    "security": ["hash_password", "verify_password", "generate_token", "verify_token", "encrypt_data", "decrypt_data"]
}
