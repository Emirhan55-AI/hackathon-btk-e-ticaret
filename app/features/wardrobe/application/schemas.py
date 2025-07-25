from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


class ClothingItemBase(BaseModel):
    """Base clothing item schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    size: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=1000)
    
    @validator('category')
    def validate_category(cls, v):
        """Validate and normalize category."""
        if v:
            v = v.lower().strip()
            # Define allowed categories
            allowed_categories = [
                'tops', 'bottoms', 'dresses', 'outerwear', 'shoes', 
                'accessories', 'activewear', 'swimwear', 'underwear'
            ]
            if v not in allowed_categories:
                # For flexibility, we'll allow any category but warn
                pass
        return v
    
    @validator('color')
    def validate_color(cls, v):
        """Validate and normalize color."""
        if v:
            v = v.lower().strip()
        return v


class ClothingItemCreate(ClothingItemBase):
    """Schema for creating clothing item."""
    pass


class ClothingItemUpdate(BaseModel):
    """Schema for updating clothing item."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    size: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=1000)
    user_tags: Optional[Dict[str, Any]] = None
    is_favorite: Optional[bool] = None


class ClothingItemResponse(ClothingItemBase):
    """Schema for clothing item response."""
    id: uuid.UUID
    user_id: uuid.UUID
    image_url: Optional[str] = None
    ai_tags: Dict[str, Any] = Field(default_factory=dict)
    user_tags: Dict[str, Any] = Field(default_factory=dict)
    is_favorite: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ClothingItemList(BaseModel):
    """Schema for clothing item list response."""
    items: List[ClothingItemResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


class AITagResponse(BaseModel):
    """Schema for AI tagging response."""
    style: Optional[str] = None
    pattern: Optional[str] = None
    material: Optional[str] = None
    fit: Optional[str] = None
    occasion: Optional[List[str]] = Field(default_factory=list)
    season: Optional[List[str]] = Field(default_factory=list)
    color_analysis: Optional[Dict[str, Any]] = Field(default_factory=dict)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    attributes: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ClothingItemUploadResponse(BaseModel):
    """Schema for upload response with AI tags."""
    id: uuid.UUID
    name: str
    category: str
    image_url: str
    ai_tags: AITagResponse
    processing_status: str = "completed"  # processing, completed, failed
    created_at: datetime


class WardrobeStats(BaseModel):
    """Schema for wardrobe statistics."""
    total_items: int
    categories: Dict[str, int]
    colors: Dict[str, int]
    brands: Dict[str, int]
    favorite_count: int
    recent_additions: int  # Last 30 days


class ClothingItemSearch(BaseModel):
    """Schema for search filters."""
    query: Optional[str] = None
    category: Optional[str] = None
    color: Optional[str] = None
    brand: Optional[str] = None
    is_favorite: Optional[bool] = None
    tags: Optional[Dict[str, Any]] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class BulkOperation(BaseModel):
    """Schema for bulk operations."""
    item_ids: List[uuid.UUID] = Field(..., min_length=1)
    operation: str = Field(..., pattern="^(delete|favorite|unfavorite|update_tags)$")
    data: Optional[Dict[str, Any]] = None


class TagUpdate(BaseModel):
    """Schema for updating tags."""
    user_tags: Dict[str, Any]
    
    @validator('user_tags')
    def validate_user_tags(cls, v):
        """Validate user tags structure."""
        if not isinstance(v, dict):
            raise ValueError("User tags must be a dictionary")
        
        # Limit the size of tags
        if len(str(v)) > 5000:  # 5KB limit
            raise ValueError("Tags data too large")
        
        return v


class ImageUpload(BaseModel):
    """Schema for image upload metadata."""
    filename: str
    content_type: str
    size: int
    
    @validator('content_type')
    def validate_content_type(cls, v):
        """Validate image content type."""
        allowed_types = [
            'image/jpeg', 'image/jpg', 'image/png', 
            'image/webp', 'image/heic', 'image/heif'
        ]
        if v.lower() not in allowed_types:
            raise ValueError(f"Unsupported image type: {v}")
        return v
    
    @validator('size')
    def validate_size(cls, v):
        """Validate image size (max 10MB)."""
        max_size = 10 * 1024 * 1024  # 10MB
        if v > max_size:
            raise ValueError(f"Image too large. Max size: {max_size} bytes")
        return v


class OutfitSuggestion(BaseModel):
    """Schema for outfit suggestions based on an item."""
    base_item_id: uuid.UUID
    suggested_items: List[ClothingItemResponse]
    occasion: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    styling_tips: List[str] = Field(default_factory=list)
