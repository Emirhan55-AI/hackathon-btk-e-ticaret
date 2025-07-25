"""Shopping cart domain entities."""
from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from uuid import uuid4


@dataclass
class CartItem:
    """Shopping cart item entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: str = ""
    variant_id: Optional[str] = None
    quantity: int = 1
    price_per_item: Decimal = Decimal("0.00")
    total_price: Decimal = field(init=False)
    added_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Calculate total price after initialization."""
        self.total_price = self.price_per_item * self.quantity
    
    def update_quantity(self, quantity: int) -> None:
        """Update item quantity and recalculate total."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        self.quantity = quantity
        self.total_price = self.price_per_item * self.quantity
    
    def update_price(self, new_price: Decimal) -> None:
        """Update price and recalculate total."""
        self.price_per_item = new_price
        self.total_price = self.price_per_item * self.quantity


@dataclass
class ShoppingCart:
    """Shopping cart entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    items: List[CartItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def total_items(self) -> int:
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items)
    
    @property
    def total_amount(self) -> Decimal:
        """Get total cart amount."""
        return sum(item.total_price for item in self.items)
    
    @property
    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self.items) == 0
    
    def add_item(
        self, 
        product_id: str, 
        price: Decimal, 
        quantity: int = 1,
        variant_id: Optional[str] = None
    ) -> CartItem:
        """Add item to cart or update quantity if exists."""
        # Check if item already exists
        existing_item = self._find_item(product_id, variant_id)
        
        if existing_item:
            # Update quantity of existing item
            new_quantity = existing_item.quantity + quantity
            existing_item.update_quantity(new_quantity)
            self.updated_at = datetime.utcnow()
            return existing_item
        else:
            # Add new item
            new_item = CartItem(
                product_id=product_id,
                variant_id=variant_id,
                quantity=quantity,
                price_per_item=price
            )
            self.items.append(new_item)
            self.updated_at = datetime.utcnow()
            return new_item
    
    def remove_item(self, item_id: str) -> bool:
        """Remove item from cart."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def update_item_quantity(self, item_id: str, quantity: int) -> bool:
        """Update quantity of specific item."""
        if quantity <= 0:
            return self.remove_item(item_id)
        
        for item in self.items:
            if item.id == item_id:
                item.update_quantity(quantity)
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def clear(self) -> None:
        """Clear all items from cart."""
        self.items.clear()
        self.updated_at = datetime.utcnow()
    
    def _find_item(self, product_id: str, variant_id: Optional[str] = None) -> Optional[CartItem]:
        """Find existing item in cart."""
        for item in self.items:
            if item.product_id == product_id and item.variant_id == variant_id:
                return item
        return None


@dataclass
class WishlistItem:
    """Wishlist item entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: str = ""
    added_at: datetime = field(default_factory=datetime.utcnow)
    notes: Optional[str] = None


@dataclass
class Wishlist:
    """User wishlist entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    items: List[WishlistItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def total_items(self) -> int:
        """Get total number of items in wishlist."""
        return len(self.items)
    
    @property
    def is_empty(self) -> bool:
        """Check if wishlist is empty."""
        return len(self.items) == 0
    
    def add_item(self, product_id: str, notes: Optional[str] = None) -> WishlistItem:
        """Add item to wishlist."""
        # Check if item already exists
        if self._has_product(product_id):
            raise ValueError(f"Product {product_id} is already in wishlist")
        
        new_item = WishlistItem(
            product_id=product_id,
            notes=notes
        )
        self.items.append(new_item)
        self.updated_at = datetime.utcnow()
        return new_item
    
    def remove_item(self, item_id: str) -> bool:
        """Remove item from wishlist."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def remove_by_product_id(self, product_id: str) -> bool:
        """Remove item by product ID."""
        for i, item in enumerate(self.items):
            if item.product_id == product_id:
                del self.items[i]
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def clear(self) -> None:
        """Clear all items from wishlist."""
        self.items.clear()
        self.updated_at = datetime.utcnow()
    
    def _has_product(self, product_id: str) -> bool:
        """Check if product is already in wishlist."""
        return any(item.product_id == product_id for item in self.items)
