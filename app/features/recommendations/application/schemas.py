from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class GenerateOutfitRequest(BaseModel):
    """Schema for generating outfit recommendations request."""
    user_id: uuid.UUID
    style_preferences: Optional[Dict[str, Any]] = None
    occasion: Optional[str] = None
    weather: Optional[str] = None
    color_preferences: Optional[List[str]] = None

class OutfitItem(BaseModel):
    """Schema for an outfit item."""
    item_id: uuid.UUID
    name: str
    category: str
    color: str
    confidence_score: float = Field(ge=0.0, le=1.0)

class OutfitRecommendation(BaseModel):
    """Schema for a complete outfit recommendation."""
    outfit_id: uuid.UUID
    items: List[OutfitItem]
    style_tags: List[str]
    occasion: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    explanation: str

class OutfitResponse(BaseModel):
    """Schema for outfit recommendations response."""
    user_id: uuid.UUID
    recommendations: List[OutfitRecommendation]
    generated_at: datetime
    total_recommendations: int

class StyleDNAProfile(BaseModel):
    """Schema for user's style DNA profile."""
    user_id: uuid.UUID
    style_preferences: Dict[str, Any]
    color_palette: List[str]
    preferred_occasions: List[str]
    fit_preferences: Dict[str, str]
    updated_at: datetime
