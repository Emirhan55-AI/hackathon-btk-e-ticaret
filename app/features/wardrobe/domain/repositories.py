from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import uuid
from app.features.wardrobe.domain.entities import ClothingItem


class WardrobeRepository(ABC):
    """Abstract repository interface for wardrobe operations."""
    
    @abstractmethod
    async def get_clothing_item_by_id(self, item_id: uuid.UUID) -> Optional[ClothingItem]:
        """Get clothing item by ID."""
        pass
    
    @abstractmethod
    async def get_user_clothing_items(
        self, 
        user_id: uuid.UUID,
        category: Optional[str] = None,
        color: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[ClothingItem]:
        """Get user's clothing items with optional filters."""
        pass
    
    @abstractmethod
    async def create_clothing_item(self, item: ClothingItem) -> ClothingItem:
        """Create a new clothing item."""
        pass
    
    @abstractmethod
    async def update_clothing_item(self, item: ClothingItem) -> ClothingItem:
        """Update existing clothing item."""
        pass
    
    @abstractmethod
    async def delete_clothing_item(self, item_id: uuid.UUID) -> bool:
        """Delete clothing item by ID."""
        pass
    
    @abstractmethod
    async def get_user_clothing_count(self, user_id: uuid.UUID) -> int:
        """Get total count of user's clothing items."""
        pass
    
    @abstractmethod
    async def search_clothing_items(
        self,
        user_id: uuid.UUID,
        search_term: str,
        limit: Optional[int] = None
    ) -> List[ClothingItem]:
        """Search clothing items by name, brand, or tags."""
        pass
