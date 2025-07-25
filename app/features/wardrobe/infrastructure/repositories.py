from typing import Optional, List, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
import uuid
import logging

from app.features.wardrobe.domain.repositories import WardrobeRepository
from app.features.wardrobe.domain.entities import ClothingItem as ClothingItemEntity
from app.features.wardrobe.infrastructure.models import ClothingItem as ClothingItemModel

logger = logging.getLogger("app.features.wardrobe.infrastructure.repositories")


class WardrobeRepositoryImpl(WardrobeRepository):
    """SQLAlchemy implementation of WardrobeRepository."""
    
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory
    
    async def get_clothing_item_by_id(self, item_id: uuid.UUID) -> Optional[ClothingItemEntity]:
        """Get clothing item by ID."""
        try:
            async with self.session_factory() as session:
                stmt = select(ClothingItemModel).where(ClothingItemModel.id == item_id)
                result = await session.execute(stmt)
                item_model = result.scalar_one_or_none()
                
                if item_model:
                    return self._model_to_entity(item_model)
                return None
                
        except Exception as e:
            logger.error(f"Error getting clothing item by ID {item_id}: {e}")
            raise
    
    async def get_user_clothing_items(
        self, 
        user_id: uuid.UUID,
        category: Optional[str] = None,
        color: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[ClothingItemEntity]:
        """Get user's clothing items with optional filters."""
        try:
            async with self.session_factory() as session:
                stmt = select(ClothingItemModel).where(ClothingItemModel.user_id == user_id)
                
                # Apply filters
                if category:
                    stmt = stmt.where(ClothingItemModel.category == category.lower())
                
                if color:
                    stmt = stmt.where(ClothingItemModel.color == color.lower())
                
                if is_favorite is not None:
                    stmt = stmt.where(ClothingItemModel.is_favorite == is_favorite)
                
                # Order by creation date (newest first)
                stmt = stmt.order_by(ClothingItemModel.created_at.desc())
                
                # Apply pagination
                if offset:
                    stmt = stmt.offset(offset)
                
                if limit:
                    stmt = stmt.limit(limit)
                
                result = await session.execute(stmt)
                item_models = result.scalars().all()
                
                return [self._model_to_entity(model) for model in item_models]
                
        except Exception as e:
            logger.error(f"Error getting user clothing items for user {user_id}: {e}")
            raise
    
    async def create_clothing_item(self, item: ClothingItemEntity) -> ClothingItemEntity:
        """Create a new clothing item."""
        try:
            async with self.session_factory() as session:
                item_model = ClothingItemModel(
                    id=item.id,
                    user_id=item.user_id,
                    name=item.name,
                    category=item.category,
                    brand=item.brand,
                    color=item.color,
                    size=item.size,
                    image_url=item.image_url,
                    ai_tags=item.ai_tags,
                    user_tags=item.user_tags,
                    description=item.description,
                    is_favorite=item.is_favorite
                )
                
                session.add(item_model)
                await session.commit()
                await session.refresh(item_model)
                
                return self._model_to_entity(item_model)
                
        except Exception as e:
            logger.error(f"Error creating clothing item {item.name}: {e}")
            raise
    
    async def update_clothing_item(self, item: ClothingItemEntity) -> ClothingItemEntity:
        """Update existing clothing item."""
        try:
            async with self.session_factory() as session:
                stmt = select(ClothingItemModel).where(ClothingItemModel.id == item.id)
                result = await session.execute(stmt)
                item_model = result.scalar_one_or_none()
                
                if not item_model:
                    raise ValueError(f"Clothing item with ID {item.id} not found")
                
                # Update fields
                item_model.name = item.name
                item_model.category = item.category
                item_model.brand = item.brand
                item_model.color = item.color
                item_model.size = item.size
                item_model.image_url = item.image_url
                item_model.ai_tags = item.ai_tags
                item_model.user_tags = item.user_tags
                item_model.description = item.description
                item_model.is_favorite = item.is_favorite
                
                await session.commit()
                await session.refresh(item_model)
                
                return self._model_to_entity(item_model)
                
        except Exception as e:
            logger.error(f"Error updating clothing item {item.id}: {e}")
            raise
    
    async def delete_clothing_item(self, item_id: uuid.UUID) -> bool:
        """Delete clothing item by ID."""
        try:
            async with self.session_factory() as session:
                stmt = select(ClothingItemModel).where(ClothingItemModel.id == item_id)
                result = await session.execute(stmt)
                item_model = result.scalar_one_or_none()
                
                if item_model:
                    await session.delete(item_model)
                    await session.commit()
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error deleting clothing item {item_id}: {e}")
            raise
    
    async def get_user_clothing_count(self, user_id: uuid.UUID) -> int:
        """Get total count of user's clothing items."""
        try:
            async with self.session_factory() as session:
                stmt = select(func.count(ClothingItemModel.id)).where(
                    ClothingItemModel.user_id == user_id
                )
                result = await session.execute(stmt)
                return result.scalar() or 0
                
        except Exception as e:
            logger.error(f"Error getting clothing count for user {user_id}: {e}")
            raise
    
    async def search_clothing_items(
        self,
        user_id: uuid.UUID,
        search_term: str,
        limit: Optional[int] = None
    ) -> List[ClothingItemEntity]:
        """Search clothing items by name, brand, or tags."""
        try:
            async with self.session_factory() as session:
                search_pattern = f"%{search_term.lower()}%"
                
                stmt = select(ClothingItemModel).where(
                    ClothingItemModel.user_id == user_id
                ).where(
                    or_(
                        ClothingItemModel.name.ilike(search_pattern),
                        ClothingItemModel.brand.ilike(search_pattern),
                        ClothingItemModel.description.ilike(search_pattern),
                        ClothingItemModel.category.ilike(search_pattern),
                        ClothingItemModel.color.ilike(search_pattern)
                    )
                ).order_by(ClothingItemModel.created_at.desc())
                
                if limit:
                    stmt = stmt.limit(limit)
                
                result = await session.execute(stmt)
                item_models = result.scalars().all()
                
                return [self._model_to_entity(model) for model in item_models]
                
        except Exception as e:
            logger.error(f"Error searching clothing items for user {user_id}: {e}")
            raise
    
    def _model_to_entity(self, model: ClothingItemModel) -> ClothingItemEntity:
        """Convert SQLAlchemy model to domain entity."""
        return ClothingItemEntity(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            category=model.category,
            brand=model.brand,
            color=model.color,
            size=model.size,
            image_url=model.image_url,
            ai_tags=model.ai_tags or {},
            user_tags=model.user_tags or {},
            description=model.description,
            is_favorite=model.is_favorite,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
