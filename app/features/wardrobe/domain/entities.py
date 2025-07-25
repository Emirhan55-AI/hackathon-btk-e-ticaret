from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


@dataclass
class ClothingItem:
    """ClothingItem domain entity representing a piece of clothing in the wardrobe."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    category: str
    brand: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    image_url: Optional[str] = None
    ai_tags: Dict[str, Any] = field(default_factory=dict)
    user_tags: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None
    is_favorite: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Clothing item name is required")
        
        if not self.category or len(self.category.strip()) == 0:
            raise ValueError("Clothing item category is required")
        
        # Normalize category to lowercase
        self.category = self.category.lower().strip()
        
        # Normalize color to lowercase if provided
        if self.color:
            self.color = self.color.lower().strip()
    
    @classmethod
    def create_new(
        cls,
        user_id: uuid.UUID,
        name: str,
        category: str,
        brand: Optional[str] = None,
        color: Optional[str] = None,
        size: Optional[str] = None,
        image_url: Optional[str] = None,
        description: Optional[str] = None
    ) -> "ClothingItem":
        """Create a new clothing item instance."""
        return cls(
            id=uuid.uuid4(),
            user_id=user_id,
            name=name.strip(),
            category=category.strip(),
            brand=brand.strip() if brand else None,
            color=color.strip() if color else None,
            size=size.strip() if size else None,
            image_url=image_url,
            description=description.strip() if description else None,
            ai_tags={},
            user_tags={},
            is_favorite=False
        )
    
    def update_ai_tags(self, tags: Dict[str, Any]) -> None:
        """Update AI-generated tags."""
        if not isinstance(tags, dict):
            raise ValueError("AI tags must be a dictionary")
        self.ai_tags = tags
    
    def update_user_tags(self, tags: Dict[str, Any]) -> None:
        """Update user-modified tags."""
        if not isinstance(tags, dict):
            raise ValueError("User tags must be a dictionary")
        self.user_tags = tags
    
    def add_user_tag(self, key: str, value: Any) -> None:
        """Add a single user tag."""
        self.user_tags[key] = value
    
    def remove_user_tag(self, key: str) -> None:
        """Remove a user tag."""
        self.user_tags.pop(key, None)
    
    def toggle_favorite(self) -> None:
        """Toggle favorite status."""
        self.is_favorite = not self.is_favorite
    
    def get_effective_tags(self) -> Dict[str, Any]:
        """Get combined tags (user tags override AI tags)."""
        effective_tags = self.ai_tags.copy()
        effective_tags.update(self.user_tags)
        return effective_tags
    
    def matches_criteria(self, **criteria) -> bool:
        """Check if item matches given criteria."""
        effective_tags = self.get_effective_tags()
        
        for key, value in criteria.items():
            if key == "category":
                if self.category != value.lower():
                    return False
            elif key == "color":
                if self.color != value.lower():
                    return False
            elif key == "brand":
                if self.brand != value:
                    return False
            elif key in effective_tags:
                if effective_tags[key] != value:
                    return False
            else:
                return False
        
        return True
