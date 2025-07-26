from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import Provide, inject
import logging

from app.features.style_quiz.application.schemas import (
    QuizResponseSchema, 
    StyleDNAResponse, 
    QuizSubmissionResponse,
    StyleDNAUpdateSchema
)
from app.features.style_quiz.infrastructure.repositories import SqlAlchemyStyleDNARepository
from app.features.style_quiz.application.use_cases import (
    SubmitQuizUseCase,
    GetStyleDNAUseCase,
    UpdateStyleDNAUseCase,
    DeleteStyleDNAUseCase
)
from app.features.auth.presentation.dependencies import get_current_user
from app.features.auth.domain.entities import User
from app.core.di import Container
from app.core.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = APIRouter()


# Dependency functions
async def get_style_dna_repository(
    db: AsyncSession = Depends(get_db_session)
) -> SqlAlchemyStyleDNARepository:
    """Get StyleDNA repository instance."""
    return SqlAlchemyStyleDNARepository(db)


async def get_submit_quiz_usecase(
    repository: SqlAlchemyStyleDNARepository = Depends(get_style_dna_repository)
) -> SubmitQuizUseCase:
    """Get submit quiz use case."""
    return SubmitQuizUseCase(repository)


async def get_style_dna_usecase(
    repository: SqlAlchemyStyleDNARepository = Depends(get_style_dna_repository)
) -> GetStyleDNAUseCase:
    """Get style DNA use case."""
    return GetStyleDNAUseCase(repository)


async def get_update_style_dna_usecase(
    repository: SqlAlchemyStyleDNARepository = Depends(get_style_dna_repository)
) -> UpdateStyleDNAUseCase:
    """Get update style DNA use case."""
    return UpdateStyleDNAUseCase(repository)


async def get_delete_style_dna_usecase(
    repository: SqlAlchemyStyleDNARepository = Depends(get_style_dna_repository)
) -> DeleteStyleDNAUseCase:
    """Get delete style DNA use case."""
    return DeleteStyleDNAUseCase(repository)


@router.post("/submit", response_model=QuizSubmissionResponse)
@inject
async def submit_quiz(
    quiz_data: QuizResponseSchema,
    current_user: User = Depends(get_current_user),
    submit_quiz_usecase: SubmitQuizUseCase = Depends(Provide[Container.submit_quiz_usecase])
):
    """Submit quiz responses and create/update style DNA profile."""
    try:
        logger.info(f"Processing quiz submission for user {current_user.id}")
        
        # Execute the use case
        style_dna = await submit_quiz_usecase.execute(
            user_id=current_user.id,
            quiz_responses=quiz_data.quiz_responses
        )
        
        # Convert to response schema
        style_dna_response = StyleDNAResponse(
            id=style_dna.id,
            user_id=style_dna.user_id,
            quiz_responses=style_dna.quiz_responses,
            style_profile=style_dna.style_profile,
            preferred_styles=style_dna.preferred_styles,
            preferred_colors=style_dna.preferred_colors,
            lifestyle_factors=style_dna.lifestyle_factors,
            version=style_dna.version,
            created_at=style_dna.created_at,
            updated_at=style_dna.updated_at
        )
        
        return QuizSubmissionResponse(
            success=True,
            message="Style quiz processed successfully",
            style_dna=style_dna_response
        )
        
    except Exception as e:
        logger.error(f"Error processing quiz submission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process quiz: {str(e)}"
        )


@router.get("/profile", response_model=StyleDNAResponse)
@inject
async def get_style_profile(
    current_user: User = Depends(get_current_user),
    get_style_dna_usecase: GetStyleDNAUseCase = Depends(Provide[Container.get_style_dna_usecase])
):
    """Get user's current style DNA profile."""
    try:
        logger.info(f"Retrieving style profile for user {current_user.id}")
        
        style_dna = await get_style_dna_usecase.execute(current_user.id)
        
        if not style_dna:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Style profile not found. Please complete the style quiz first."
            )
        
        return StyleDNAResponse(
            id=style_dna.id,
            user_id=style_dna.user_id,
            quiz_responses=style_dna.quiz_responses,
            style_profile=style_dna.style_profile,
            preferred_styles=style_dna.preferred_styles,
            preferred_colors=style_dna.preferred_colors,
            lifestyle_factors=style_dna.lifestyle_factors,
            version=style_dna.version,
            created_at=style_dna.created_at,
            updated_at=style_dna.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving style profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve style profile: {str(e)}"
        )


@router.patch("/profile", response_model=StyleDNAResponse)
@inject
async def update_style_profile(
    update_data: StyleDNAUpdateSchema,
    current_user: User = Depends(get_current_user),
    update_style_dna_usecase: UpdateStyleDNAUseCase = Depends(Provide[Container.update_style_dna_usecase])
):
    """Update user's style DNA profile."""
    try:
        logger.info(f"Updating style profile for user {current_user.id}")
        
        # Convert update schema to dict, excluding None values
        updates = update_data.dict(exclude_none=True)
        
        if not updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid updates provided"
            )
        
        style_dna = await update_style_dna_usecase.execute(current_user.id, updates)
        
        if not style_dna:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Style profile not found. Please complete the style quiz first."
            )
        
        return StyleDNAResponse(
            id=style_dna.id,
            user_id=style_dna.user_id,
            quiz_responses=style_dna.quiz_responses,
            style_profile=style_dna.style_profile,
            preferred_styles=style_dna.preferred_styles,
            preferred_colors=style_dna.preferred_colors,
            lifestyle_factors=style_dna.lifestyle_factors,
            version=style_dna.version,
            created_at=style_dna.created_at,
            updated_at=style_dna.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating style profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update style profile: {str(e)}"
        )


@router.delete("/profile")
@inject
async def delete_style_profile(
    current_user: User = Depends(get_current_user),
    delete_style_dna_usecase: DeleteStyleDNAUseCase = Depends(Provide[Container.delete_style_dna_usecase])
):
    """Delete user's style DNA profile."""
    try:
        logger.info(f"Deleting style profile for user {current_user.id}")
        
        success = await delete_style_dna_usecase.execute(current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Style profile not found"
            )
        
        return {"message": "Style profile deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting style profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete style profile: {str(e)}"
        )
