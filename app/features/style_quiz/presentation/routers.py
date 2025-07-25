from fastapi import APIRouter, HTTPException, Depends, status
from app.features.style_quiz.domain.models import QuizResponse
from app.features.recommendations.application.use_cases import AnalyzeStyleDNAUseCase
from app.features.recommendations.application.schemas import StyleDNAProfile
from app.features.recommendations.infrastructure.ai_service_client import AIServiceClient
from app.features.auth.presentation.dependencies import get_current_user
from app.features.auth.domain.entities import User

router = APIRouter()

# Dependency injection
def get_ai_service() -> AIServiceClient:
    return AIServiceClient()

def get_analyze_style_use_case(
    ai_service: AIServiceClient = Depends(get_ai_service)
) -> AnalyzeStyleDNAUseCase:
    return AnalyzeStyleDNAUseCase(ai_service)

@router.post("/submit", response_model=StyleDNAProfile)
async def submit_quiz(
    quiz_response: QuizResponse,
    current_user: User = Depends(get_current_user),
    use_case: AnalyzeStyleDNAUseCase = Depends(get_analyze_style_use_case)
):
    """Submit quiz responses and analyze style DNA."""
    if not quiz_response.answers:
        raise HTTPException(status_code=400, detail="No answers provided")

    try:
        # Analyze style preferences from quiz answers
        style_profile = await use_case.execute(current_user.id, quiz_response.answers)
        
        return style_profile
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process quiz: {str(e)}"
        )
