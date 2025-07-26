"""Order management domain entities."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import datetime
from enum import Enum
from uuid import uuid4


class OrderStatus(Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class PaymentMethod(Enum):
    """Payment method enumeration."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"


@dataclass
class Address:
    """Address entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    full_name: str = ""
    address_line_1: str = ""
    address_line_2: Optional[str] = None
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = ""
    phone: Optional[str] = None
    is_default: bool = False
    
    def get_full_address(self) -> str:
        """Get formatted full address."""
        lines = [self.address_line_1]
        if self.address_line_2:
            lines.append(self.address_line_2)
        lines.append(f"{self.city}, {self.state} {self.postal_code}")
        lines.append(self.country)
        return "\n".join(lines)


@dataclass
class OrderItem:
    """Order item entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: str = ""
    product_name: str = ""
    product_brand: str = ""
    variant_id: Optional[str] = None
    variant_details: Optional[Dict[str, Any]] = None
    quantity: int = 1
    unit_price: Decimal = Decimal("0.00")
    total_price: Decimal = field(init=False)
    product_image_url: Optional[str] = None
    
    def __post_init__(self):
        """Calculate total price after initialization."""
        self.total_price = self.unit_price * self.quantity


@dataclass
class PaymentInfo:
    """Payment information entity."""
    
    method: PaymentMethod = PaymentMethod.CREDIT_CARD
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    amount: Decimal = Decimal("0.00")
    currency: str = "USD"
    gateway_response: Optional[Dict[str, Any]] = None


@dataclass
class ShippingInfo:
    """Shipping information entity."""
    
    method: str = "standard"
    cost: Decimal = Decimal("0.00")
    estimated_delivery: Optional[datetime] = None
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    shipped_date: Optional[datetime] = None
    delivered_date: Optional[datetime] = None


@dataclass
class Order:
    """Order entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    order_number: str = field(default_factory=lambda: f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid4())[:8].upper()}")
    user_id: str = ""
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    
    # Pricing
    subtotal: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    shipping_cost: Decimal = Decimal("0.00")
    discount_amount: Decimal = Decimal("0.00")
    total_amount: Decimal = field(init=False)
    currency: str = "USD"
    
    # Addresses
    billing_address: Optional[Address] = None
    shipping_address: Optional[Address] = None
    
    # Payment & Shipping
    payment_info: Optional[PaymentInfo] = None
    shipping_info: Optional[ShippingInfo] = None
    
    # Metadata
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Calculate total amount after initialization."""
        self.calculate_total()
    
    def calculate_total(self) -> None:
        """Calculate total order amount."""
        self.total_amount = (
            self.subtotal + 
            self.tax_amount + 
            self.shipping_cost - 
            self.discount_amount
        )
    
    def add_item(self, item: OrderItem) -> None:
        """Add item to order."""
        self.items.append(item)
        self.recalculate_subtotal()
        self.updated_at = datetime.utcnow()
    
    def remove_item(self, item_id: str) -> bool:
        """Remove item from order."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                self.recalculate_subtotal()
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def recalculate_subtotal(self) -> None:
        """Recalculate subtotal based on items."""
        self.subtotal = sum(item.total_price for item in self.items)
        self.calculate_total()
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update order status."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        # Update related info based on status
        if new_status == OrderStatus.SHIPPED and self.shipping_info:
            self.shipping_info.shipped_date = datetime.utcnow()
        elif new_status == OrderStatus.DELIVERED and self.shipping_info:
            self.shipping_info.delivered_date = datetime.utcnow()
    
    def apply_discount(self, discount_amount: Decimal) -> None:
        """Apply discount to order."""
        self.discount_amount = discount_amount
        self.calculate_total()
        self.updated_at = datetime.utcnow()
    
    def set_shipping_cost(self, shipping_cost: Decimal) -> None:
        """Set shipping cost."""
        self.shipping_cost = shipping_cost
        self.calculate_total()
        self.updated_at = datetime.utcnow()
    
    def set_tax_amount(self, tax_amount: Decimal) -> None:
        """Set tax amount."""
        self.tax_amount = tax_amount
        self.calculate_total()
        self.updated_at = datetime.utcnow()
    
    @property
    def total_items(self) -> int:
        """Get total number of items in order."""
        return sum(item.quantity for item in self.items)
    
    @property
    def can_be_cancelled(self) -> bool:
        """Check if order can be cancelled."""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    @property
    def is_completed(self) -> bool:
        """Check if order is completed."""
        return self.status == OrderStatus.DELIVERED
    
    @property
    def is_paid(self) -> bool:
        """Check if order is paid."""
        return (
            self.payment_info is not None and 
            self.payment_info.status == PaymentStatus.COMPLETED
        )
