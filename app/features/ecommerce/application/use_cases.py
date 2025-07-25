from typing import List, Optional, Dict, Any
import logging

from app.features.ecommerce.infrastructure.repositories import EcommerceRepository
from app.features.ecommerce.domain.entities import (
    Product, 
    ProductSearchFilters, 
    ProductSearchResult
)
from app.features.ecommerce.application.schemas import (
    ProductSearchFiltersSchema,
    ProductSearchResultSchema,
    TrendingProductsRequest
)

logger = logging.getLogger(__name__)


class SearchProductsUseCase:
    """Use case for searching products."""
    
    def __init__(self, repository: EcommerceRepository):
        self._repository = repository
    
    async def execute(
        self,
        query: str,
        filters: ProductSearchFiltersSchema,
        page: int = 1,
        page_size: int = 20
    ) -> ProductSearchResult:
        """
        Execute product search with filters and pagination.
        
        Args:
            query: Search query
            filters: Search filters
            page: Page number (1-based)
            page_size: Number of items per page
        
        Returns:
            ProductSearchResult with products and pagination info
        """
        try:
            logger.info(
                f"Searching products: query='{query}', page={page}, "
                f"page_size={page_size}, filters={filters.dict()}"
            )
            
            if not query or len(query.strip()) == 0:
                raise ValueError("Search query cannot be empty")
            
            if page_size <= 0 or page_size > 100:
                raise ValueError("Page size must be between 1 and 100")
            
            if page <= 0:
                raise ValueError("Page number must be greater than 0")
            
            # Convert filters to domain object
            domain_filters = ProductSearchFilters(
                category=filters.category,
                brand=filters.brand,
                min_price=filters.min_price,
                max_price=filters.max_price,
                sizes=filters.sizes,
                colors=filters.colors,
                tags=filters.tags,
                available_only=filters.available_only,
                has_discount=filters.has_discount,
                min_rating=filters.min_rating,
                sort_by=filters.sort_by
            )
            
            # Search products
            products = await self._repository.search_products(
                query=query.strip(),
                limit=page_size * 2,  # Get more to ensure we have enough after filtering
                category=filters.category,
                min_price=float(filters.min_price) if filters.min_price else None,
                max_price=float(filters.max_price) if filters.max_price else None
            )
            
            # Apply additional filters
            filtered_products = self._apply_filters(products, domain_filters)
            
            # Calculate pagination
            total_count = len(filtered_products)
            total_pages = (total_count + page_size - 1) // page_size
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            page_products = filtered_products[start_idx:end_idx]
            
            # Create result
            result = ProductSearchResult(
                products=page_products,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=max(1, total_pages),
                filters_applied=domain_filters
            )
            
            logger.info(f"Found {total_count} products, returning {len(page_products)} for page {page}")
            return result
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            raise
    
    def _apply_filters(self, products: List[Product], filters: ProductSearchFilters) -> List[Product]:
        """Apply additional filters to products."""
        filtered = products
        
        # Filter by brand
        if filters.brand:
            filtered = [p for p in filtered if p.brand.lower() == filters.brand.lower()]
        
        # Filter by tags
        if filters.tags:
            filtered = [
                p for p in filtered 
                if any(tag.lower() in [t.lower() for t in p.tags] for tag in filters.tags)
            ]
        
        # Filter by availability
        if filters.available_only:
            filtered = [p for p in filtered if p.available]
        
        # Filter by discount
        if filters.has_discount is not None:
            if filters.has_discount:
                filtered = [p for p in filtered if p.has_discount]
            else:
                filtered = [p for p in filtered if not p.has_discount]
        
        # Filter by rating
        if filters.min_rating is not None:
            filtered = [
                p for p in filtered 
                if p.rating is not None and p.rating >= filters.min_rating
            ]
        
        # Sort products
        filtered = self._sort_products(filtered, filters.sort_by)
        
        return filtered
    
    def _sort_products(self, products: List[Product], sort_by: str) -> List[Product]:
        """Sort products based on sort_by parameter."""
        if sort_by == "price_low":
            return sorted(products, key=lambda p: p.price)
        elif sort_by == "price_high":
            return sorted(products, key=lambda p: p.price, reverse=True)
        elif sort_by == "rating":
            return sorted(products, key=lambda p: p.rating or 0, reverse=True)
        elif sort_by == "newest":
            return sorted(products, key=lambda p: p.created_at, reverse=True)
        else:  # relevance or default
            return products


class GetProductByIdUseCase:
    """Use case for getting a specific product by ID."""
    
    def __init__(self, repository: EcommerceRepository):
        self._repository = repository
    
    async def execute(self, product_id: str) -> Optional[Product]:
        """
        Get product by ID.
        
        Args:
            product_id: Product ID
        
        Returns:
            Product if found, None otherwise
        """
        try:
            logger.info(f"Getting product by ID: {product_id}")
            
            if not product_id or len(product_id.strip()) == 0:
                raise ValueError("Product ID cannot be empty")
            
            product = await self._repository.get_product_by_id(product_id.strip())
            
            if product:
                logger.info(f"Found product: {product.name}")
            else:
                logger.info(f"Product not found: {product_id}")
            
            return product
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting product by ID: {e}")
            raise


