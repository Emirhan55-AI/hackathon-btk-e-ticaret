"""Shopping cart repository interfaces and implementations."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import json
import logging
from datetime import datetime
from decimal import Decimal

from app.features.ecommerce.domain.cart_entities import ShoppingCart, CartItem, Wishlist, WishlistItem

logger = logging.getLogger(__name__)


class CartRepository(ABC):
    """Abstract repository interface for shopping cart operations."""
    
    @abstractmethod
    async def get_cart_by_user_id(self, user_id: str) -> Optional[ShoppingCart]:
        """Get shopping cart for a user."""
        pass
    
    @abstractmethod
    async def save_cart(self, cart: ShoppingCart) -> ShoppingCart:
        """Save shopping cart."""
        pass
    
    @abstractmethod
    async def delete_cart(self, user_id: str) -> bool:
        """Delete shopping cart."""
        pass
    
    @abstractmethod
    async def get_wishlist_by_user_id(self, user_id: str) -> Optional[Wishlist]:
        """Get wishlist for a user."""
        pass
    
    @abstractmethod
    async def save_wishlist(self, wishlist: Wishlist) -> Wishlist:
        """Save wishlist."""
        pass
    
    @abstractmethod
    async def delete_wishlist(self, user_id: str) -> bool:
        """Delete wishlist."""
        pass


class InMemoryCartRepository(CartRepository):
    """In-memory implementation of cart repository for development/testing."""
    
    def __init__(self):
        self._carts: Dict[str, ShoppingCart] = {}
        self._wishlists: Dict[str, Wishlist] = {}
    
    async def get_cart_by_user_id(self, user_id: str) -> Optional[ShoppingCart]:
        """Get shopping cart for a user."""
        try:
            cart = self._carts.get(user_id)
            if cart:
                logger.info(f"Found cart for user {user_id} with {len(cart.items)} items")
            else:
                logger.info(f"No cart found for user {user_id}")
            return cart
        except Exception as e:
            logger.error(f"Error getting cart for user {user_id}: {e}")
            return None
    
    async def save_cart(self, cart: ShoppingCart) -> ShoppingCart:
        """Save shopping cart."""
        try:
            cart.updated_at = datetime.utcnow()
            self._carts[cart.user_id] = cart
            logger.info(f"Saved cart for user {cart.user_id} with {len(cart.items)} items")
            return cart
        except Exception as e:
            logger.error(f"Error saving cart: {e}")
            raise
    
    async def delete_cart(self, user_id: str) -> bool:
        """Delete shopping cart."""
        try:
            if user_id in self._carts:
                del self._carts[user_id]
                logger.info(f"Deleted cart for user {user_id}")
                return True
            else:
                logger.info(f"No cart found to delete for user {user_id}")
                return False
        except Exception as e:
            logger.error(f"Error deleting cart for user {user_id}: {e}")
            return False
    
    async def get_wishlist_by_user_id(self, user_id: str) -> Optional[Wishlist]:
        """Get wishlist for a user."""
        try:
            wishlist = self._wishlists.get(user_id)
            if wishlist:
                logger.info(f"Found wishlist for user {user_id} with {len(wishlist.items)} items")
            else:
                logger.info(f"No wishlist found for user {user_id}")
            return wishlist
        except Exception as e:
            logger.error(f"Error getting wishlist for user {user_id}: {e}")
            return None
    
    async def save_wishlist(self, wishlist: Wishlist) -> Wishlist:
        """Save wishlist."""
        try:
            wishlist.updated_at = datetime.utcnow()
            self._wishlists[wishlist.user_id] = wishlist
            logger.info(f"Saved wishlist for user {wishlist.user_id} with {len(wishlist.items)} items")
            return wishlist
        except Exception as e:
            logger.error(f"Error saving wishlist: {e}")
            raise
    
    async def delete_wishlist(self, user_id: str) -> bool:
        """Delete wishlist."""
        try:
            if user_id in self._wishlists:
                del self._wishlists[user_id]
                logger.info(f"Deleted wishlist for user {user_id}")
                return True
            else:
                logger.info(f"No wishlist found to delete for user {user_id}")
                return False
        except Exception as e:
            logger.error(f"Error deleting wishlist for user {user_id}: {e}")
            return False


class FileBasedCartRepository(CartRepository):
    """File-based implementation of cart repository for persistence."""
    
    def __init__(self, file_path: str = "cart_data.json"):
        self.file_path = file_path
        self._data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from file."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"carts": {}, "wishlists": {}}
        except Exception as e:
            logger.error(f"Error loading cart data: {e}")
            return {"carts": {}, "wishlists": {}}
    
    def _save_data(self) -> None:
        """Save data to file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self._data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving cart data: {e}")
            raise
    
    def _cart_to_dict(self, cart: ShoppingCart) -> Dict[str, Any]:
        """Convert cart to dictionary."""
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price_per_item": str(item.price_per_item),
                    "total_price": str(item.total_price),
                    "added_at": item.added_at.isoformat()
                }
                for item in cart.items
            ],
            "created_at": cart.created_at.isoformat(),
            "updated_at": cart.updated_at.isoformat()
        }
    
    def _dict_to_cart(self, data: Dict[str, Any]) -> ShoppingCart:
        """Convert dictionary to cart."""
        cart = ShoppingCart(
            id=data["id"],
            user_id=data["user_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )
        
        for item_data in data["items"]:
            item = CartItem(
                id=item_data["id"],
                product_id=item_data["product_id"],
                variant_id=item_data.get("variant_id"),
                quantity=item_data["quantity"],
                price_per_item=Decimal(item_data["price_per_item"]),
                added_at=datetime.fromisoformat(item_data["added_at"])
            )
            cart.items.append(item)
        
        return cart
    
    async def get_cart_by_user_id(self, user_id: str) -> Optional[ShoppingCart]:
        """Get shopping cart for a user."""
        try:
            cart_data = self._data["carts"].get(user_id)
            if cart_data:
                return self._dict_to_cart(cart_data)
            return None
        except Exception as e:
            logger.error(f"Error getting cart for user {user_id}: {e}")
            return None
    
    async def save_cart(self, cart: ShoppingCart) -> ShoppingCart:
        """Save shopping cart."""
        try:
            cart.updated_at = datetime.utcnow()
            self._data["carts"][cart.user_id] = self._cart_to_dict(cart)
            self._save_data()
            return cart
        except Exception as e:
            logger.error(f"Error saving cart: {e}")
            raise
    
    async def delete_cart(self, user_id: str) -> bool:
        """Delete shopping cart."""
        try:
            if user_id in self._data["carts"]:
                del self._data["carts"][user_id]
                self._save_data()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting cart for user {user_id}: {e}")
            return False
    
    # Similar implementations for wishlist methods...
    async def get_wishlist_by_user_id(self, user_id: str) -> Optional[Wishlist]:
        """Get wishlist for a user."""
        try:
            wishlist_data = self._data["wishlists"].get(user_id)
            if wishlist_data:
                return self._dict_to_wishlist(wishlist_data)
            return None
        except Exception as e:
            logger.error(f"Error getting wishlist for user {user_id}: {e}")
            return None
    
    async def save_wishlist(self, wishlist: Wishlist) -> Wishlist:
        """Save wishlist."""
        try:
            wishlist.updated_at = datetime.utcnow()
            self._data["wishlists"][wishlist.user_id] = self._wishlist_to_dict(wishlist)
            self._save_data()
            return wishlist
        except Exception as e:
            logger.error(f"Error saving wishlist: {e}")
            raise
    
    async def delete_wishlist(self, user_id: str) -> bool:
        """Delete wishlist."""
        try:
            if user_id in self._data["wishlists"]:
                del self._data["wishlists"][user_id]
                self._save_data()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting wishlist for user {user_id}: {e}")
            return False
    
    def _wishlist_to_dict(self, wishlist: Wishlist) -> Dict[str, Any]:
        """Convert wishlist to dictionary."""
        return {
            "id": wishlist.id,
            "user_id": wishlist.user_id,
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "added_at": item.added_at.isoformat(),
                    "notes": item.notes
                }
                for item in wishlist.items
            ],
            "created_at": wishlist.created_at.isoformat(),
            "updated_at": wishlist.updated_at.isoformat()
        }
    
    def _dict_to_wishlist(self, data: Dict[str, Any]) -> Wishlist:
        """Convert dictionary to wishlist."""
        wishlist = Wishlist(
            id=data["id"],
            user_id=data["user_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )
        
        for item_data in data["items"]:
            item = WishlistItem(
                id=item_data["id"],
                product_id=item_data["product_id"],
                added_at=datetime.fromisoformat(item_data["added_at"]),
                notes=item_data.get("notes")
            )
            wishlist.items.append(item)
        
        return wishlist
