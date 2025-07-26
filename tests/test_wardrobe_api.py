import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from uuid import uuid4
import json
from io import BytesIO

from app.main import app
from app.core.database import get_db_session
from app.features.auth.infrastructure.models import UserModel
from app.features.wardrobe.infrastructure.models import ClothingItemModel
from tests.conftest import test_session


class TestWardrobeAPI:
    """Integration tests for Wardrobe API endpoints."""
    
    @pytest.fixture
    def test_user_data(self):
        return {
            "email": "wardrobe@test.com",
            "password": "TestPassword123!",
            "full_name": "Wardrobe Test User"
        }
    
    @pytest.fixture
    async def authenticated_client(self, test_user_data):
        """Create an authenticated client."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Register user
            await client.post("/api/v1/auth/register", json=test_user_data)
            
            # Login to get access token
            login_response = await client.post(
                "/api/v1/auth/login",
                data={
                    "username": test_user_data["email"],
                    "password": test_user_data["password"]
                }
            )
            
            assert login_response.status_code == 200
            
            # Extract access token from cookies
            access_token = None
            for cookie in login_response.cookies:
                if cookie.name == "access_token":
                    access_token = cookie.value
                    break
            
            assert access_token is not None
            
            # Set cookie for subsequent requests
            client.cookies.set("access_token", access_token)
            
            yield client
    
    @pytest.fixture
    def sample_clothing_data(self):
        return {
            "name": "Blue Denim Jeans",
            "category": "bottoms",
            "subcategory": "jeans",
            "color": "blue",
            "brand": "Levi's",
            "size": "32",
            "material": "denim",
            "style": "casual",
            "pattern": "solid",
            "fit": "straight",
            "occasion": ["casual", "everyday"],
            "season": ["all-season"],
            "purchase_price": 79.99,
            "notes": "Favorite pair of jeans"
        }
    
    @pytest.fixture
    def sample_image_file(self):
        """Create a sample image file for testing."""
        # Create a minimal valid JPEG file
        image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        return BytesIO(image_data)
    
    @pytest.mark.asyncio
    async def test_upload_clothing_item_success(
        self, 
        authenticated_client, 
        sample_clothing_data,
        sample_image_file
    ):
        """Test successful clothing item upload."""
        
        # Prepare multipart form data
        files = {
            "image": ("test_jeans.jpg", sample_image_file, "image/jpeg")
        }
        
        response = await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=sample_clothing_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["upload_status"] == "success"
        assert result["clothing_item"]["name"] == sample_clothing_data["name"]
        assert result["clothing_item"]["category"] == sample_clothing_data["category"]
        assert result["ai_analysis"] is not None
        assert "processing_time" in result
    
    @pytest.mark.asyncio
    async def test_upload_clothing_item_invalid_file(self, authenticated_client):
        """Test upload with invalid file type."""
        
        # Create a text file instead of image
        files = {
            "image": ("test.txt", BytesIO(b"This is not an image"), "text/plain")
        }
        
        data = {
            "name": "Test Item",
            "category": "tops"
        }
        
        response = await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=data
        )
        
        assert response.status_code == 400
        assert "File must be an image" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_get_clothing_items_empty(self, authenticated_client):
        """Test getting clothing items when wardrobe is empty."""
        
        response = await authenticated_client.get("/api/v1/wardrobe/items")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_get_clothing_items_with_data(
        self, 
        authenticated_client,
        sample_clothing_data,
        sample_image_file
    ):
        """Test getting clothing items after uploading."""
        
        # First upload an item
        files = {
            "image": ("test_jeans.jpg", sample_image_file, "image/jpeg")
        }
        
        upload_response = await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=sample_clothing_data
        )
        assert upload_response.status_code == 200
        
        # Now get the items
        response = await authenticated_client.get("/api/v1/wardrobe/items")
        
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        assert items[0]["name"] == sample_clothing_data["name"]
    
    @pytest.mark.asyncio
    async def test_get_clothing_items_with_filters(
        self, 
        authenticated_client,
        sample_clothing_data,
        sample_image_file
    ):
        """Test getting clothing items with category filter."""
        
        # Upload an item
        files = {
            "image": ("test_jeans.jpg", sample_image_file, "image/jpeg")
        }
        
        await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=sample_clothing_data
        )
        
        # Test category filter
        response = await authenticated_client.get(
            "/api/v1/wardrobe/items?category=bottoms"
        )
        
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        assert items[0]["category"] == "bottoms"
        
        # Test filter that should return no items
        response = await authenticated_client.get(
            "/api/v1/wardrobe/items?category=tops"
        )
        
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_get_single_clothing_item(
        self, 
        authenticated_client,
        sample_clothing_data,
        sample_image_file
    ):
        """Test getting a specific clothing item."""
        
        # Upload an item
        files = {
            "image": ("test_jeans.jpg", sample_image_file, "image/jpeg")
        }
        
        upload_response = await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=sample_clothing_data
        )
        
        item_id = upload_response.json()["clothing_item"]["id"]
        
        # Get the specific item
        response = await authenticated_client.get(f"/api/v1/wardrobe/items/{item_id}")
        
        assert response.status_code == 200
        item = response.json()
        assert item["id"] == item_id
        assert item["name"] == sample_clothing_data["name"]
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_clothing_item(self, authenticated_client):
        """Test getting a clothing item that doesn't exist."""
        
        fake_id = str(uuid4())
        response = await authenticated_client.get(f"/api/v1/wardrobe/items/{fake_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_update_clothing_item(
        self, 
        authenticated_client,
        sample_clothing_data,
        sample_image_file
    ):
        """Test updating a clothing item."""
        
        # Upload an item
        files = {
            "image": ("test_jeans.jpg", sample_image_file, "image/jpeg")
        }
        
        upload_response = await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=sample_clothing_data
        )
        
        item_id = upload_response.json()["clothing_item"]["id"]
        
        # Update the item
        update_data = {
            "name": "Updated Jeans Name",
            "notes": "Updated notes"
        }
        
        response = await authenticated_client.put(
            f"/api/v1/wardrobe/items/{item_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        updated_item = response.json()
        assert updated_item["name"] == "Updated Jeans Name"
        assert updated_item["notes"] == "Updated notes"
        assert updated_item["category"] == sample_clothing_data["category"]  # Unchanged
    
    @pytest.mark.asyncio
    async def test_delete_clothing_item(
        self, 
        authenticated_client,
        sample_clothing_data,
        sample_image_file
    ):
        """Test deleting a clothing item."""
        
        # Upload an item
        files = {
            "image": ("test_jeans.jpg", sample_image_file, "image/jpeg")
        }
        
        upload_response = await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=sample_clothing_data
        )
        
        item_id = upload_response.json()["clothing_item"]["id"]
        
        # Delete the item
        response = await authenticated_client.delete(f"/api/v1/wardrobe/items/{item_id}")
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify item is gone
        get_response = await authenticated_client.get(f"/api/v1/wardrobe/items/{item_id}")
        assert get_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_wardrobe_stats(
        self, 
        authenticated_client,
        sample_clothing_data,
        sample_image_file
    ):
        """Test getting wardrobe statistics."""
        
        # Start with empty wardrobe
        response = await authenticated_client.get("/api/v1/wardrobe/stats")
        
        assert response.status_code == 200
        stats = response.json()
        assert stats["total_items"] == 0
        assert stats["total_estimated_value"] == 0
        
        # Upload an item
        files = {
            "image": ("test_jeans.jpg", sample_image_file, "image/jpeg")
        }
        
        await authenticated_client.post(
            "/api/v1/wardrobe/upload",
            files=files,
            data=sample_clothing_data
        )
        
        # Check stats again
        response = await authenticated_client.get("/api/v1/wardrobe/stats")
        
        assert response.status_code == 200
        stats = response.json()
        assert stats["total_items"] == 1
        assert stats["total_estimated_value"] == sample_clothing_data["purchase_price"]
        assert stats["items_by_category"]["bottoms"] == 1
        assert stats["most_common_category"] == "bottoms"
    
    @pytest.mark.asyncio
    async def test_get_categories(self, authenticated_client):
        """Test getting available categories."""
        
        response = await authenticated_client.get("/api/v1/wardrobe/categories")
        
        assert response.status_code == 200
        categories = response.json()["categories"]
        assert "tops" in categories
        assert "bottoms" in categories
        assert "dresses" in categories
        assert len(categories) >= 5
    
    @pytest.mark.asyncio
    async def test_get_occasions(self, authenticated_client):
        """Test getting available occasions."""
        
        response = await authenticated_client.get("/api/v1/wardrobe/occasions")
        
        assert response.status_code == 200
        occasions = response.json()["occasions"]
        assert "casual" in occasions
        assert "work" in occasions
        assert "formal" in occasions
        assert len(occasions) >= 5
    
    @pytest.mark.asyncio
    async def test_get_seasons(self, authenticated_client):
        """Test getting available seasons."""
        
        response = await authenticated_client.get("/api/v1/wardrobe/seasons")
        
        assert response.status_code == 200
        seasons = response.json()["seasons"]
        assert "spring" in seasons
        assert "summer" in seasons
        assert "fall" in seasons
        assert "winter" in seasons
        assert "all-season" in seasons
    
    @pytest.mark.asyncio
    async def test_unauthorized_access(self):
        """Test that wardrobe endpoints require authentication."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test various endpoints without authentication
            endpoints = [
                "/api/v1/wardrobe/items",
                "/api/v1/wardrobe/stats",
                "/api/v1/wardrobe/categories"
            ]
            
            for endpoint in endpoints:
                response = await client.get(endpoint)
                assert response.status_code == 401