class GetTrendingProductsUseCase:
    """Use case for getting trending/popular products."""
    
    def __init__(self, repository: EcommerceRepository):
        self._repository = repository
    
    async def execute(
        self,
        request: TrendingProductsRequest,
        page: int = 1,
        page_size: int = 20
    ) -> ProductSearchResult:
        """
        Get trending products with pagination.
        
        Args:
            request: Trending products request
            page: Page number (1-based)
            page_size: Number of items per page
        
        Returns:
            ProductSearchResult with trending products
        """
        try:
            logger.info(
                f"Getting trending products: category={request.category}, "
                f"time_period={request.time_period}, limit={request.limit}"
            )
            
            if page_size <= 0 or page_size > 100:
                raise ValueError("Page size must be between 1 and 100")
            
            if page <= 0:
                raise ValueError("Page number must be greater than 0")
            
            # Get trending products
            products = await self._repository.get_trending_products(limit=request.limit * 2)
            
            # Filter by category if specified
            if request.category:
                products = [
                    product for product in products 
                    if product.category.lower() == request.category.lower()
                ]
            
            # Calculate pagination
            total_count = len(products)
            total_pages = (total_count + page_size - 1) // page_size
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            page_products = products[start_idx:end_idx]
            
            # Create filters for result
            filters = ProductSearchFilters(
                category=request.category,
                available_only=True,
                sort_by="relevance"
            )
            
            # Create result
            result = ProductSearchResult(
                products=page_products,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=max(1, total_pages),
                filters_applied=filters
            )
            
            logger.info(f"Found {total_count} trending products, returning {len(page_products)} for page {page}")
            return result
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting trending products: {e}")
            raise


class GetRecommendedProductsUseCase:
    """Use case for getting product recommendations based on user preferences."""
    
    def __init__(self, repository: EcommerceRepository):
        self._repository = repository
    
    async def execute(
        self,
        user_preferences: Dict[str, Any],
        limit: int = 10
    ) -> List[Product]:
        """
        Get product recommendations based on user preferences.
        
        Args:
            user_preferences: User style preferences and history
            limit: Maximum number of results
        
        Returns:
            List of recommended products
        """
        try:
            logger.info(f"Getting product recommendations: limit={limit}")
            
            if limit <= 0 or limit > 50:
                raise ValueError("Limit must be between 1 and 50")
            
            # Extract preferences
            preferred_styles = user_preferences.get("preferred_styles", [])
            preferred_colors = user_preferences.get("preferred_colors", [])
            price_range = user_preferences.get("price_range", {})
            
            # Build search query based on preferences
            if preferred_styles:
                query = preferred_styles[0]  # Use primary style
            else:
                query = "clothing"  # Default fallback
            
            # Apply price filters
            min_price = price_range.get("min")
            max_price = price_range.get("max")
            
            # Search for products based on preferences
            products = await self._repository.search_products(
                query=query,
                limit=limit,
                min_price=min_price,
                max_price=max_price
            )
            
            # Filter by color preferences if available
            if preferred_colors and products:
                filtered_products = []
                for product in products:
                    # Check if product tags or name contains preferred colors
                    product_text = f"{product.name} {' '.join(product.tags)}".lower()
                    if any(color.lower() in product_text for color in preferred_colors):
                        filtered_products.append(product)
                
                # If we have filtered results, use them; otherwise use all results
                if filtered_products:
                    products = filtered_products
            
            logger.info(f"Found {len(products)} recommended products")
            return products[:limit]
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting product recommendations: {e}")
            raise


class GetProductsByCategoryUseCase:
    """Use case for getting products by category."""
    
    def __init__(self, repository: EcommerceRepository):
        self._repository = repository
    
    async def execute(self, category: str, limit: int = 10) -> List[Product]:
        """
        Get products by category.
        
        Args:
            category: Product category
            limit: Maximum number of results
        
        Returns:
            List of products in the category
        """
        try:
            logger.info(f"Getting products by category: {category}, limit={limit}")
            
            if not category or len(category.strip()) == 0:
                raise ValueError("Category cannot be empty")
            
            if limit <= 0 or limit > 100:
                raise ValueError("Limit must be between 1 and 100")
            
            # Use a generic search with category filter
            products = await self._repository.search_products(
                query="clothing",  # Generic query
                limit=limit,
                category=category.strip()
            )
            
            logger.info(f"Found {len(products)} products in category '{category}'")
            return products
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting products by category: {e}")
            raise


class GetProductRecommendationsUseCase:
    """Use case for getting personalized product recommendations."""
    
    def __init__(self, repository: EcommerceRepository):
        self._repository = repository
    
    async def execute(
        self,
        user_id: str,
        category: Optional[str] = None,
        limit: int = 10
    ) -> ProductSearchResult:
        """
        Get personalized product recommendations for a user.
        
        Args:
            user_id: User ID for personalization
            category: Optional category filter
            limit: Maximum number of recommendations
        
        Returns:
            ProductSearchResult with recommended products
        """
        try:
            logger.info(
                f"Getting product recommendations for user: {user_id}, "
                f"category: {category}, limit: {limit}"
            )
            
            if not user_id or len(user_id.strip()) == 0:
                raise ValueError("User ID cannot be empty")
            
            if limit <= 0 or limit > 50:
                raise ValueError("Limit must be between 1 and 50")
            
            # For now, use trending products as recommendations
            # In a real implementation, this would use user history, preferences, etc.
            products = await self._repository.get_trending_products(limit=limit)
            
            # Filter by category if provided
            if category:
                products = [
                    product for product in products 
                    if product.category.lower() == category.lower()
                ]
            
            # Create search result
            result = ProductSearchResult(
                products=products,
                total_count=len(products),
                page=1,
                page_size=limit,
                total_pages=1,
                filters_applied=ProductSearchFilters(
                    category=category,
                    available_only=True,
                    sort_by="relevance"
                )
            )
            
            logger.info(f"Generated {len(products)} product recommendations")
            return result
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting product recommendations: {e}")
            raise
