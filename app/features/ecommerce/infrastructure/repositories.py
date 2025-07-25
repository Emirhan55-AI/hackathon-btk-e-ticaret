from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import httpx
import logging
from datetime import datetime

from app.features.ecommerce.domain.entities import Product

logger = logging.getLogger(__name__)


class EcommerceRepository(ABC):
    """Abstract repository interface for e-commerce operations."""
    
    @abstractmethod
    async def search_products(
        self, 
        query: str, 
        limit: int = 10, 
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """Search for products based on query and filters."""
        pass
    
    @abstractmethod
    async def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a specific product by ID."""
        pass
    
    @abstractmethod
    async def get_trending_products(self, limit: int = 10) -> List[Product]:
        """Get trending/popular products."""
        pass


class HttpEcommerceRepository(EcommerceRepository):
    """HTTP-based e-commerce repository using external APIs."""
    
    def __init__(self, http_client: httpx.AsyncClient):
        self._http_client = http_client
        self.base_url = "https://dummyjson.com"  # Free API for demo
        self.timeout = 30.0
    
    async def search_products(
        self, 
        query: str, 
        limit: int = 10, 
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """Search for products using external API."""
        try:
            logger.info(f"Searching products with query: {query}")
            
            # Use DummyJSON API for demo
            url = f"{self.base_url}/products/search"
            params = {
                "q": query,
                "limit": limit
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    products = []
                    
                    for item in data.get("products", []):
                        # Filter by category if specified
                        if category and category.lower() not in item.get("category", "").lower():
                            continue
                        
                        # Filter by price range if specified
                        price = item.get("price", 0)
                        if min_price and price < min_price:
                            continue
                        if max_price and price > max_price:
                            continue
                        
                        product = self._json_to_product(item)
                        products.append(product)
                    
                    return products[:limit]
                else:
                    logger.warning(f"External API returned {response.status_code}")
                    return self._generate_fallback_products(query, limit)
                    
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return self._generate_fallback_products(query, limit)
    
    async def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a specific product by ID."""
        try:
            logger.info(f"Getting product by ID: {product_id}")
            
            url = f"{self.base_url}/products/{product_id}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._json_to_product(data)
                else:
                    logger.warning(f"Product not found: {product_id}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting product by ID: {e}")
            return None
    
    async def get_trending_products(self, limit: int = 10) -> List[Product]:
        """Get trending/popular products."""
        try:
            logger.info("Getting trending products")
            
            url = f"{self.base_url}/products"
            params = {
                "limit": limit,
                "skip": 0
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    products = []
                    
                    for item in data.get("products", []):
                        product = self._json_to_product(item)
                        products.append(product)
                    
                    return products
                else:
                    logger.warning(f"External API returned {response.status_code}")
                    return self._generate_trending_fallback(limit)
                    
        except Exception as e:
            logger.error(f"Error getting trending products: {e}")
            return self._generate_trending_fallback(limit)
    
    def _json_to_product(self, data: Dict[str, Any]) -> Product:
        """Convert JSON data to Product entity."""
        return Product(
            id=str(data.get("id", "")),
            name=data.get("title", "Unknown Product"),
            description=data.get("description", ""),
            price=float(data.get("price", 0)),
            currency="USD",
            category=data.get("category", "general"),
            brand=data.get("brand", "Unknown"),
            image_url=data.get("thumbnail", ""),
            additional_images=data.get("images", []),
            rating=float(data.get("rating", 0)),
            stock_quantity=data.get("stock", 0),
            tags=data.get("tags", []),
            discount_percentage=float(data.get("discountPercentage", 0)),
            metadata={
                "sku": data.get("sku", ""),
                "weight": data.get("weight", 0),
                "dimensions": data.get("dimensions", {}),
                "warranty": data.get("warrantyInformation", ""),
                "shipping": data.get("shippingInformation", ""),
                "availability": data.get("availabilityStatus", ""),
                "return_policy": data.get("returnPolicy", ""),
                "minimum_order": data.get("minimumOrderQuantity", 1)
            }
        )
    
    def _generate_fallback_products(self, query: str, limit: int) -> List[Product]:
        """Generate fallback products when external API is unavailable."""
        logger.info("Generating fallback products")
        
        fallback_products = [
            Product(
                id="fallback-1",
                name=f"Classic {query.title()} Item",
                description=f"A classic {query} item perfect for any occasion.",
                price=29.99,
                currency="USD",
                category="fashion",
                brand="Generic",
                image_url="https://via.placeholder.com/300x300?text=Classic+Item",
                rating=4.0,
                stock_quantity=50,
                tags=[query, "classic", "versatile"],
                discount_percentage=0
            ),
            Product(
                id="fallback-2",
                name=f"Premium {query.title()} Collection",
                description=f"Premium quality {query} from our exclusive collection.",
                price=79.99,
                currency="USD",
                category="fashion",
                brand="Premium",
                image_url="https://via.placeholder.com/300x300?text=Premium+Item",
                rating=4.5,
                stock_quantity=25,
                tags=[query, "premium", "quality"],
                discount_percentage=10
            ),
            Product(
                id="fallback-3",
                name=f"Budget {query.title()} Option",
                description=f"Affordable {query} option without compromising style.",
                price=19.99,
                currency="USD",
                category="fashion",
                brand="Budget",
                image_url="https://via.placeholder.com/300x300?text=Budget+Item",
                rating=3.5,
                stock_quantity=100,
                tags=[query, "budget", "affordable"],
                discount_percentage=5
            )
        ]
        
        return fallback_products[:limit]
    
    def _generate_trending_fallback(self, limit: int) -> List[Product]:
        """Generate fallback trending products."""
        trending_items = [
            "jacket", "jeans", "dress", "shoes", "shirt", 
            "sweater", "coat", "pants", "skirt", "blouse"
        ]
        
        products = []
        for i, item in enumerate(trending_items[:limit]):
            product = Product(
                id=f"trending-{i+1}",
                name=f"Trending {item.title()}",
                description=f"Currently trending {item} in our collection.",
                price=49.99 + (i * 10),
                currency="USD",
                category="fashion",
                brand="Trending",
                image_url=f"https://via.placeholder.com/300x300?text=Trending+{item.title()}",
                rating=4.2 + (i * 0.1),
                stock_quantity=75 - (i * 5),
                tags=[item, "trending", "popular"],
                discount_percentage=15 if i % 2 == 0 else 0
            )
            products.append(product)
        
        return products


class DummyEcommerceRepository(EcommerceRepository):
    """Dummy repository for testing and fallback scenarios."""
    
    async def search_products(
        self, 
        query: str, 
        limit: int = 10, 
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """Return dummy search results."""
        dummy_products = [
            Product(
                id="dummy-1",
                name=f"Sample {query.title()} Product",
                description=f"This is a sample {query} product for demonstration.",
                price=39.99,
                currency="USD",
                category=category or "general",
                brand="Demo Brand",
                image_url="https://via.placeholder.com/300x300?text=Sample+Product",
                rating=4.0,
                stock_quantity=10,
                tags=[query, "sample", "demo"]
            )
        ]
        
        return dummy_products[:limit]
    
    async def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Return a dummy product."""
        return Product(
            id=product_id,
            name="Sample Product",
            description="This is a sample product for demonstration.",
            price=39.99,
            currency="USD",
            category="general",
            brand="Demo Brand",
            image_url="https://via.placeholder.com/300x300?text=Sample+Product",
            rating=4.0,
            stock_quantity=10,
            tags=["sample", "demo"]
        )
    
    async def get_trending_products(self, limit: int = 10) -> List[Product]:
        """Return dummy trending products."""
        trending = []
        for i in range(min(limit, 5)):
            product = Product(
                id=f"trending-dummy-{i+1}",
                name=f"Trending Item {i+1}",
                description=f"This is trending item number {i+1}.",
                price=29.99 + (i * 10),
                currency="USD",
                category="trending",
                brand="Trending Brand",
                image_url=f"https://via.placeholder.com/300x300?text=Trending+{i+1}",
                rating=4.0 + (i * 0.2),
                stock_quantity=20 - i,
                tags=["trending", "popular", f"item-{i+1}"]
            )
            trending.append(product)
        
        return trending
