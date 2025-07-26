"""Shopping cart and wishlist use cases."""
from typing import List, Optional
from decimal import Decimal
import logging

from app.features.ecommerce.domain.cart_entities import ShoppingCart, CartItem, Wishlist, WishlistItem
from app.features.ecommerce.infrastructure.cart_repositories import CartRepository
from app.features.ecommerce.infrastructure.repositories import EcommerceRepository

logger = logging.getLogger(__name__)


class GetCartUseCase:
    """Use case for getting user's shopping cart."""
    
    def __init__(self, cart_repository: CartRepository):
        self._cart_repository = cart_repository
    
    async def execute(self, user_id: str) -> ShoppingCart:
        """
        Get or create user's shopping cart.
        
        Args:
            user_id: User ID
        
        Returns:
            User's shopping cart
        """
        try:
            logger.info(f"Getting cart for user: {user_id}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            # Try to get existing cart
            cart = await self._cart_repository.get_cart_by_user_id(user_id)
            
            if cart is None:
                # Create new cart if none exists
                cart = ShoppingCart(user_id=user_id)
                cart = await self._cart_repository.save_cart(cart)
                logger.info(f"Created new cart for user: {user_id}")
            else:
                logger.info(f"Found existing cart for user: {user_id} with {len(cart.items)} items")
            
            return cart
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting cart for user {user_id}: {e}")
            raise


class AddToCartUseCase:
    """Use case for adding items to shopping cart."""
    
    def __init__(
        self, 
        cart_repository: CartRepository, 
        ecommerce_repository: EcommerceRepository
    ):
        self._cart_repository = cart_repository
        self._ecommerce_repository = ecommerce_repository
    
    async def execute(
        self, 
        user_id: str, 
        product_id: str, 
        quantity: int = 1,
        variant_id: Optional[str] = None
    ) -> ShoppingCart:
        """
        Add item to user's shopping cart.
        
        Args:
            user_id: User ID
            product_id: Product ID to add
            quantity: Quantity to add
            variant_id: Optional variant ID
        
        Returns:
            Updated shopping cart
        """
        try:
            logger.info(f"Adding to cart: user={user_id}, product={product_id}, qty={quantity}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            if not product_id or len(product_id.strip()) == 0:
                raise ValueError("Product ID cannot be empty")
            
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0")
            
            # Get product details to validate and get price
            product = await self._ecommerce_repository.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"Product not found: {product_id}")
            
            # Calculate price (including variant if specified)
            if variant_id:
                price = product.get_price_for_variant(variant_id)
            else:
                price = product.price
            
            # Get or create cart
            cart = await self._cart_repository.get_cart_by_user_id(user_id)
            if cart is None:
                cart = ShoppingCart(user_id=user_id)
            
            # Add item to cart
            cart.add_item(
                product_id=product_id,
                price=price,
                quantity=quantity,
                variant_id=variant_id
            )
            
            # Save cart
            cart = await self._cart_repository.save_cart(cart)
            
            logger.info(f"Added {quantity}x {product.name} to cart for user {user_id}")
            return cart
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error adding to cart: {e}")
            raise


class UpdateCartItemUseCase:
    """Use case for updating cart item quantity."""
    
    def __init__(self, cart_repository: CartRepository):
        self._cart_repository = cart_repository
    
    async def execute(
        self, 
        user_id: str, 
        item_id: str, 
        quantity: int
    ) -> ShoppingCart:
        """
        Update quantity of cart item.
        
        Args:
            user_id: User ID
            item_id: Cart item ID
            quantity: New quantity (0 to remove)
        
        Returns:
            Updated shopping cart
        """
        try:
            logger.info(f"Updating cart item: user={user_id}, item={item_id}, qty={quantity}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            if not item_id or len(item_id.strip()) == 0:
                raise ValueError("Item ID cannot be empty")
            
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
            
            # Get cart
            cart = await self._cart_repository.get_cart_by_user_id(user_id)
            if not cart:
                raise ValueError("Cart not found")
            
            # Update item quantity
            if quantity == 0:
                success = cart.remove_item(item_id)
                if not success:
                    raise ValueError("Item not found in cart")
            else:
                success = cart.update_item_quantity(item_id, quantity)
                if not success:
                    raise ValueError("Item not found in cart")
            
            # Save cart
            cart = await self._cart_repository.save_cart(cart)
            
            logger.info(f"Updated cart item {item_id} to quantity {quantity}")
            return cart
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error updating cart item: {e}")
            raise


class RemoveFromCartUseCase:
    """Use case for removing items from shopping cart."""
    
    def __init__(self, cart_repository: CartRepository):
        self._cart_repository = cart_repository
    
    async def execute(self, user_id: str, item_id: str) -> ShoppingCart:
        """
        Remove item from user's shopping cart.
        
        Args:
            user_id: User ID
            item_id: Cart item ID to remove
        
        Returns:
            Updated shopping cart
        """
        try:
            logger.info(f"Removing from cart: user={user_id}, item={item_id}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            if not item_id or len(item_id.strip()) == 0:
                raise ValueError("Item ID cannot be empty")
            
            # Get cart
            cart = await self._cart_repository.get_cart_by_user_id(user_id)
            if not cart:
                raise ValueError("Cart not found")
            
            # Remove item
            success = cart.remove_item(item_id)
            if not success:
                raise ValueError("Item not found in cart")
            
            # Save cart
            cart = await self._cart_repository.save_cart(cart)
            
            logger.info(f"Removed item {item_id} from cart for user {user_id}")
            return cart
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error removing from cart: {e}")
            raise


class ClearCartUseCase:
    """Use case for clearing shopping cart."""
    
    def __init__(self, cart_repository: CartRepository):
        self._cart_repository = cart_repository
    
    async def execute(self, user_id: str) -> ShoppingCart:
        """
        Clear all items from user's shopping cart.
        
        Args:
            user_id: User ID
        
        Returns:
            Empty shopping cart
        """
        try:
            logger.info(f"Clearing cart for user: {user_id}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            # Get cart
            cart = await self._cart_repository.get_cart_by_user_id(user_id)
            if not cart:
                # Create empty cart if none exists
                cart = ShoppingCart(user_id=user_id)
            else:
                # Clear existing cart
                cart.clear()
            
            # Save cart
            cart = await self._cart_repository.save_cart(cart)
            
            logger.info(f"Cleared cart for user {user_id}")
            return cart
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
            raise


# Wishlist Use Cases

class GetWishlistUseCase:
    """Use case for getting user's wishlist."""
    
    def __init__(self, cart_repository: CartRepository):
        self._cart_repository = cart_repository
    
    async def execute(self, user_id: str) -> Wishlist:
        """
        Get or create user's wishlist.
        
        Args:
            user_id: User ID
        
        Returns:
            User's wishlist
        """
        try:
            logger.info(f"Getting wishlist for user: {user_id}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            # Try to get existing wishlist
            wishlist = await self._cart_repository.get_wishlist_by_user_id(user_id)
            
            if wishlist is None:
                # Create new wishlist if none exists
                wishlist = Wishlist(user_id=user_id)
                wishlist = await self._cart_repository.save_wishlist(wishlist)
                logger.info(f"Created new wishlist for user: {user_id}")
            else:
                logger.info(f"Found existing wishlist for user: {user_id} with {len(wishlist.items)} items")
            
            return wishlist
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting wishlist for user {user_id}: {e}")
            raise


class AddToWishlistUseCase:
    """Use case for adding items to wishlist."""
    
    def __init__(
        self, 
        cart_repository: CartRepository, 
        ecommerce_repository: EcommerceRepository
    ):
        self._cart_repository = cart_repository
        self._ecommerce_repository = ecommerce_repository
    
    async def execute(
        self, 
        user_id: str, 
        product_id: str, 
        notes: Optional[str] = None
    ) -> Wishlist:
        """
        Add item to user's wishlist.
        
        Args:
            user_id: User ID
            product_id: Product ID to add
            notes: Optional notes about the item
        
        Returns:
            Updated wishlist
        """
        try:
            logger.info(f"Adding to wishlist: user={user_id}, product={product_id}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            if not product_id or len(product_id.strip()) == 0:
                raise ValueError("Product ID cannot be empty")
            
            # Validate product exists
            product = await self._ecommerce_repository.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"Product not found: {product_id}")
            
            # Get or create wishlist
            wishlist = await self._cart_repository.get_wishlist_by_user_id(user_id)
            if wishlist is None:
                wishlist = Wishlist(user_id=user_id)
            
            # Add item to wishlist
            wishlist.add_item(product_id=product_id, notes=notes)
            
            # Save wishlist
            wishlist = await self._cart_repository.save_wishlist(wishlist)
            
            logger.info(f"Added {product.name} to wishlist for user {user_id}")
            return wishlist
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error adding to wishlist: {e}")
            raise


class RemoveFromWishlistUseCase:
    """Use case for removing items from wishlist."""
    
    def __init__(self, cart_repository: CartRepository):
        self._cart_repository = cart_repository
    
    async def execute(self, user_id: str, item_id: str) -> Wishlist:
        """
        Remove item from user's wishlist.
        
        Args:
            user_id: User ID
            item_id: Wishlist item ID to remove
        
        Returns:
            Updated wishlist
        """
        try:
            logger.info(f"Removing from wishlist: user={user_id}, item={item_id}")
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            if not item_id or len(item_id.strip()) == 0:
                raise ValueError("Item ID cannot be empty")
            
            # Get wishlist
            wishlist = await self._cart_repository.get_wishlist_by_user_id(user_id)
            if not wishlist:
                raise ValueError("Wishlist not found")
            
            # Remove item
            success = wishlist.remove_item(item_id)
            if not success:
                raise ValueError("Item not found in wishlist")
            
            # Save wishlist
            wishlist = await self._cart_repository.save_wishlist(wishlist)
            
            logger.info(f"Removed item {item_id} from wishlist for user {user_id}")
            return wishlist
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error removing from wishlist: {e}")
            raise
