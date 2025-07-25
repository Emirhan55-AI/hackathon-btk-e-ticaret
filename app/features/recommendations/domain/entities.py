from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid


@dataclass
class Outfit:
    """Outfit domain entity representing a clothing combination."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    clothing_item_ids: List[uuid.UUID]
    occasion: Optional[str] = None
    season: Optional[str] = None
    description: Optional[str] = None
    styling_tips: List[str] = field(default_factory=list)
    user_rating: Optional[int] = None
    is_favorite: bool = False
    is_ai_generated: bool = True
    confidence_score: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Outfit name is required")
        
        if not self.clothing_item_ids or len(self.clothing_item_ids) == 0:
            raise ValueError("Outfit must contain at least one clothing item")
        
        if self.user_rating is not None and not (1 <= self.user_rating <= 5):
            raise ValueError("User rating must be between 1 and 5")
        
        if self.confidence_score is not None and not (0 <= self.confidence_score <= 1):
            raise ValueError("Confidence score must be between 0 and 1")
    
    @classmethod
    def create_ai_generated(
        cls,
        user_id: uuid.UUID,
        name: str,
        clothing_item_ids: List[uuid.UUID],
        occasion: Optional[str] = None,
        season: Optional[str] = None,
        confidence_score: Optional[float] = None,
        styling_tips: Optional[List[str]] = None
    ) -> "Outfit":
        """Create a new AI-generated outfit."""
        return cls(
            id=uuid.uuid4(),
            user_id=user_id,
            name=name.strip(),
            clothing_item_ids=clothing_item_ids,
            occasion=occasion,
            season=season,
            styling_tips=styling_tips or [],
            is_ai_generated=True,
            confidence_score=confidence_score,
            is_favorite=False
        )
    
    @classmethod
    def create_user_generated(
        cls,
        user_id: uuid.UUID,
        name: str,
        clothing_item_ids: List[uuid.UUID],
        occasion: Optional[str] = None,
        season: Optional[str] = None,
        description: Optional[str] = None
    ) -> "Outfit":
        """Create a new user-generated outfit."""
        return cls(
            id=uuid.uuid4(),
            user_id=user_id,
            name=name.strip(),
            clothing_item_ids=clothing_item_ids,
            occasion=occasion,
            season=season,
            description=description,
            is_ai_generated=False,
            is_favorite=False
        )
    
    def add_clothing_item(self, item_id: uuid.UUID) -> None:
        """Add a clothing item to the outfit."""
        if item_id not in self.clothing_item_ids:
            self.clothing_item_ids.append(item_id)
    
    def remove_clothing_item(self, item_id: uuid.UUID) -> None:
        """Remove a clothing item from the outfit."""
        if item_id in self.clothing_item_ids:
            self.clothing_item_ids.remove(item_id)
    
    def add_styling_tip(self, tip: str) -> None:
        """Add a styling tip."""
        if tip and tip not in self.styling_tips:
            self.styling_tips.append(tip.strip())
    
    def remove_styling_tip(self, tip: str) -> None:
        """Remove a styling tip."""
        if tip in self.styling_tips:
            self.styling_tips.remove(tip)
    
    def rate_outfit(self, rating: int) -> None:
        """Rate the outfit (1-5 stars)."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.user_rating = rating
    
    def toggle_favorite(self) -> None:
        """Toggle favorite status."""
        self.is_favorite = not self.is_favorite
    
    def update_confidence(self, score: float) -> None:
        """Update confidence score."""
        if not (0 <= score <= 1):
            raise ValueError("Confidence score must be between 0 and 1")
        self.confidence_score = score
    
    def get_item_count(self) -> int:
        """Get the number of clothing items in the outfit."""
        return len(self.clothing_item_ids)
    
    def is_complete_outfit(self) -> bool:
        """Check if outfit contains items from multiple categories (basic completeness check)."""
        # This would need actual clothing items to check categories
        # For now, we assume an outfit with 2+ items is potentially complete
        return len(self.clothing_item_ids) >= 2
    
    def matches_occasion(self, occasion: str) -> bool:
        """Check if outfit matches a specific occasion."""
        if not self.occasion:
            return False
        return self.occasion.lower() == occasion.lower()
    
    def matches_season(self, season: str) -> bool:
        """Check if outfit matches a specific season."""
        if not self.season:
            return True  # Season-neutral outfits match any season
        return self.season.lower() == season.lower()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the outfit."""
        return {
            "id": str(self.id),
            "name": self.name,
            "item_count": self.get_item_count(),
            "occasion": self.occasion,
            "season": self.season,
            "is_ai_generated": self.is_ai_generated,
            "is_favorite": self.is_favorite,
            "user_rating": self.user_rating,
            "confidence_score": self.confidence_score,
            "is_complete": self.is_complete_outfit()
        }
