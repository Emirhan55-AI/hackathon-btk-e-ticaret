import uuid
from datetime import datetime
from typing import List
from app.features.recommendations.domain.services import AIRecommendationService
from app.features.recommendations.application.schemas import (
    GenerateOutfitRequest, OutfitResponse, StyleDNAProfile
)

class GenerateOutfitRecommendationsUseCase:
    """Use case for generating outfit recommendations."""

    def __init__(self, ai_service: AIRecommendationService):
        self.ai_service = ai_service

    async def execute(self, request: GenerateOutfitRequest) -> OutfitResponse:
        """Generate outfit recommendations for a user."""
        # Create a basic style profile (in real implementation, this would come from database)
        style_profile = StyleDNAProfile(
            user_id=request.user_id,
            style_preferences=request.style_preferences or {},
            color_palette=request.color_preferences or [],
            preferred_occasions=[request.occasion] if request.occasion else [],
            fit_preferences={},
            updated_at=datetime.utcnow()
        )
        
        # Generate recommendations using AI service
        recommendations = await self.ai_service.generate_outfit_recommendations(
            style_profile=style_profile,
            occasion=request.occasion,
            weather=request.weather
        )
        
        return OutfitResponse(
            user_id=request.user_id,
            recommendations=recommendations,
            generated_at=datetime.utcnow(),
            total_recommendations=len(recommendations)
        )

class AnalyzeStyleDNAUseCase:
    """Use case for analyzing style preferences from quiz answers."""

    def __init__(self, ai_service: AIRecommendationService):
        self.ai_service = ai_service

    async def execute(self, user_id: uuid.UUID, quiz_answers: List[dict]) -> StyleDNAProfile:
        """Analyze quiz answers to create/update user's style DNA."""
        # Add user_id to quiz answers for processing
        enriched_answers = [{"user_id": str(user_id), **answer} for answer in quiz_answers]
        
        # Analyze using AI service
        style_profile = await self.ai_service.analyze_style_preferences(enriched_answers)
        
        # In a real implementation, you would save this to database here
        
        return style_profile
