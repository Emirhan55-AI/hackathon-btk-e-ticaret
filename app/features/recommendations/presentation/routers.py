from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import Provide, inject
from typing import Optional
import logging

from app.features.recommendations.application.schemas import (
    GenerateOutfitRequest, 
    OutfitResponse,
    QuickRecommendationRequest,
    RecommendationErrorResponse
)
from app.features.recommendations.application.use_cases import (
    GenerateRecommendationsUseCase,
    GenerateQuickRecommendationsUseCase
)
from app.features.auth.presentation.dependencies import get_current_user
from app.features.auth.domain.entities import User
from app.core.di import Container

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/outfits", response_model=OutfitResponse)
@inject
async def get_outfit_recommendations(
    occasion: Optional[str] = None,
    season: Optional[str] = None,
    weather: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    use_case: GenerateRecommendationsUseCase = Depends(Provide[Container.generate_recommendations_usecase])
):
    """Generate outfit recommendations for the current user."""
    try:
        logger.info(f"Generating outfit recommendations for user {current_user.id}")
        
        request = GenerateOutfitRequest(
            user_id=current_user.id,
            occasion=occasion,
            season=season,
            weather=weather
        )
        
        return await use_case.execute(request)
        
    except ValueError as e:
        if "style quiz" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "NO_STYLE_DNA",
                    "message": str(e),
                    "suggestion": "Please complete the style quiz first to get personalized recommendations"
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating outfit recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.post("/outfits", response_model=OutfitResponse)
@inject
async def generate_custom_outfit_recommendations(
    request: GenerateOutfitRequest,
    current_user: User = Depends(get_current_user),
    use_case: GenerateRecommendationsUseCase = Depends(Provide[Container.generate_recommendations_usecase])
):
    """Generate custom outfit recommendations with specific parameters."""
    try:
        logger.info(f"Generating custom outfit recommendations for user {current_user.id}")
        
        # Ensure the request is for the current user
        request.user_id = current_user.id
        
        return await use_case.execute(request)
        
    except ValueError as e:
        if "style quiz" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "NO_STYLE_DNA",
                    "message": str(e),
                    "suggestion": "Please complete the style quiz first to get personalized recommendations"
                }
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating custom outfit recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate custom recommendations: {str(e)}"
        )


@router.get("/quick", response_model=OutfitResponse)
@inject
async def get_quick_recommendations(
    occasion: Optional[str] = None,
    weather: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    use_case: GenerateQuickRecommendationsUseCase = Depends(Provide[Container.generate_quick_recommendations_usecase])
):
    """Generate quick outfit recommendations without requiring full wardrobe analysis."""
    try:
        logger.info(f"Generating quick recommendations for user {current_user.id}")
        
        return await use_case.execute(
            user_id=current_user.id,
            occasion=occasion,
            weather=weather
        )
        
    except Exception as e:
        logger.error(f"Error generating quick recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quick recommendations: {str(e)}"
        )


@router.post("/quick", response_model=OutfitResponse)
@inject
async def generate_quick_recommendations_with_params(
    request: QuickRecommendationRequest,
    current_user: User = Depends(get_current_user),
    use_case: GenerateQuickRecommendationsUseCase = Depends(Provide[Container.generate_quick_recommendations_usecase])
):
    """Generate quick outfit recommendations with specific parameters."""
    try:
        logger.info(f"Generating quick recommendations with params for user {current_user.id}")
        
        return await use_case.execute(
            user_id=current_user.id,
            occasion=request.occasion,
            weather=request.weather
        )
        
    except Exception as e:
        logger.error(f"Error generating quick recommendations with params: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quick recommendations: {str(e)}"
        )
