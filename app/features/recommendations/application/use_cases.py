import uuid
from datetime import datetime
from typing import List, Optional
import logging

from app.features.recommendations.infrastructure.ai_service_client import AIServiceClient
from app.features.recommendations.application.schemas import (
    GenerateOutfitRequest, OutfitResponse
)
from app.features.recommendations.domain.entities import Outfit
from app.features.style_quiz.infrastructure.repositories import StyleDNARepository
from app.features.wardrobe.infrastructure.repositories import WardrobeRepository

logger = logging.getLogger(__name__)


class GenerateRecommendationsUseCase:
    """Use case for generating outfit recommendations."""

    def __init__(
        self,
        ai_client: AIServiceClient,
        style_dna_repository: StyleDNARepository,
        wardrobe_repository: WardrobeRepository
    ):
        self._ai_client = ai_client
        self._style_dna_repository = style_dna_repository
        self._wardrobe_repository = wardrobe_repository

    async def execute(self, request: GenerateOutfitRequest) -> OutfitResponse:
        """Generate outfit recommendations for a user."""
        try:
            logger.info(f"Generating recommendations for user {request.user_id}")
            
            # Get user's style DNA
            style_dna = await self._style_dna_repository.get_by_user_id(request.user_id)
            if not style_dna:
                logger.warning(f"No style DNA found for user {request.user_id}")
                # Create a basic profile or throw error
                raise ValueError("User must complete style quiz first")
            
            # Get user's wardrobe items
            wardrobe_items = await self._wardrobe_repository.get_by_user_id(request.user_id)
            
            # Prepare data for AI service
            ai_request_data = {
                "user_id": str(request.user_id),
                "style_profile": style_dna.style_profile,
                "preferred_styles": style_dna.preferred_styles,
                "preferred_colors": style_dna.preferred_colors,
                "lifestyle_factors": style_dna.lifestyle_factors,
                "wardrobe_items": [
                    {
                        "id": str(item.id),
                        "category": item.category,
                        "color": item.color,
                        "style": item.style,
                        "tags": item.tags
                    } for item in wardrobe_items
                ],
                "occasion": request.occasion,
                "season": request.season,
                "weather": request.weather
            }
            
            # Generate recommendations using AI service
            ai_response = await self._ai_client.generate_outfit_recommendations(ai_request_data)
            
            # Convert AI response to Outfit entities
            outfits = []
            for ai_outfit in ai_response.get("outfits", []):
                outfit = Outfit.create_ai_generated(
                    user_id=request.user_id,
                    name=ai_outfit.get("name", "AI Generated Outfit"),
                    clothing_item_ids=[uuid.UUID(item_id) for item_id in ai_outfit.get("item_ids", [])],
                    occasion=ai_outfit.get("occasion"),
                    season=ai_outfit.get("season"),
                    confidence_score=ai_outfit.get("confidence_score"),
                    styling_tips=ai_outfit.get("styling_tips", [])
                )
                outfits.append(outfit)
            
            return OutfitResponse(
                user_id=request.user_id,
                outfits=outfits,
                generated_at=datetime.utcnow(),
                total_recommendations=len(outfits),
                request_context={
                    "occasion": request.occasion,
                    "season": request.season,
                    "weather": request.weather
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise


class GenerateQuickRecommendationsUseCase:
    """Use case for generating quick recommendations without full wardrobe analysis."""

    def __init__(self, ai_client: AIServiceClient, style_dna_repository: StyleDNARepository):
        self._ai_client = ai_client
        self._style_dna_repository = style_dna_repository

    async def execute(
        self, 
        user_id: uuid.UUID, 
        occasion: Optional[str] = None,
        weather: Optional[str] = None
    ) -> OutfitResponse:
        """Generate quick outfit recommendations."""
        try:
            logger.info(f"Generating quick recommendations for user {user_id}")
            
            # Get user's style DNA
            style_dna = await self._style_dna_repository.get_by_user_id(user_id)
            
            # Prepare minimal request for AI service
            ai_request_data = {
                "user_id": str(user_id),
                "quick_mode": True,
                "style_profile": style_dna.style_profile if style_dna else {},
                "preferred_styles": style_dna.preferred_styles if style_dna else [],
                "preferred_colors": style_dna.preferred_colors if style_dna else [],
                "occasion": occasion,
                "weather": weather
            }
            
            # Generate recommendations using AI service
            ai_response = await self._ai_client.generate_quick_recommendations(ai_request_data)
            
            # Convert to simplified outfits (these would be suggestions to purchase)
            outfits = []
            for ai_outfit in ai_response.get("outfits", []):
                outfit = Outfit.create_ai_generated(
                    user_id=user_id,
                    name=ai_outfit.get("name", "Quick Recommendation"),
                    clothing_item_ids=[],  # Empty for purchase recommendations
                    occasion=ai_outfit.get("occasion"),
                    confidence_score=ai_outfit.get("confidence_score"),
                    styling_tips=ai_outfit.get("styling_tips", [])
                )
                outfits.append(outfit)
            
            return OutfitResponse(
                user_id=user_id,
                outfits=outfits,
                generated_at=datetime.utcnow(),
                total_recommendations=len(outfits),
                request_context={
                    "quick_mode": True,
                    "occasion": occasion,
                    "weather": weather
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating quick recommendations: {e}")
            raise
