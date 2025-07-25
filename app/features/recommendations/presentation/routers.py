from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional
import uuid

from app.features.recommendations.application.schemas import (
    GenerateOutfitRequest, OutfitResponse
)
from app.features.recommendations.application.use_cases import (
    GenerateOutfitRecommendationsUseCase
)
from app.features.recommendations.infrastructure.ai_service_client import AIServiceClient
from app.features.auth.presentation.dependencies import get_current_user
from app.features.auth.domain.entities import User

router = APIRouter()

# Dependency injection
def get_ai_service() -> AIServiceClient:
    return AIServiceClient()

def get_generate_outfit_use_case(
    ai_service: AIServiceClient = Depends(get_ai_service)
) -> GenerateOutfitRecommendationsUseCase:
    return GenerateOutfitRecommendationsUseCase(ai_service)

@router.get("/outfits", response_model=OutfitResponse)
async def get_outfit_recommendations(
    occasion: Optional[str] = None,
    weather: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    use_case: GenerateOutfitRecommendationsUseCase = Depends(get_generate_outfit_use_case)
):
    """Generate outfit recommendations for the current user."""
    try:
        request = GenerateOutfitRequest(
            user_id=current_user.id,
            occasion=occasion,
            weather=weather
        )
        
        return await use_case.execute(request)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@router.post("/outfits", response_model=OutfitResponse)
async def generate_custom_outfit_recommendations(
    request: GenerateOutfitRequest,
    current_user: User = Depends(get_current_user),
    use_case: GenerateOutfitRecommendationsUseCase = Depends(get_generate_outfit_use_case)
):
    """Generate custom outfit recommendations with specific parameters."""
    try:
        # Ensure the request is for the current user
        request.user_id = current_user.id
        
        return await use_case.execute(request)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate custom recommendations: {str(e)}"
        )
