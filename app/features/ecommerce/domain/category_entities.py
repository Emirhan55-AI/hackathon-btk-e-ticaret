"""Product categories domain entities."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4


@dataclass
class Category:
    """Product category entity."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    slug: str = ""
    description: Optional[str] = None
    parent_id: Optional[str] = None
    level: int = 0
    sort_order: int = 0
    is_active: bool = True
    image_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def is_root_category(self) -> bool:
        """Check if this is a root category."""
        return self.parent_id is None
    
    @property
    def is_leaf_category(self) -> bool:
        """Check if this is a leaf category (no children)."""
        # This would need to be determined by checking children count
        # In a real implementation, this would be computed based on actual data
        return True  # Placeholder


@dataclass
class CategoryTree:
    """Category tree structure."""
    
    categories: List[Category] = field(default_factory=list)
    
    def get_root_categories(self) -> List[Category]:
        """Get all root categories."""
        return [cat for cat in self.categories if cat.is_root_category]
    
    def get_children(self, parent_id: str) -> List[Category]:
        """Get children of a specific category."""
        return [cat for cat in self.categories if cat.parent_id == parent_id]
    
    def get_category_path(self, category_id: str) -> List[Category]:
        """Get the full path from root to the specified category."""
        path = []
        category = self.find_category(category_id)
        
        while category:
            path.insert(0, category)
            if category.parent_id:
                category = self.find_category(category.parent_id)
            else:
                break
        
        return path
    
    def find_category(self, category_id: str) -> Optional[Category]:
        """Find category by ID."""
        for category in self.categories:
            if category.id == category_id:
                return category
        return None
    
    def find_by_slug(self, slug: str) -> Optional[Category]:
        """Find category by slug."""
        for category in self.categories:
            if category.slug == slug:
                return category
        return None
