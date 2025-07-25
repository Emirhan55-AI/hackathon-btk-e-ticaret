import httpx
import uuid
from datetime import datetime
from typing import List, Dict, Any
from app.features.recommendations.domain.services import AIRecommendationService
from app.features.recommendations.application.schemas import (
    OutfitRecommendation, StyleDNAProfile, OutfitItem
)
from app.core.config import settings
import logging

logger = logging.getLogger("app.features.recommendations.infrastructure.ai_service_client")

class AIServiceClient(AIRecommendationService):
    """Concrete implementation of AI recommendation service."""
    
    def __init__(self):
        self.base_url = settings.ai_service_url
        self.api_key = settings.ai_service_api_key
    
    async def generate_outfit_recommendations(
        self, 
        style_profile: StyleDNAProfile,
        occasion: str = None,
        weather: str = None
    ) -> List[OutfitRecommendation]:
        """Generate outfit recommendations based on user's style profile."""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "style_profile": style_profile.dict(),
                    "occasion": occasion,
                    "weather": weather
                }
                
                response = await client.post(
                    f"{self.base_url}/recommendations/outfits",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_outfit_recommendations(data)
                else:
                    logger.warning(f"AI service returned {response.status_code}")
                    return self._fallback_recommendations()
                    
        except Exception as e:
            logger.error(f"Error calling AI service: {e}")
            return self._fallback_recommendations()
    
    async def analyze_style_preferences(
        self, 
        quiz_answers: List[Dict[str, Any]]
    ) -> StyleDNAProfile:
        """Analyze quiz answers to create/update style DNA profile."""
        try:
            async with httpx.AsyncClient() as client:
                payload = {"quiz_answers": quiz_answers}
                
                response = await client.post(
                    f"{self.base_url}/analyze/style-dna",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_style_dna(data, quiz_answers[0].get("user_id"))
                else:
                    logger.warning(f"AI service returned {response.status_code}")
                    return self._fallback_style_dna(quiz_answers[0].get("user_id"))
                    
        except Exception as e:
            logger.error(f"Error analyzing style preferences: {e}")
            return self._fallback_style_dna(quiz_answers[0].get("user_id"))
    
    def _parse_outfit_recommendations(self, data: Dict[str, Any]) -> List[OutfitRecommendation]:
        """Parse AI service response into outfit recommendations."""
        recommendations = []
        for outfit_data in data.get("outfits", []):
            items = [
                OutfitItem(
                    item_id=uuid.UUID(item["id"]),
                    name=item["name"],
                    category=item["category"],
                    color=item["color"],
                    confidence_score=item.get("confidence", 0.8)
                )
                for item in outfit_data.get("items", [])
            ]
            
            recommendation = OutfitRecommendation(
                outfit_id=uuid.uuid4(),
                items=items,
                style_tags=outfit_data.get("style_tags", []),
                occasion=outfit_data.get("occasion", "casual"),
                confidence_score=outfit_data.get("confidence", 0.8),
                explanation=outfit_data.get("explanation", "AI-generated outfit recommendation")
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _parse_style_dna(self, data: Dict[str, Any], user_id: str) -> StyleDNAProfile:
        """Parse AI service response into style DNA profile."""
        return StyleDNAProfile(
            user_id=uuid.UUID(user_id),
            style_preferences=data.get("style_preferences", {}),
            color_palette=data.get("color_palette", []),
            preferred_occasions=data.get("preferred_occasions", []),
            fit_preferences=data.get("fit_preferences", {}),
            updated_at=datetime.utcnow()
        )
    
    def _fallback_recommendations(self) -> List[OutfitRecommendation]:
        """Provide fallback recommendations when AI service is unavailable."""
        return [
            OutfitRecommendation(
                outfit_id=uuid.uuid4(),
                items=[
                    OutfitItem(
                        item_id=uuid.uuid4(),
                        name="Classic White Shirt",
                        category="tops",
                        color="white",
                        confidence_score=0.7
                    )
                ],
                style_tags=["classic", "versatile"],
                occasion="casual",
                confidence_score=0.7,
                explanation="Fallback recommendation - classic versatile piece"
            )
        ]
    
    def _fallback_style_dna(self, user_id: str) -> StyleDNAProfile:
        """Provide fallback style DNA when AI service is unavailable."""
        return StyleDNAProfile(
            user_id=uuid.UUID(user_id),
            style_preferences={"style": "classic", "preference_score": 0.5},
            color_palette=["black", "white", "navy"],
            preferred_occasions=["casual", "work"],
            fit_preferences={"tops": "fitted", "bottoms": "straight"},
            updated_at=datetime.utcnow()
        )
