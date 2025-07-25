"""E-commerce domain entities."""
from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime


@dataclass
class ProductImage:
    """Product image entity."""
    
    url: str
    alt_text: Optional[str] = None
    is_primary: bool = False


@dataclass
class ProductVariant:
    """Product variant entity (size, color, etc.)."""
    
    id: str
    name: str
    value: str
    price_modifier: Decimal = Decimal('0.00')
    available: bool = True


@dataclass
class ProductReview:
    """Product review entity."""
    
    id: str
    user_id: str
    rating: int  # 1-5 stars
    comment: Optional[str] = None
    verified_purchase: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Product:
    """E-commerce product entity."""
    
    id: str
    name: str
    description: str
    brand: str
    category: str
    price: Decimal
    original_price: Optional[Decimal] = None
    currency: str = "USD"
    images: List[ProductImage] = field(default_factory=list)
    variants: List[ProductVariant] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    available: bool = True
    stock_quantity: Optional[int] = None
    rating: Optional[float] = None
    review_count: int = 0
    reviews: List[ProductReview] = field(default_factory=list)
    external_url: Optional[str] = None
    affiliate_link: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def has_discount(self) -> bool:
        """Check if product has a discount."""
        return (
            self.original_price is not None 
            and self.original_price > self.price
        )
    
    @property
    def discount_percentage(self) -> Optional[float]:
        """Calculate discount percentage."""
        if not self.has_discount or not self.original_price:
            return None
        
        discount = self.original_price - self.price
        return float((discount / self.original_price) * 100)
    
    @property
    def primary_image(self) -> Optional[ProductImage]:
        """Get primary product image."""
        for image in self.images:
            if image.is_primary:
                return image
        
        return self.images[0] if self.images else None
    
    def add_review(self, review: ProductReview) -> None:
        """Add a review to the product."""
        self.reviews.append(review)
        self.review_count = len(self.reviews)
        
        # Recalculate rating
        if self.reviews:
            total_rating = sum(review.rating for review in self.reviews)
            self.rating = total_rating / len(self.reviews)
    
    def is_available_in_size(self, size: str) -> bool:
        """Check if product is available in specific size."""
        size_variants = [
            variant for variant in self.variants 
            if variant.name.lower() == "size" and variant.available
        ]
        return any(
            variant.value.lower() == size.lower() 
            for variant in size_variants
        )
    
    def get_price_for_variant(self, variant_id: str) -> Decimal:
        """Get price including variant modifier."""
        variant = next(
            (v for v in self.variants if v.id == variant_id), 
            None
        )
        
        if variant:
            return self.price + variant.price_modifier
        
        return self.price


@dataclass
class ProductSearchFilters:
    """Product search filters entity."""
    
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    sizes: List[str] = field(default_factory=list)
    colors: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    available_only: bool = True
    has_discount: Optional[bool] = None
    min_rating: Optional[float] = None
    sort_by: str = "relevance"  # relevance, price_low, price_high, rating, newest
    
    def to_dict(self) -> dict:
        """Convert filters to dictionary for API calls."""
        filters = {}
        
        if self.category:
            filters["category"] = self.category
        if self.brand:
            filters["brand"] = self.brand
        if self.min_price:
            filters["min_price"] = float(self.min_price)
        if self.max_price:
            filters["max_price"] = float(self.max_price)
        if self.sizes:
            filters["sizes"] = self.sizes
        if self.colors:
            filters["colors"] = self.colors
        if self.tags:
            filters["tags"] = self.tags
        if self.available_only:
            filters["available_only"] = self.available_only
        if self.has_discount is not None:
            filters["has_discount"] = self.has_discount
        if self.min_rating:
            filters["min_rating"] = self.min_rating
        
        filters["sort_by"] = self.sort_by
        
        return filters


@dataclass
class ProductSearchResult:
    """Product search result entity."""
    
    products: List[Product]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    filters_applied: ProductSearchFilters
    
    @property
    def has_next_page(self) -> bool:
        """Check if there's a next page."""
        return self.page < self.total_pages
    
    @property
    def has_previous_page(self) -> bool:
        """Check if there's a previous page."""
        return self.page > 1
