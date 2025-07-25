from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.features.recommendations.application.schemas import OutfitRecommendation, StyleDNAProfile

class AIRecommendationService(ABC):
    """Abstract interface for AI recommendation service."""
    
    @abstractmethod
    async def generate_outfit_recommendations(
        self, 
        style_profile: StyleDNAProfile,
        occasion: str = None,
        weather: str = None
    ) -> List[OutfitRecommendation]:
        """Generate outfit recommendations based on user's style profile."""
        pass
    
    @abstractmethod
    async def analyze_style_preferences(
        self, 
        quiz_answers: List[Dict[str, Any]]
    ) -> StyleDNAProfile:
        """Analyze quiz answers to create/update style DNA profile."""
        pass
