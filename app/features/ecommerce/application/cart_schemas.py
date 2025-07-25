"""Shopping cart and wishlist API schemas."""
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, validator


class CartItemSchema(BaseModel):
    """Cart item schema."""
    
    id: str = Field(..., description="Cart item ID")
    product_id: str = Field(..., description="Product ID")
    variant_id: Optional[str] = Field(None, description="Product variant ID")
    quantity: int = Field(..., ge=1, description="Item quantity")
    price_per_item: Decimal = Field(..., ge=0, description="Price per item")
    total_price: Decimal = Field(..., ge=0, description="Total price for this item")
    added_at: datetime = Field(..., description="When item was added to cart")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "id": "item-123",
                "product_id": "prod-456",
                "variant_id": "var-789",
                "quantity": 2,
                "price_per_item": 29.99,
                "total_price": 59.98,
                "added_at": "2024-01-15T10:30:00Z"
            }
        }


class ShoppingCartSchema(BaseModel):
    """Shopping cart schema."""
    
    id: str = Field(..., description="Cart ID")
    user_id: str = Field(..., description="User ID")
    items: List[CartItemSchema] = Field(default_factory=list, description="Cart items")
    total_items: int = Field(..., ge=0, description="Total number of items")
    total_amount: Decimal = Field(..., ge=0, description="Total cart amount")
    is_empty: bool = Field(..., description="Whether cart is empty")
    created_at: datetime = Field(..., description="Cart creation date")
    updated_at: datetime = Field(..., description="Last update date")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "id": "cart-123",
                "user_id": "user-456",
                "items": [
                    {
                        "id": "item-123",
                        "product_id": "prod-456",
                        "variant_id": "var-789",
                        "quantity": 2,
                        "price_per_item": 29.99,
                        "total_price": 59.98,
                        "added_at": "2024-01-15T10:30:00Z"
                    }
                ],
                "total_items": 2,
                "total_amount": 59.98,
                "is_empty": False,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class AddToCartRequest(BaseModel):
    """Add to cart request schema."""
    
    product_id: str = Field(..., min_length=1, description="Product ID to add")
    quantity: int = Field(1, ge=1, le=100, description="Quantity to add")
    variant_id: Optional[str] = Field(None, description="Product variant ID")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "product_id": "prod-456",
                "quantity": 2,
                "variant_id": "var-789"
            }
        }


class UpdateCartItemRequest(BaseModel):
    """Update cart item request schema."""
    
    quantity: int = Field(..., ge=0, le=100, description="New quantity (0 to remove)")
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Validate quantity."""
        if v < 0:
            raise ValueError('Quantity cannot be negative')
        return v
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "quantity": 3
            }
        }


class WishlistItemSchema(BaseModel):
    """Wishlist item schema."""
    
    id: str = Field(..., description="Wishlist item ID")
    product_id: str = Field(..., description="Product ID")
    added_at: datetime = Field(..., description="When item was added to wishlist")
    notes: Optional[str] = Field(None, description="Optional notes about the item")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "id": "wishlist-item-123",
                "product_id": "prod-456",
                "added_at": "2024-01-15T10:30:00Z",
                "notes": "Perfect for summer vacation"
            }
        }


class WishlistSchema(BaseModel):
    """Wishlist schema."""
    
    id: str = Field(..., description="Wishlist ID")
    user_id: str = Field(..., description="User ID")
    items: List[WishlistItemSchema] = Field(default_factory=list, description="Wishlist items")
    total_items: int = Field(..., ge=0, description="Total number of items")
    is_empty: bool = Field(..., description="Whether wishlist is empty")
    created_at: datetime = Field(..., description="Wishlist creation date")
    updated_at: datetime = Field(..., description="Last update date")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "id": "wishlist-123",
                "user_id": "user-456",
                "items": [
                    {
                        "id": "wishlist-item-123",
                        "product_id": "prod-456",
                        "added_at": "2024-01-15T10:30:00Z",
                        "notes": "Perfect for summer vacation"
                    }
                ],
                "total_items": 1,
                "is_empty": False,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class AddToWishlistRequest(BaseModel):
    """Add to wishlist request schema."""
    
    product_id: str = Field(..., min_length=1, description="Product ID to add")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes about the item")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "product_id": "prod-456",
                "notes": "Perfect for summer vacation"
            }
        }


class CartSummarySchema(BaseModel):
    """Cart summary schema for quick overview."""
    
    total_items: int = Field(..., ge=0, description="Total number of items")
    total_amount: Decimal = Field(..., ge=0, description="Total cart amount")
    currency: str = Field(default="USD", description="Currency code")
    last_updated: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "total_items": 5,
                "total_amount": 149.95,
                "currency": "USD",
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }


class WishlistSummarySchema(BaseModel):
    """Wishlist summary schema for quick overview."""
    
    total_items: int = Field(..., ge=0, description="Total number of items")
    last_updated: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "total_items": 8,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }
