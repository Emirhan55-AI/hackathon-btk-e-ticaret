"""E-commerce API schemas."""
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, validator


class ProductImageSchema(BaseModel):
    """Product image schema."""
    
    url: str = Field(..., description="Image URL")
    alt_text: Optional[str] = Field(None, description="Alt text for accessibility")
    is_primary: bool = Field(False, description="Whether this is the primary image")


class ProductVariantSchema(BaseModel):
    """Product variant schema."""
    
    id: str = Field(..., description="Variant ID")
    name: str = Field(..., description="Variant name (e.g., 'size', 'color')")
    value: str = Field(..., description="Variant value (e.g., 'Large', 'Red')")
    price_modifier: Decimal = Field(Decimal('0.00'), description="Price modifier for this variant")
    available: bool = Field(True, description="Whether this variant is available")


class ProductReviewSchema(BaseModel):
    """Product review schema."""
    
    id: str = Field(..., description="Review ID")
    user_id: str = Field(..., description="User ID who wrote the review")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: Optional[str] = Field(None, description="Review comment")
    verified_purchase: bool = Field(False, description="Whether this is a verified purchase")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Review creation timestamp")


class ProductSchema(BaseModel):
    """Product schema."""
    
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    brand: str = Field(..., description="Product brand")
    category: str = Field(..., description="Product category")
    price: Decimal = Field(..., gt=0, description="Current price")
    original_price: Optional[Decimal] = Field(None, description="Original price (if discounted)")
    currency: str = Field("USD", description="Currency code")
    images: List[ProductImageSchema] = Field(default_factory=list, description="Product images")
    variants: List[ProductVariantSchema] = Field(default_factory=list, description="Product variants")
    tags: List[str] = Field(default_factory=list, description="Product tags")
    available: bool = Field(True, description="Whether product is available")
    stock_quantity: Optional[int] = Field(None, description="Stock quantity")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")
    review_count: int = Field(0, ge=0, description="Number of reviews")
    reviews: List[ProductReviewSchema] = Field(default_factory=list, description="Product reviews")
    external_url: Optional[str] = Field(None, description="External product URL")
    affiliate_link: Optional[str] = Field(None, description="Affiliate link")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    @validator('original_price')
    def validate_original_price(cls, v, values):
        """Validate that original price is greater than current price if provided."""
        if v is not None and 'price' in values and v <= values['price']:
            raise ValueError('Original price must be greater than current price')
        return v
    
    class Config:
        """Pydantic config."""
        
        json_encoders = {
            Decimal: lambda v: float(v),
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "id": "prod_123",
                "name": "Stylish Summer Dress",
                "description": "A beautiful summer dress perfect for any occasion",
                "brand": "Fashion Brand",
                "category": "Dresses",
                "price": 89.99,
                "original_price": 119.99,
                "currency": "USD",
                "images": [
                    {
                        "url": "https://example.com/dress1.jpg",
                        "alt_text": "Front view of summer dress",
                        "is_primary": True
                    }
                ],
                "variants": [
                    {
                        "id": "var_size_m",
                        "name": "size",
                        "value": "Medium",
                        "price_modifier": 0.00,
                        "available": True
                    }
                ],
                "tags": ["summer", "casual", "dress"],
                "available": True,
                "stock_quantity": 15,
                "rating": 4.5,
                "review_count": 42,
                "external_url": "https://store.example.com/dress-123",
                "affiliate_link": "https://affiliate.example.com/dress-123"
            }
        }


class ProductSearchFiltersSchema(BaseModel):
    """Product search filters schema."""
    
    category: Optional[str] = Field(None, description="Filter by category")
    brand: Optional[str] = Field(None, description="Filter by brand")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Maximum price filter")
    sizes: List[str] = Field(default_factory=list, description="Filter by sizes")
    colors: List[str] = Field(default_factory=list, description="Filter by colors")
    tags: List[str] = Field(default_factory=list, description="Filter by tags")
    available_only: bool = Field(True, description="Show only available products")
    has_discount: Optional[bool] = Field(None, description="Filter by discount availability")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating filter")
    sort_by: str = Field("relevance", description="Sort order")
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        """Validate sort_by field."""
        allowed_values = ["relevance", "price_low", "price_high", "rating", "newest"]
        if v not in allowed_values:
            raise ValueError(f'sort_by must be one of: {", ".join(allowed_values)}')
        return v
    
    @validator('max_price')
    def validate_price_range(cls, v, values):
        """Validate that max_price is greater than min_price."""
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v <= values['min_price']:
                raise ValueError('max_price must be greater than min_price')
        return v


class ProductSearchResultSchema(BaseModel):
    """Product search result schema."""
    
    products: List[ProductSchema] = Field(..., description="List of products")
    total_count: int = Field(..., ge=0, description="Total number of products matching filters")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Number of products per page")
    total_pages: int = Field(..., ge=1, description="Total number of pages")
    filters_applied: ProductSearchFiltersSchema = Field(..., description="Filters that were applied")
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "products": [
                    {
                        "id": "prod_123",
                        "name": "Stylish Summer Dress",
                        "description": "A beautiful summer dress",
                        "brand": "Fashion Brand",
                        "category": "Dresses",
                        "price": 89.99,
                        "currency": "USD",
                        "available": True,
                        "rating": 4.5,
                        "review_count": 42
                    }
                ],
                "total_count": 156,
                "page": 1,
                "page_size": 20,
                "total_pages": 8,
                "filters_applied": {
                    "category": "Dresses",
                    "available_only": True,
                    "sort_by": "relevance"
                }
            }
        }


class ProductSearchRequest(BaseModel):
    """Product search request schema."""
    
    query: str = Field(..., min_length=1, description="Search query")
    filters: ProductSearchFiltersSchema = Field(default_factory=ProductSearchFiltersSchema, description="Search filters")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Number of products per page")
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "query": "summer dress",
                "filters": {
                    "category": "Dresses",
                    "min_price": 50.00,
                    "max_price": 200.00,
                    "available_only": True,
                    "sort_by": "price_low"
                },
                "page": 1,
                "page_size": 20
            }
        }


class ProductRecommendationRequest(BaseModel):
    """Product recommendation request schema."""
    
    user_id: str = Field(..., description="User ID for personalized recommendations")
    category: Optional[str] = Field(None, description="Specific category for recommendations")
    limit: int = Field(10, ge=1, le=50, description="Number of recommendations to return")
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "user_id": "user_123",
                "category": "Tops",
                "limit": 10
            }
        }


class TrendingProductsRequest(BaseModel):
    """Trending products request schema."""
    
    category: Optional[str] = Field(None, description="Filter by category")
    time_period: str = Field("week", description="Time period for trending calculation")
    limit: int = Field(20, ge=1, le=100, description="Number of trending products to return")
    
    @validator('time_period')
    def validate_time_period(cls, v):
        """Validate time_period field."""
        allowed_values = ["day", "week", "month", "year"]
        if v not in allowed_values:
            raise ValueError(f'time_period must be one of: {", ".join(allowed_values)}')
        return v
    
    class Config:
        """Pydantic config."""
        
        schema_extra = {
            "example": {
                "category": "Tops",
                "time_period": "week",
                "limit": 20
            }
        }
