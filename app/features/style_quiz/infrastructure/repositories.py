from abc import ABC, abstractmethod
from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.features.style_quiz.domain.entities import StyleDNA
from app.features.style_quiz.infrastructure.models import StyleDNAModel


class StyleDNARepository(ABC):
    """Abstract repository interface for StyleDNA operations."""
    
    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[StyleDNA]:
        """Get StyleDNA by user ID."""
        pass
    
    @abstractmethod
    async def save(self, style_dna: StyleDNA) -> StyleDNA:
        """Save or update StyleDNA."""
        pass
    
    @abstractmethod
    async def delete_by_user_id(self, user_id: uuid.UUID) -> bool:
        """Delete StyleDNA by user ID."""
        pass


class SqlAlchemyStyleDNARepository(StyleDNARepository):
    """SQLAlchemy implementation of StyleDNA repository."""
    
    def __init__(self, session_factory):
        self._session_factory = session_factory
    
    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[StyleDNA]:
        """Get StyleDNA by user ID."""
        async with self._session_factory() as session:
            query = select(StyleDNAModel).where(StyleDNAModel.user_id == user_id)
            result = await session.execute(query)
            model = result.scalar_one_or_none()
            
            if model:
                return self._model_to_entity(model)
            return None
    
    async def save(self, style_dna: StyleDNA) -> StyleDNA:
        """Save or update StyleDNA."""
        async with self._session_factory() as session:
            # Check if StyleDNA already exists for this user
            existing_query = select(StyleDNAModel).where(StyleDNAModel.user_id == style_dna.user_id)
            result = await session.execute(existing_query)
            existing_model = result.scalar_one_or_none()
            
            if existing_model:
                # Update existing record
                existing_model.quiz_responses = style_dna.quiz_responses
                existing_model.style_profile = style_dna.style_profile
                existing_model.preferred_styles = style_dna.preferred_styles
                existing_model.preferred_colors = style_dna.preferred_colors
                existing_model.lifestyle_factors = style_dna.lifestyle_factors
                existing_model.version = style_dna.version
                existing_model.updated_at = style_dna.updated_at
                
                await session.commit()
                await session.refresh(existing_model)
                return self._model_to_entity(existing_model)
            else:
                # Create new record
                model = self._entity_to_model(style_dna)
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return self._model_to_entity(model)
    
    async def delete_by_user_id(self, user_id: uuid.UUID) -> bool:
        """Delete StyleDNA by user ID."""
        async with self._session_factory() as session:
            query = select(StyleDNAModel).where(StyleDNAModel.user_id == user_id)
            result = await session.execute(query)
            model = result.scalar_one_or_none()
            
            if model:
                await session.delete(model)
                await session.commit()
                return True
            return False
    
    def _model_to_entity(self, model: StyleDNAModel) -> StyleDNA:
        """Convert database model to domain entity."""
        return StyleDNA(
            id=model.id,
            user_id=model.user_id,
            quiz_responses=model.quiz_responses,
            style_profile=model.style_profile,
            preferred_styles=model.preferred_styles,
            preferred_colors=model.preferred_colors,
            lifestyle_factors=model.lifestyle_factors,
            version=model.version,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: StyleDNA) -> StyleDNAModel:
        """Convert domain entity to database model."""
        return StyleDNAModel(
            id=entity.id,
            user_id=entity.user_id,
            quiz_responses=entity.quiz_responses,
            style_profile=entity.style_profile,
            preferred_styles=entity.preferred_styles,
            preferred_colors=entity.preferred_colors,
            lifestyle_factors=entity.lifestyle_factors,
            version=entity.version,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
