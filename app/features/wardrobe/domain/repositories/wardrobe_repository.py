from abc import ABC, abstractmethod
from typing import List, Optional
from app.features.wardrobe.domain.entities import ClothingItem

class WardrobeRepository(ABC):
    """Abstract base class for wardrobe repository."""

    @abstractmethod
    async def add_clothing_item(self, item: ClothingItem) -> ClothingItem:
        """Add a new clothing item to the wardrobe."""
        pass

    @abstractmethod
    async def get_clothing_item(self, item_id: str) -> Optional[ClothingItem]:
        """Retrieve a clothing item by its ID."""
        pass

    @abstractmethod
    async def list_clothing_items(self, user_id: str) -> List[ClothingItem]:
        """List all clothing items for a user."""
        pass

    @abstractmethod
    async def update_clothing_item(self, item: ClothingItem) -> ClothingItem:
        """Update an existing clothing item."""
        pass

    @abstractmethod
    async def delete_clothing_item(self, item_id: str) -> None:
        """Delete a clothing item by its ID."""
        pass
