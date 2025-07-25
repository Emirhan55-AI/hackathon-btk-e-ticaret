from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid


class QuizResponseSchema(BaseModel):
    """Schema for quiz response data."""
    
    quiz_responses: Dict[str, Any] = Field(
        ..., 
        description="User's responses to style quiz questions"
    )
    
    @validator('quiz_responses')
    def validate_quiz_responses(cls, v):
        """Validate quiz responses are not empty."""
        if not v:
            raise ValueError("Quiz responses cannot be empty")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "quiz_responses": {
                    "style_preference": "minimalist",
                    "color_preferences": ["black", "white", "gray"],
                    "lifestyle": "professional",
                    "body_type": "rectangle",
                    "budget_range": "medium",
                    "occasion_frequency": {
                        "work": 5,
                        "casual": 7,
                        "formal": 2
                    }
                }
            }
        }


class StyleDNAResponse(BaseModel):
    """Schema for StyleDNA response data."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    quiz_responses: Dict[str, Any]
    style_profile: Dict[str, Any]
    preferred_styles: List[str]
    preferred_colors: List[str]
    lifestyle_factors: Dict[str, Any]
    version: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "quiz_responses": {
                    "style_preference": "minimalist",
                    "color_preferences": ["black", "white", "gray"]
                },
                "style_profile": {
                    "dominant_style": "minimalist",
                    "secondary_style": "classic",
                    "style_confidence": 0.85
                },
                "preferred_styles": ["minimalist", "classic"],
                "preferred_colors": ["black", "white", "gray"],
                "lifestyle_factors": {
                    "activity_level": "high",
                    "work_environment": "office"
                },
                "version": "1.0",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class StyleDNAUpdateSchema(BaseModel):
    """Schema for updating StyleDNA profile."""
    
    preferred_styles: Optional[List[str]] = Field(None, description="Updated preferred styles")
    preferred_colors: Optional[List[str]] = Field(None, description="Updated preferred colors")
    lifestyle_factors: Optional[Dict[str, Any]] = Field(None, description="Updated lifestyle factors")
    
    class Config:
        schema_extra = {
            "example": {
                "preferred_styles": ["minimalist", "bohemian"],
                "preferred_colors": ["navy", "beige", "white"],
                "lifestyle_factors": {
                    "activity_level": "medium",
                    "work_environment": "hybrid"
                }
            }
        }


class StyleDNABasicResponse(BaseModel):
    """Basic StyleDNA response schema for summary views."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    dominant_style: str
    preferred_colors: List[str]
    style_confidence: float
    version: str
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class QuizSubmissionResponse(BaseModel):
    """Response schema for quiz submission."""
    
    success: bool
    message: str
    style_dna: StyleDNAResponse
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Style quiz processed successfully",
                "style_dna": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "quiz_responses": {},
                    "style_profile": {},
                    "preferred_styles": [],
                    "preferred_colors": [],
                    "lifestyle_factors": {},
                    "version": "1.0",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
            }
        }
