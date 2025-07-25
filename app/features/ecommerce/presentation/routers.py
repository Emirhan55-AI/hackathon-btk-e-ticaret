"""E-commerce API endpoints."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.features.ecommerce.infrastructure.repositories import HttpEcommerceRepository
from app.features.ecommerce.application.use_cases import (
    SearchProductsUseCase,
    GetProductByIdUseCase,
    GetTrendingProductsUseCase,
    GetProductRecommendationsUseCase
)
from app.features.ecommerce.application.schemas import (
    ProductSchema,
    ProductSearchRequest,
    ProductSearchResultSchema,
    ProductRecommendationRequest,
    TrendingProductsRequest
)
from app.features.auth.presentation.dependencies import get_current_user_optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ecommerce", tags=["E-commerce"])


# Dependency functions
async def get_ecommerce_repository() -> HttpEcommerceRepository:
    """Get e-commerce repository instance."""
    return HttpEcommerceRepository()


async def get_search_use_case(
    repository: HttpEcommerceRepository = Depends(get_ecommerce_repository)
) -> SearchProductsUseCase:
    """Get search products use case."""
    return SearchProductsUseCase(repository)


async def get_product_by_id_use_case(
    repository: HttpEcommerceRepository = Depends(get_ecommerce_repository)
) -> GetProductByIdUseCase:
    """Get product by ID use case."""
    return GetProductByIdUseCase(repository)


async def get_trending_use_case(
    repository: HttpEcommerceRepository = Depends(get_ecommerce_repository)
) -> GetTrendingProductsUseCase:
    """Get trending products use case."""
    return GetTrendingProductsUseCase(repository)


async def get_recommendations_use_case(
    repository: HttpEcommerceRepository = Depends(get_ecommerce_repository)
) -> GetProductRecommendationsUseCase:
    """Get product recommendations use case."""
    return GetProductRecommendationsUseCase(repository)


@router.post(
    "/search",
    response_model=ProductSearchResultSchema,
    summary="Search Products",
    description="Search for products with filters and pagination"
)
async def search_products(
    search_request: ProductSearchRequest,
    search_use_case: SearchProductsUseCase = Depends(get_search_use_case)
) -> ProductSearchResultSchema:
    """Search for products."""
    try:
        logger.info(
            f"Searching products with query: {search_request.query}, "
            f"filters: {search_request.filters.dict()}"
        )
        
        result = await search_use_case.execute(
            query=search_request.query,
            filters=search_request.filters,
            page=search_request.page,
            page_size=search_request.page_size
        )
        
        logger.info(f"Found {result.total_count} products")
        return result
        
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search products"
        )


@router.get(
    "/products/{product_id}",
    response_model=ProductSchema,
    summary="Get Product by ID",
    description="Get detailed information about a specific product"
)
async def get_product(
    product_id: str,
    get_product_use_case: GetProductByIdUseCase = Depends(get_product_by_id_use_case)
) -> ProductSchema:
    """Get product by ID."""
    try:
        logger.info(f"Getting product with ID: {product_id}")
        
        product = await get_product_use_case.execute(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get product"
        )


@router.get(
    "/trending",
    response_model=ProductSearchResultSchema,
    summary="Get Trending Products",
    description="Get currently trending products"
)
async def get_trending_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    time_period: str = Query("week", description="Time period for trending"),
    limit: int = Query(20, ge=1, le=100, description="Number of products"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Products per page"),
    trending_use_case: GetTrendingProductsUseCase = Depends(get_trending_use_case)
) -> ProductSearchResultSchema:
    """Get trending products."""
    try:
        logger.info(
            f"Getting trending products - category: {category}, "
            f"time_period: {time_period}, limit: {limit}"
        )
        
        request = TrendingProductsRequest(
            category=category,
            time_period=time_period,
            limit=limit
        )
        
        result = await trending_use_case.execute(
            request=request,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"Found {result.total_count} trending products")
        return result
        
    except Exception as e:
        logger.error(f"Error getting trending products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get trending products"
        )


@router.post(
    "/recommendations",
    response_model=ProductSearchResultSchema,
    summary="Get Product Recommendations",
    description="Get personalized product recommendations for a user"
)
async def get_product_recommendations(
    recommendation_request: ProductRecommendationRequest,
    current_user = Depends(get_current_user_optional),
    recommendations_use_case: GetProductRecommendationsUseCase = Depends(get_recommendations_use_case)
) -> ProductSearchResultSchema:
    """Get product recommendations for a user."""
    try:
        # Use current user if authenticated, otherwise use provided user_id
        user_id = current_user.id if current_user else recommendation_request.user_id
        
        logger.info(
            f"Getting product recommendations for user: {user_id}, "
            f"category: {recommendation_request.category}, "
            f"limit: {recommendation_request.limit}"
        )
        
        result = await recommendations_use_case.execute(
            user_id=user_id,
            category=recommendation_request.category,
            limit=recommendation_request.limit
        )
        
        logger.info(f"Generated {result.total_count} product recommendations")
        return result
        
    except Exception as e:
        logger.error(f"Error getting product recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get product recommendations"
        )


@router.get(
    "/categories",
    response_model=list[str],
    summary="Get Product Categories",
    description="Get list of available product categories"
)
async def get_categories(
    search_use_case: SearchProductsUseCase = Depends(get_search_use_case)
) -> list[str]:
    """Get available product categories."""
    try:
        logger.info("Getting product categories")
        
        # This would typically come from a separate service or be cached
        # For now, return common fashion categories
        categories = [
            "Tops",
            "Bottoms",
            "Dresses",
            "Outerwear",
            "Shoes",
            "Accessories",
            "Bags",
            "Jewelry",
            "Underwear",
            "Activewear",
            "Formal",
            "Casual",
            "Business"
        ]
        
        return categories
        
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get categories"
        )


@router.get(
    "/brands",
    response_model=list[str],
    summary="Get Product Brands",
    description="Get list of available product brands"
)
async def get_brands() -> list[str]:
    """Get available product brands."""
    try:
        logger.info("Getting product brands")
        
        # This would typically come from a database or external service
        # For now, return popular fashion brands
        brands = [
            "Zara",
            "H&M",
            "Nike",
            "Adidas",
            "Uniqlo",
            "Forever 21",
            "ASOS",
            "Urban Outfitters",
            "Mango",
            "COS",
            "Massimo Dutti",
            "Bershka",
            "Pull & Bear"
        ]
        
        return brands
        
    except Exception as e:
        logger.error(f"Error getting brands: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get brands"
        )
