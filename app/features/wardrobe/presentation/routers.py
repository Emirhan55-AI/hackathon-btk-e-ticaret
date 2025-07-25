from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import JSONResponse

from app.features.auth.presentation.dependencies import get_current_user
from app.features.auth.domain.entities import User
from app.features.wardrobe.application.schemas import (
    ClothingItemCreate, ClothingItemUpdate, ClothingItemResponse,
    ClothingItemUploadResponse, ClothingItemSearch, WardrobeStats
)
from app.features.wardrobe.application.use_cases import (
    UploadClothingUseCase, GetClothingListUseCase, GetClothingItemUseCase,
    UpdateClothingItemUseCase, DeleteClothingItemUseCase, GetWardrobeStatsUseCase
)
from app.features.wardrobe.infrastructure.repositories import SqlAlchemyClothingItemRepository
from app.features.wardrobe.infrastructure.ai_service_factory import get_ai_service
from app.core.database import get_db_session
from app.core.exceptions import NotFoundError, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/wardrobe", tags=["wardrobe"])


async def get_clothing_repository(
    db: AsyncSession = Depends(get_db_session)
) -> SqlAlchemyClothingItemRepository:
    """Dependency to get clothing repository."""
    return SqlAlchemyClothingItemRepository(db)


@router.post("/upload", response_model=ClothingItemUploadResponse)
async def upload_clothing_item(
    # File upload
    image: UploadFile = File(..., description="Clothing item image"),
    
    # Form data
    name: str = Form(..., description="Name of the clothing item"),
    category: str = Form(..., description="Category (tops, bottoms, dresses, etc.)"),
    subcategory: Optional[str] = Form(None, description="Subcategory"),
    color: Optional[str] = Form(None, description="Primary color"),
    brand: Optional[str] = Form(None, description="Brand"),
    size: Optional[str] = Form(None, description="Size"),
    material: Optional[str] = Form(None, description="Material"),
    style: Optional[str] = Form(None, description="Style"),
    pattern: Optional[str] = Form(None, description="Pattern"),
    fit: Optional[str] = Form(None, description="Fit"),
    occasion: Optional[List[str]] = Form(None, description="Occasions"),
    season: Optional[List[str]] = Form(None, description="Seasons"),
    purchase_price: Optional[float] = Form(None, description="Purchase price"),
    notes: Optional[str] = Form(None, description="Additional notes"),
    
    # Dependencies
    current_user: User = Depends(get_current_user),
    clothing_repository = Depends(get_clothing_repository),
    ai_service = Depends(get_ai_service)
):
    """Upload a new clothing item with image analysis."""
    
    # Validate file type
    if not image.content_type or not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Validate file size (max 10MB)
    if image.size and image.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 10MB"
        )
    
    try:
        # Read image data
        image_data = await image.read()
        
        # Create clothing item data
        clothing_data = ClothingItemCreate(
            name=name,
            category=category,
            subcategory=subcategory,
            color=color,
            brand=brand,
            size=size,
            material=material,
            style=style,
            pattern=pattern,
            fit=fit,
            occasion=occasion or [],
            season=season or [],
            purchase_price=purchase_price,
            notes=notes
        )
        
        # Execute upload use case
        upload_use_case = UploadClothingUseCase(clothing_repository, ai_service)
        result = await upload_use_case.execute(
            user_id=current_user.id,
            image_data=image_data,
            filename=image.filename or "uploaded_image.jpg",
            clothing_data=clothing_data
        )
        
        return result
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload clothing item"
        )


@router.get("/items", response_model=List[ClothingItemResponse])
async def get_clothing_items(
    category: Optional[str] = None,
    color: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    clothing_repository = Depends(get_clothing_repository)
):
    """Get user's clothing items with optional filters."""
    
    get_list_use_case = GetClothingListUseCase(clothing_repository)
    items = await get_list_use_case.execute(
        user_id=current_user.id,
        category=category,
        color=color,
        season=season,
        occasion=occasion,
        limit=limit,
        offset=offset
    )
    
    return items


@router.get("/items/{item_id}", response_model=ClothingItemResponse)
async def get_clothing_item(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    clothing_repository = Depends(get_clothing_repository)
):
    """Get a specific clothing item."""
    
    try:
        get_item_use_case = GetClothingItemUseCase(clothing_repository)
        item = await get_item_use_case.execute(
            user_id=current_user.id,
            item_id=item_id
        )
        return item
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothing item not found"
        )


@router.put("/items/{item_id}", response_model=ClothingItemResponse)
async def update_clothing_item(
    item_id: UUID,
    update_data: ClothingItemUpdate,
    current_user: User = Depends(get_current_user),
    clothing_repository = Depends(get_clothing_repository)
):
    """Update a clothing item."""
    
    try:
        update_use_case = UpdateClothingItemUseCase(clothing_repository)
        updated_item = await update_use_case.execute(
            user_id=current_user.id,
            item_id=item_id,
            update_data=update_data
        )
        return updated_item
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothing item not found"
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/items/{item_id}")
async def delete_clothing_item(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    clothing_repository = Depends(get_clothing_repository)
):
    """Delete a clothing item."""
    
    try:
        delete_use_case = DeleteClothingItemUseCase(clothing_repository)
        await delete_use_case.execute(
            user_id=current_user.id,
            item_id=item_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Clothing item deleted successfully"}
        )
        
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothing item not found"
        )


@router.get("/stats", response_model=WardrobeStats)
async def get_wardrobe_stats(
    current_user: User = Depends(get_current_user),
    clothing_repository = Depends(get_clothing_repository)
):
    """Get user's wardrobe statistics."""
    
    stats_use_case = GetWardrobeStatsUseCase(clothing_repository)
    stats = await stats_use_case.execute(user_id=current_user.id)
    
    return stats


@router.get("/categories")
async def get_categories():
    """Get available clothing categories."""
    categories = [
        "tops",
        "bottoms", 
        "dresses",
        "outerwear",
        "shoes",
        "accessories",
        "intimates",
        "activewear",
        "formal",
        "sleepwear"
    ]
    
    return {"categories": categories}


@router.get("/occasions")
async def get_occasions():
    """Get available occasion types."""
    occasions = [
        "casual",
        "work",
        "formal",
        "party",
        "date",
        "vacation",
        "exercise",
        "sleep",
        "special_event",
        "everyday"
    ]
    
    return {"occasions": occasions}


@router.get("/seasons")
async def get_seasons():
    """Get available seasons."""
    seasons = [
        "spring",
        "summer", 
        "fall",
        "winter",
        "all-season"
    ]
    
    return {"seasons": seasons}
