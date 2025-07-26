"""Recommendations domain repositories."""
from abc import ABC, abstractmethod
from typing import Optional, List
import uuid

from app.features.recommendations.domain.entities import Recommendation


class RecommendationsRepository(ABC):
    """Abstract repository interface for recommendations operations."""
    
    @abstractmethod
    async def get_recommendations_by_user_id(
        self, 
        user_id: uuid.UUID,
        limit: Optional[int] = None
    ) -> List[Recommendation]:
        """Get recommendations for a user."""
        pass
    
    @abstractmethod
    async def save_recommendation(self, recommendation: Recommendation) -> Recommendation:
        """Save a recommendation."""
        pass
    
    @abstractmethod
    async def delete_recommendation(self, recommendation_id: uuid.UUID) -> bool:
        """Delete a recommendation."""
        pass
    
    @abstractmethod
    async def get_recommendation_by_id(
        self, 
        recommendation_id: uuid.UUID
    ) -> Optional[Recommendation]:
        """Get a recommendation by ID."""
        pass
