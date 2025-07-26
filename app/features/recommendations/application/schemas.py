from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class GenerateOutfitRequest(BaseModel):
    """Schema for generating outfit recommendations request."""
    user_id: Optional[uuid.UUID] = None  # Will be set by the router
    occasion: Optional[str] = Field(None, description="Occasion for the outfit (e.g., work, casual, formal)")
    season: Optional[str] = Field(None, description="Season for the outfit (e.g., spring, summer, fall, winter)")
    weather: Optional[str] = Field(None, description="Weather conditions (e.g., sunny, rainy, cold)")
    color_preferences: Optional[List[str]] = Field(None, description="Preferred colors for the outfit")
    style_preferences: Optional[List[str]] = Field(None, description="Preferred styles")
    
    class Config:
        schema_extra = {
            "example": {
                "occasion": "work",
                "season": "fall",
                "weather": "cool",
                "color_preferences": ["navy", "gray", "white"],
                "style_preferences": ["professional", "minimalist"]
            }
        }


class OutfitItemResponse(BaseModel):
    """Schema for an outfit item in response."""
    id: uuid.UUID
    name: str
    category: str
    color: str
    style: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="AI confidence in this item choice")
    
    class Config:
        from_attributes = True


class OutfitSummary(BaseModel):
    """Schema for outfit summary information."""
    id: uuid.UUID
    name: str
    occasion: Optional[str]
    season: Optional[str]
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    styling_tips: List[str] = Field(default_factory=list)
    is_ai_generated: bool = True
    item_count: int
    
    class Config:
        from_attributes = True


class OutfitResponse(BaseModel):
    """Schema for outfit recommendations response."""
    user_id: uuid.UUID
    outfits: List[OutfitSummary]
    generated_at: datetime
    total_recommendations: int
    request_context: Optional[Dict[str, Any]] = Field(None, description="Context of the request")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "outfits": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "name": "Professional Fall Look",
                        "occasion": "work",
                        "season": "fall",
                        "confidence_score": 0.85,
                        "styling_tips": ["Pair with comfortable heels", "Add a light cardigan"],
                        "is_ai_generated": True,
                        "item_count": 4
                    }
                ],
                "generated_at": "2024-01-01T12:00:00Z",
                "total_recommendations": 1,
                "request_context": {
                    "occasion": "work",
                    "season": "fall",
                    "weather": "cool"
                }
            }
        }


class QuickRecommendationRequest(BaseModel):
    """Schema for quick recommendation request."""
    occasion: Optional[str] = Field(None, description="Occasion for the outfit")
    weather: Optional[str] = Field(None, description="Weather conditions")
    
    class Config:
        schema_extra = {
            "example": {
                "occasion": "casual",
                "weather": "warm"
            }
        }


class RecommendationErrorResponse(BaseModel):
    """Schema for recommendation error response."""
    error: str
    message: str
    suggestion: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "error": "NO_STYLE_DNA",
                "message": "User has not completed the style quiz",
                "suggestion": "Please complete the style quiz first to get personalized recommendations"
            }
        }
