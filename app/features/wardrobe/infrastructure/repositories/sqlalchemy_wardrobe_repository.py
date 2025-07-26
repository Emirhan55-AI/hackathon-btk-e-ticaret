from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.features.wardrobe.domain.entities import ClothingItem
from app.features.wardrobe.domain.repositories.wardrobe_repository import WardrobeRepository

class SqlAlchemyWardrobeRepository(WardrobeRepository):
    """SQLAlchemy implementation of the WardrobeRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_clothing_item(self, item: ClothingItem) -> ClothingItem:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_clothing_item(self, item_id: str) -> Optional[ClothingItem]:
        result = await self.session.execute(select(ClothingItem).where(ClothingItem.id == item_id))
        return result.scalar_one_or_none()

    async def list_clothing_items(self, user_id: str) -> List[ClothingItem]:
        result = await self.session.execute(select(ClothingItem).where(ClothingItem.user_id == user_id))
        return result.scalars().all()

    async def update_clothing_item(self, item: ClothingItem) -> ClothingItem:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_clothing_item(self, item_id: str) -> None:
        result = await self.session.execute(select(ClothingItem).where(ClothingItem.id == item_id))
        item = result.scalar_one_or_none()
        if item:
            await self.session.delete(item)
            await self.session.commit()
