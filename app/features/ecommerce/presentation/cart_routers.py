"""Shopping cart and wishlist API endpoints."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.features.ecommerce.infrastructure.cart_repositories import InMemoryCartRepository, CartRepository
from app.features.ecommerce.infrastructure.repositories import HttpEcommerceRepository, EcommerceRepository
from app.features.ecommerce.application.cart_use_cases import (
    GetCartUseCase,
    AddToCartUseCase,
    UpdateCartItemUseCase,
    RemoveFromCartUseCase,
    ClearCartUseCase,
    GetWishlistUseCase,
    AddToWishlistUseCase,
    RemoveFromWishlistUseCase
)
from app.features.ecommerce.application.cart_schemas import (
    ShoppingCartSchema,
    AddToCartRequest,
    UpdateCartItemRequest,
    WishlistSchema,
    AddToWishlistRequest,
    CartSummarySchema,
    WishlistSummarySchema
)
from app.features.auth.presentation.dependencies import get_current_user
from app.features.auth.domain.entities import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])


# Repository Dependencies
async def get_cart_repository() -> CartRepository:
    """Get cart repository instance."""
    return InMemoryCartRepository()


async def get_ecommerce_repository() -> EcommerceRepository:
    """Get e-commerce repository instance."""
    return HttpEcommerceRepository(http_client=None)


# Use Case Dependencies
async def get_cart_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> GetCartUseCase:
    """Get cart use case."""
    return GetCartUseCase(cart_repo)


async def get_add_to_cart_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository),
    ecommerce_repo: EcommerceRepository = Depends(get_ecommerce_repository)
) -> AddToCartUseCase:
    """Get add to cart use case."""
    return AddToCartUseCase(cart_repo, ecommerce_repo)


async def get_update_cart_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> UpdateCartItemUseCase:
    """Get update cart use case."""
    return UpdateCartItemUseCase(cart_repo)


async def get_remove_from_cart_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> RemoveFromCartUseCase:
    """Get remove from cart use case."""
    return RemoveFromCartUseCase(cart_repo)


async def get_clear_cart_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> ClearCartUseCase:
    """Get clear cart use case."""
    return ClearCartUseCase(cart_repo)


async def get_wishlist_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> GetWishlistUseCase:
    """Get wishlist use case."""
    return GetWishlistUseCase(cart_repo)


async def get_add_to_wishlist_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository),
    ecommerce_repo: EcommerceRepository = Depends(get_ecommerce_repository)
) -> AddToWishlistUseCase:
    """Get add to wishlist use case."""
    return AddToWishlistUseCase(cart_repo, ecommerce_repo)


async def get_remove_from_wishlist_use_case(
    cart_repo: CartRepository = Depends(get_cart_repository)
) -> RemoveFromWishlistUseCase:
    """Get remove from wishlist use case."""
    return RemoveFromWishlistUseCase(cart_repo)


# Shopping Cart Endpoints

@router.get("/", response_model=ShoppingCartSchema)
async def get_cart(
    current_user: User = Depends(get_current_user),
    use_case: GetCartUseCase = Depends(get_cart_use_case)
):
    """Get user's shopping cart."""
    try:
        cart = await use_case.execute(current_user.id)
        
        return ShoppingCartSchema(
            id=cart.id,
            user_id=cart.user_id,
            items=[
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price_per_item": item.price_per_item,
                    "total_price": item.total_price,
                    "added_at": item.added_at
                }
                for item in cart.items
            ],
            total_items=cart.total_items,
            total_amount=cart.total_amount,
            is_empty=cart.is_empty,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error getting cart: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get cart"
        )


@router.post("/items", response_model=ShoppingCartSchema)
async def add_to_cart(
    request: AddToCartRequest,
    current_user: User = Depends(get_current_user),
    use_case: AddToCartUseCase = Depends(get_add_to_cart_use_case)
):
    """Add item to shopping cart."""
    try:
        cart = await use_case.execute(
            user_id=current_user.id,
            product_id=request.product_id,
            quantity=request.quantity,
            variant_id=request.variant_id
        )
        
        return ShoppingCartSchema(
            id=cart.id,
            user_id=cart.user_id,
            items=[
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price_per_item": item.price_per_item,
                    "total_price": item.total_price,
                    "added_at": item.added_at
                }
                for item in cart.items
            ],
            total_items=cart.total_items,
            total_amount=cart.total_amount,
            is_empty=cart.is_empty,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add item to cart"
        )


@router.put("/items/{item_id}", response_model=ShoppingCartSchema)
async def update_cart_item(
    item_id: str,
    request: UpdateCartItemRequest,
    current_user: User = Depends(get_current_user),
    use_case: UpdateCartItemUseCase = Depends(get_update_cart_use_case)
):
    """Update cart item quantity."""
    try:
        cart = await use_case.execute(
            user_id=current_user.id,
            item_id=item_id,
            quantity=request.quantity
        )
        
        return ShoppingCartSchema(
            id=cart.id,
            user_id=cart.user_id,
            items=[
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price_per_item": item.price_per_item,
                    "total_price": item.total_price,
                    "added_at": item.added_at
                }
                for item in cart.items
            ],
            total_items=cart.total_items,
            total_amount=cart.total_amount,
            is_empty=cart.is_empty,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating cart item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update cart item"
        )


