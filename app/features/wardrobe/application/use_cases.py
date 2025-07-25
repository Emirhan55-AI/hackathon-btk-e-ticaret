from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
from datetime import datetime

from app.features.wardrobe.domain.entities import ClothingItem
from app.features.wardrobe.domain.repositories import ClothingItemRepository
from app.features.wardrobe.application.schemas import (
    ClothingItemCreate, ClothingItemUpdate, ClothingItemResponse,
    ClothingItemUploadResponse, AITagResponse, WardrobeStats
)
from app.features.wardrobe.infrastructure.ai_service import AIServiceClient
from app.core.exceptions import NotFoundError, ValidationError

logger = logging.getLogger("app.features.wardrobe.application.use_cases")


class UploadClothingUseCase:
    """Use case for uploading and analyzing clothing items."""
    
    def __init__(
        self, 
        clothing_repository: ClothingItemRepository,
        ai_service: AIServiceClient
    ):
        self.clothing_repository = clothing_repository
        self.ai_service = ai_service
    
    async def execute(
        self, 
        user_id: UUID,
        image_data: bytes,
        filename: str,
        clothing_data: ClothingItemCreate
    ) -> ClothingItemUploadResponse:
        """Upload and analyze a clothing item."""
        try:
            # Step 1: Analyze image with AI service
            logger.info(f"Analyzing clothing image for user {user_id}: {filename}")
            
            user_provided_info = {
                'category': clothing_data.category,
                'color': clothing_data.color,
                'brand': clothing_data.brand
            }
            
            ai_analysis = await self.ai_service.analyze_clothing_image(
                image_data=image_data,
                filename=filename,
                user_provided_info=user_provided_info
            )
            
            # Step 2: Merge user data with AI analysis
            enhanced_data = self._merge_user_and_ai_data(clothing_data, ai_analysis)
            
            # Step 3: Create clothing item entity
            clothing_item = ClothingItem(
                user_id=user_id,
                name=enhanced_data.name,
                category=enhanced_data.category,
                subcategory=enhanced_data.subcategory,
                color=enhanced_data.color,
                brand=enhanced_data.brand,
                size=enhanced_data.size,
                material=enhanced_data.material,
                style=enhanced_data.style,
                pattern=enhanced_data.pattern,
                fit=enhanced_data.fit,
                occasion=enhanced_data.occasion,
                season=enhanced_data.season,
                purchase_price=enhanced_data.purchase_price,
                purchase_date=enhanced_data.purchase_date,
                notes=enhanced_data.notes,
                image_url=f"clothing_images/{user_id}/{filename}",  # This would be set by file storage service
                ai_tags=ai_analysis.dict() if ai_analysis else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Step 4: Save to repository
            saved_item = await self.clothing_repository.create(clothing_item)
            
            # Step 5: Return response
            return ClothingItemUploadResponse(
                clothing_item=ClothingItemResponse.from_entity(saved_item),
                ai_analysis=ai_analysis,
                upload_status="success",
                processing_time=1.5  # This would be calculated
            )
            
        except Exception as e:
            logger.error(f"Error uploading clothing item: {e}")
            raise ValidationError(f"Failed to upload clothing item: {str(e)}")
    
    def _merge_user_and_ai_data(
        self, 
        user_data: ClothingItemCreate, 
        ai_analysis: AITagResponse
    ) -> ClothingItemCreate:
        """Merge user-provided data with AI analysis, prioritizing user input."""
        # Create a copy of user data
        merged_data = user_data.dict()
        
        # Fill in missing fields from AI analysis
        if not merged_data.get('style') and ai_analysis.style:
            merged_data['style'] = ai_analysis.style
        
        if not merged_data.get('pattern') and ai_analysis.pattern:
            merged_data['pattern'] = ai_analysis.pattern
        
        if not merged_data.get('material') and ai_analysis.material:
            merged_data['material'] = ai_analysis.material
        
        if not merged_data.get('fit') and ai_analysis.fit:
            merged_data['fit'] = ai_analysis.fit
        
        if not merged_data.get('occasion') and ai_analysis.occasion:
            merged_data['occasion'] = ai_analysis.occasion
        
        if not merged_data.get('season') and ai_analysis.season:
            merged_data['season'] = ai_analysis.season
        
        return ClothingItemCreate(**merged_data)


class GetClothingListUseCase:
    """Use case for retrieving user's clothing items."""
    
    def __init__(self, clothing_repository: ClothingItemRepository):
        self.clothing_repository = clothing_repository
    
    async def execute(
        self, 
        user_id: UUID,
        category: Optional[str] = None,
        color: Optional[str] = None,
        season: Optional[str] = None,
        occasion: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ClothingItemResponse]:
        """Get user's clothing items with optional filters."""
        
        # Build filters
        filters = {}
        if category:
            filters['category'] = category
        if color:
            filters['color'] = color
        if season:
            filters['season'] = season
        if occasion:
            filters['occasion'] = occasion
        
        # Get items from repository
        items = await self.clothing_repository.find_by_user_id(
            user_id=user_id,
            filters=filters,
            limit=limit,
            offset=offset
        )
        
        # Convert to response DTOs
        return [ClothingItemResponse.from_entity(item) for item in items]


class GetClothingItemUseCase:
    """Use case for retrieving a specific clothing item."""
    
    def __init__(self, clothing_repository: ClothingItemRepository):
        self.clothing_repository = clothing_repository
    
    async def execute(self, user_id: UUID, item_id: UUID) -> ClothingItemResponse:
        """Get a specific clothing item."""
        item = await self.clothing_repository.find_by_id(item_id)
        
        if not item:
            raise NotFoundError("Clothing item not found")
        
        if item.user_id != user_id:
            raise NotFoundError("Clothing item not found")
        
        return ClothingItemResponse.from_entity(item)


class UpdateClothingItemUseCase:
    """Use case for updating a clothing item."""
    
    def __init__(self, clothing_repository: ClothingItemRepository):
        self.clothing_repository = clothing_repository
    
    async def execute(
        self, 
        user_id: UUID, 
        item_id: UUID, 
        update_data: ClothingItemUpdate
    ) -> ClothingItemResponse:
        """Update a clothing item."""
        # Get existing item
        item = await self.clothing_repository.find_by_id(item_id)
        
        if not item:
            raise NotFoundError("Clothing item not found")
        
        if item.user_id != user_id:
            raise NotFoundError("Clothing item not found")
        
        # Update fields
        update_fields = update_data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(item, field, value)
        
        item.updated_at = datetime.utcnow()
        
        # Save changes
        updated_item = await self.clothing_repository.update(item)
        
        return ClothingItemResponse.from_entity(updated_item)


class DeleteClothingItemUseCase:
    """Use case for deleting a clothing item."""
    
    def __init__(self, clothing_repository: ClothingItemRepository):
        self.clothing_repository = clothing_repository
    
    async def execute(self, user_id: UUID, item_id: UUID) -> bool:
        """Delete a clothing item."""
        # Get existing item
        item = await self.clothing_repository.find_by_id(item_id)
        
        if not item:
            raise NotFoundError("Clothing item not found")
        
        if item.user_id != user_id:
            raise NotFoundError("Clothing item not found")
        
        # Delete item
        await self.clothing_repository.delete(item_id)
        
        return True


class GetWardrobeStatsUseCase:
    """Use case for getting wardrobe statistics."""
    
    def __init__(self, clothing_repository: ClothingItemRepository):
        self.clothing_repository = clothing_repository
    
    async def execute(self, user_id: UUID) -> WardrobeStats:
        """Get user's wardrobe statistics."""
        
        # Get all user's items
        items = await self.clothing_repository.find_by_user_id(user_id)
        
        # Calculate statistics
        total_items = len(items)
        
        # Count by category
        category_counts = {}
        color_counts = {}
        brand_counts = {}
        
        for item in items:
            # Category counts
            category_counts[item.category] = category_counts.get(item.category, 0) + 1
            
            # Color counts
            if item.color:
                color_counts[item.color] = color_counts.get(item.color, 0) + 1
            
            # Brand counts
            if item.brand:
                brand_counts[item.brand] = brand_counts.get(item.brand, 0) + 1
        
        # Calculate total value
        total_value = sum(
            item.purchase_price for item in items 
            if item.purchase_price is not None
        )
        
        return WardrobeStats(
            total_items=total_items,
            items_by_category=category_counts,
            items_by_color=color_counts,
            items_by_brand=brand_counts,
            total_estimated_value=total_value,
            most_common_category=max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None,
            most_common_color=max(color_counts.items(), key=lambda x: x[1])[0] if color_counts else None
        )
