import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4, UUID
from datetime import datetime
from typing import Dict, Any

from app.features.wardrobe.application.use_cases import (
    UploadClothingUseCase, GetClothingListUseCase, GetClothingItemUseCase,
    UpdateClothingItemUseCase, DeleteClothingItemUseCase, GetWardrobeStatsUseCase
)
from app.features.wardrobe.application.schemas import (
    ClothingItemCreate, ClothingItemUpdate, AITagResponse
)
from app.features.wardrobe.domain.entities import ClothingItem
from app.core.exceptions import NotFoundError, ValidationError


class TestUploadClothingUseCase:
    """Test cases for UploadClothingUseCase."""
    
    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.create = AsyncMock()
        return repository
    
    @pytest.fixture
    def mock_ai_service(self):
        ai_service = Mock()
        ai_service.analyze_clothing_image = AsyncMock()
        return ai_service
    
    @pytest.fixture
    def clothing_create_data(self):
        return ClothingItemCreate(
            name="Blue Jeans",
            category="bottoms",
            color="blue",
            brand="Levi's",
            size="M"
        )
    
    @pytest.fixture
    def mock_ai_response(self):
        return AITagResponse(
            style="casual",
            pattern="solid",
            material="denim",
            fit="straight",
            occasion=["casual", "everyday"],
            season=["all-season"],
            confidence=0.85,
            color_analysis={"primary_color": "blue"},
            attributes={"analyzed": True}
        )
    
    @pytest.mark.asyncio
    async def test_upload_clothing_success(
        self, 
        mock_repository, 
        mock_ai_service, 
        clothing_create_data,
        mock_ai_response
    ):
        """Test successful clothing upload."""
        user_id = uuid4()
        image_data = b"fake_image_data"
        filename = "jeans.jpg"
        
        # Setup mocks
        mock_ai_service.analyze_clothing_image.return_value = mock_ai_response
        
        created_item = ClothingItem(
            id=uuid4(),
            user_id=user_id,
            name=clothing_create_data.name,
            category=clothing_create_data.category,
            color=clothing_create_data.color,
            brand=clothing_create_data.brand,
            size=clothing_create_data.size,
            style=mock_ai_response.style,
            material=mock_ai_response.material,
            image_url=f"clothing_images/{user_id}/{filename}",
            ai_tags=mock_ai_response.dict(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        mock_repository.create.return_value = created_item
        
        # Execute use case
        use_case = UploadClothingUseCase(mock_repository, mock_ai_service)
        result = await use_case.execute(
            user_id=user_id,
            image_data=image_data,
            filename=filename,
            clothing_data=clothing_create_data
        )
        
        # Assertions
        assert result.upload_status == "success"
        assert result.clothing_item.name == clothing_create_data.name
        assert result.ai_analysis == mock_ai_response
        mock_ai_service.analyze_clothing_image.assert_called_once()
        mock_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_upload_clothing_ai_service_failure(
        self, 
        mock_repository, 
        mock_ai_service, 
        clothing_create_data
    ):
        """Test upload when AI service fails."""
        user_id = uuid4()
        image_data = b"fake_image_data"
        filename = "jeans.jpg"
        
        # Setup AI service to fail
        mock_ai_service.analyze_clothing_image.side_effect = Exception("AI service error")
        
        # Execute use case
        use_case = UploadClothingUseCase(mock_repository, mock_ai_service)
        
        with pytest.raises(ValidationError):
            await use_case.execute(
                user_id=user_id,
                image_data=image_data,
                filename=filename,
                clothing_data=clothing_create_data
            )


class TestGetClothingListUseCase:
    """Test cases for GetClothingListUseCase."""
    
    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.find_by_user_id = AsyncMock()
        return repository
    
    @pytest.fixture
    def sample_clothing_items(self):
        user_id = uuid4()
        return [
            ClothingItem(
                id=uuid4(),
                user_id=user_id,
                name="Blue Jeans",
                category="bottoms",
                color="blue",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            ClothingItem(
                id=uuid4(),
                user_id=user_id,
                name="White T-Shirt",
                category="tops",
                color="white",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
    
    @pytest.mark.asyncio
    async def test_get_clothing_list_success(self, mock_repository, sample_clothing_items):
        """Test successful retrieval of clothing list."""
        user_id = sample_clothing_items[0].user_id
        mock_repository.find_by_user_id.return_value = sample_clothing_items
        
        use_case = GetClothingListUseCase(mock_repository)
        result = await use_case.execute(user_id=user_id)
        
        assert len(result) == 2
        assert result[0].name == "Blue Jeans"
        assert result[1].name == "White T-Shirt"
        mock_repository.find_by_user_id.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_clothing_list_with_filters(self, mock_repository, sample_clothing_items):
        """Test retrieval with filters."""
        user_id = sample_clothing_items[0].user_id
        # Filter to only return the jeans
        filtered_items = [sample_clothing_items[0]]
        mock_repository.find_by_user_id.return_value = filtered_items
        
        use_case = GetClothingListUseCase(mock_repository)
        result = await use_case.execute(
            user_id=user_id,
            category="bottoms",
            color="blue"
        )
        
        assert len(result) == 1
        assert result[0].name == "Blue Jeans"
        mock_repository.find_by_user_id.assert_called_once_with(
            user_id=user_id,
            filters={"category": "bottoms", "color": "blue"},
            limit=100,
            offset=0
        )


class TestUpdateClothingItemUseCase:
    """Test cases for UpdateClothingItemUseCase."""
    
    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.find_by_id = AsyncMock()
        repository.update = AsyncMock()
        return repository
    
    @pytest.fixture
    def sample_clothing_item(self):
        return ClothingItem(
            id=uuid4(),
            user_id=uuid4(),
            name="Blue Jeans",
            category="bottoms",
            color="blue",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    @pytest.mark.asyncio
    async def test_update_clothing_item_success(self, mock_repository, sample_clothing_item):
        """Test successful clothing item update."""
        item_id = sample_clothing_item.id
        user_id = sample_clothing_item.user_id
        
        update_data = ClothingItemUpdate(name="Dark Blue Jeans", notes="Updated notes")
        
        # Setup mocks
        mock_repository.find_by_id.return_value = sample_clothing_item
        mock_repository.update.return_value = sample_clothing_item
        
        use_case = UpdateClothingItemUseCase(mock_repository)
        result = await use_case.execute(
            user_id=user_id,
            item_id=item_id,
            update_data=update_data
        )
        
        assert result.name == "Dark Blue Jeans"
        mock_repository.find_by_id.assert_called_once_with(item_id)
        mock_repository.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_clothing_item_not_found(self, mock_repository):
        """Test update when item doesn't exist."""
        item_id = uuid4()
        user_id = uuid4()
        update_data = ClothingItemUpdate(name="Updated Name")
        
        mock_repository.find_by_id.return_value = None
        
        use_case = UpdateClothingItemUseCase(mock_repository)
        
        with pytest.raises(NotFoundError):
            await use_case.execute(
                user_id=user_id,
                item_id=item_id,
                update_data=update_data
            )
    
    @pytest.mark.asyncio
    async def test_update_clothing_item_wrong_user(self, mock_repository, sample_clothing_item):
        """Test update when item belongs to different user."""
        item_id = sample_clothing_item.id
        wrong_user_id = uuid4()  # Different user
        
        update_data = ClothingItemUpdate(name="Updated Name")
        mock_repository.find_by_id.return_value = sample_clothing_item
        
        use_case = UpdateClothingItemUseCase(mock_repository)
        
        with pytest.raises(NotFoundError):
            await use_case.execute(
                user_id=wrong_user_id,
                item_id=item_id,
                update_data=update_data
            )


class TestGetWardrobeStatsUseCase:
    """Test cases for GetWardrobeStatsUseCase."""
    
    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        repository.find_by_user_id = AsyncMock()
        return repository
    
    @pytest.fixture
    def sample_wardrobe_items(self):
        user_id = uuid4()
        return [
            ClothingItem(
                id=uuid4(),
                user_id=user_id,
                name="Blue Jeans",
                category="bottoms",
                color="blue",
                brand="Levi's",
                purchase_price=80.00,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            ClothingItem(
                id=uuid4(),
                user_id=user_id,
                name="White T-Shirt",
                category="tops",
                color="white",
                brand="Nike",
                purchase_price=25.00,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            ClothingItem(
                id=uuid4(),
                user_id=user_id,
                name="Black Sneakers",
                category="shoes",
                color="black",
                brand="Nike",
                purchase_price=120.00,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
    
    @pytest.mark.asyncio
    async def test_get_wardrobe_stats_success(self, mock_repository, sample_wardrobe_items):
        """Test successful wardrobe stats calculation."""
        user_id = sample_wardrobe_items[0].user_id
        mock_repository.find_by_user_id.return_value = sample_wardrobe_items
        
        use_case = GetWardrobeStatsUseCase(mock_repository)
        result = await use_case.execute(user_id=user_id)
        
        assert result.total_items == 3
        assert result.total_estimated_value == 225.00
        assert result.items_by_category == {
            "bottoms": 1,
            "tops": 1,
            "shoes": 1
        }
        assert result.items_by_color == {
            "blue": 1,
            "white": 1,
            "black": 1
        }
        assert result.items_by_brand == {
            "Levi's": 1,
            "Nike": 2
        }
        assert result.most_common_brand == "Nike"
    
    @pytest.mark.asyncio
    async def test_get_wardrobe_stats_empty_wardrobe(self, mock_repository):
        """Test stats for empty wardrobe."""
        user_id = uuid4()
        mock_repository.find_by_user_id.return_value = []
        
        use_case = GetWardrobeStatsUseCase(mock_repository)
        result = await use_case.execute(user_id=user_id)
        
        assert result.total_items == 0
        assert result.total_estimated_value == 0
        assert result.items_by_category == {}
        assert result.most_common_category is None
        assert result.most_common_color is None