@router.delete("/items/{item_id}", response_model=ShoppingCartSchema)
async def remove_from_cart(
    item_id: str,
    current_user: User = Depends(get_current_user),
    use_case: RemoveFromCartUseCase = Depends(get_remove_from_cart_use_case)
):
    """Remove item from shopping cart."""
    try:
        cart = await use_case.execute(
            user_id=current_user.id,
            item_id=item_id
        )
        
        return ShoppingCartSchema(
            id=cart.id,
            user_id=cart.user_id,
            items=[
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price_per_item": item.price_per_item,
                    "total_price": item.total_price,
                    "added_at": item.added_at
                }
                for item in cart.items
            ],
            total_items=cart.total_items,
            total_amount=cart.total_amount,
            is_empty=cart.is_empty,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error removing from cart: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove item from cart"
        )


@router.delete("/", response_model=ShoppingCartSchema)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    use_case: ClearCartUseCase = Depends(get_clear_cart_use_case)
):
    """Clear all items from shopping cart."""
    try:
        cart = await use_case.execute(current_user.id)
        
        return ShoppingCartSchema(
            id=cart.id,
            user_id=cart.user_id,
            items=[],
            total_items=cart.total_items,
            total_amount=cart.total_amount,
            is_empty=cart.is_empty,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error clearing cart: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear cart"
        )


@router.get("/summary", response_model=CartSummarySchema)
async def get_cart_summary(
    current_user: User = Depends(get_current_user),
    use_case: GetCartUseCase = Depends(get_cart_use_case)
):
    """Get cart summary."""
    try:
        cart = await use_case.execute(current_user.id)
        
        return CartSummarySchema(
            total_items=cart.total_items,
            total_amount=cart.total_amount,
            currency="USD",
            last_updated=cart.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error getting cart summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get cart summary"
        )


# Wishlist Endpoints

@router.get("/wishlist", response_model=WishlistSchema)
async def get_wishlist(
    current_user: User = Depends(get_current_user),
    use_case: GetWishlistUseCase = Depends(get_wishlist_use_case)
):
    """Get user's wishlist."""
    try:
        wishlist = await use_case.execute(current_user.id)
        
        return WishlistSchema(
            id=wishlist.id,
            user_id=wishlist.user_id,
            items=[
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "added_at": item.added_at,
                    "notes": item.notes
                }
                for item in wishlist.items
            ],
            total_items=wishlist.total_items,
            is_empty=wishlist.is_empty,
            created_at=wishlist.created_at,
            updated_at=wishlist.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error getting wishlist: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get wishlist"
        )


@router.post("/wishlist/items", response_model=WishlistSchema)
async def add_to_wishlist(
    request: AddToWishlistRequest,
    current_user: User = Depends(get_current_user),
    use_case: AddToWishlistUseCase = Depends(get_add_to_wishlist_use_case)
):
    """Add item to wishlist."""
    try:
        wishlist = await use_case.execute(
            user_id=current_user.id,
            product_id=request.product_id,
            notes=request.notes
        )
        
        return WishlistSchema(
            id=wishlist.id,
            user_id=wishlist.user_id,
            items=[
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "added_at": item.added_at,
                    "notes": item.notes
                }
                for item in wishlist.items
            ],
            total_items=wishlist.total_items,
            is_empty=wishlist.is_empty,
            created_at=wishlist.created_at,
            updated_at=wishlist.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error adding to wishlist: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add item to wishlist"
        )


@router.delete("/wishlist/items/{item_id}", response_model=WishlistSchema)
async def remove_from_wishlist(
    item_id: str,
    current_user: User = Depends(get_current_user),
    use_case: RemoveFromWishlistUseCase = Depends(get_remove_from_wishlist_use_case)
):
    """Remove item from wishlist."""
    try:
        wishlist = await use_case.execute(
            user_id=current_user.id,
            item_id=item_id
        )
        
        return WishlistSchema(
            id=wishlist.id,
            user_id=wishlist.user_id,
            items=[
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "added_at": item.added_at,
                    "notes": item.notes
                }
                for item in wishlist.items
            ],
            total_items=wishlist.total_items,
            is_empty=wishlist.is_empty,
            created_at=wishlist.created_at,
            updated_at=wishlist.updated_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error removing from wishlist: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove item from wishlist"
        )


@router.get("/wishlist/summary", response_model=WishlistSummarySchema)
async def get_wishlist_summary(
    current_user: User = Depends(get_current_user),
    use_case: GetWishlistUseCase = Depends(get_wishlist_use_case)
):
    """Get wishlist summary."""
    try:
        wishlist = await use_case.execute(current_user.id)
        
        return WishlistSummarySchema(
            total_items=wishlist.total_items,
            last_updated=wishlist.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error getting wishlist summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get wishlist summary"
        )
