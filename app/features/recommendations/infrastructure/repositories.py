"""Recommendations infrastructure repositories."""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
import logging

from app.features.recommendations.domain.repositories import RecommendationsRepository
from app.features.recommendations.domain.entities import Recommendation as RecommendationEntity
from app.features.recommendations.infrastructure.models import Recommendation as RecommendationModel

logger = logging.getLogger("app.features.recommendations.infrastructure.repositories")


class SqlAlchemyRecommendationsRepository(RecommendationsRepository):
    """SQLAlchemy implementation of RecommendationsRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_recommendations_by_user_id(
        self, 
        user_id: uuid.UUID,
        limit: Optional[int] = None
    ) -> List[RecommendationEntity]:
        """Get recommendations for a user."""
        try:
            stmt = select(RecommendationModel).where(
                RecommendationModel.user_id == user_id
            ).order_by(RecommendationModel.created_at.desc())
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await self.session.execute(stmt)
            recommendation_models = result.scalars().all()
            
            return [
                self._model_to_entity(model) 
                for model in recommendation_models
            ]
            
        except Exception as e:
            logger.error(f"Error getting recommendations for user {user_id}: {e}")
            raise
    
    async def save_recommendation(
        self, 
        recommendation: RecommendationEntity
    ) -> RecommendationEntity:
        """Save a recommendation."""
        try:
            recommendation_model = RecommendationModel(
                id=recommendation.id,
                user_id=recommendation.user_id,
                outfit_data=recommendation.outfit_data,
                recommendation_type=recommendation.recommendation_type,
                confidence_score=str(recommendation.confidence_score),
                meta_data=recommendation.metadata
            )
            
            self.session.add(recommendation_model)
            await self.session.commit()
            await self.session.refresh(recommendation_model)
            
            return self._model_to_entity(recommendation_model)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error saving recommendation: {e}")
            raise
    
    async def delete_recommendation(self, recommendation_id: uuid.UUID) -> bool:
        """Delete a recommendation."""
        try:
            stmt = select(RecommendationModel).where(
                RecommendationModel.id == recommendation_id
            )
            result = await self.session.execute(stmt)
            recommendation_model = result.scalar_one_or_none()
            
            if not recommendation_model:
                return False
            
            await self.session.delete(recommendation_model)
            await self.session.commit()
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting recommendation {recommendation_id}: {e}")
            raise
    
    async def get_recommendation_by_id(
        self, 
        recommendation_id: uuid.UUID
    ) -> Optional[RecommendationEntity]:
        """Get a recommendation by ID."""
        try:
            stmt = select(RecommendationModel).where(
                RecommendationModel.id == recommendation_id
            )
            result = await self.session.execute(stmt)
            recommendation_model = result.scalar_one_or_none()
            
            if recommendation_model:
                return self._model_to_entity(recommendation_model)
            return None
            
        except Exception as e:
            logger.error(f"Error getting recommendation {recommendation_id}: {e}")
            raise
    
    def _model_to_entity(self, model: RecommendationModel) -> RecommendationEntity:
        """Convert SQLAlchemy model to domain entity."""
        return RecommendationEntity(
            id=model.id,
            user_id=model.user_id,
            outfit_data=model.outfit_data,
            recommendation_type=model.recommendation_type,
            confidence_score=float(model.confidence_score),
            metadata=model.meta_data or {},
            created_at=model.created_at,
            updated_at=model.updated_at
        )
