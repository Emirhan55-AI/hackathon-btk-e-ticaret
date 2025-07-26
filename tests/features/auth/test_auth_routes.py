import pytest
from httpx import AsyncClient
from app.features.auth.application.schemas import UserCreate, UserLogin


class TestAuthRoutes:
    """Test authentication routes."""
    
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration."""
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123",
            "full_name": "Test User"
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert "created_at" in data
    
    async def test_register_duplicate_email(self, client: AsyncClient):
        """Test registration with duplicate email."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "TestPassword123"
        }
        
        # First registration
        response1 = await client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same email
        response2 = await client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 409
    
    async def test_register_invalid_password(self, client: AsyncClient):
        """Test registration with invalid password."""
        user_data = {
            "email": "test2@example.com",
            "password": "weak"  # Too weak
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
    
    async def test_login_success(self, client: AsyncClient):
        """Test successful login."""
        # First register a user
        register_data = {
            "email": "login@example.com",
            "password": "TestPassword123"
        }
        register_response = await client.post("/api/v1/auth/register", json=register_data)
        assert register_response.status_code == 201
        
        # Then login
        login_data = {
            "email": "login@example.com",
            "password": "TestPassword123"
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        
        # Check cookies are set
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies
        assert "csrf_token" in response.cookies
    
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPassword123"
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
    
    async def test_get_current_user(self, client: AsyncClient):
        """Test getting current user info."""
        # Register and login
        register_data = {
            "email": "current@example.com",
            "password": "TestPassword123",
            "full_name": "Current User"
        }
        register_response = await client.post("/api/v1/auth/register", json=register_data)
        assert register_response.status_code == 201
        
        login_data = {
            "email": "current@example.com",
            "password": "TestPassword123"
        }
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        # Get current user
        response = await client.get("/api/v1/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == register_data["email"]
        assert data["full_name"] == register_data["full_name"]
    
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """Test getting current user without authentication."""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    async def test_logout(self, client: AsyncClient):
        """Test logout."""
        # Register and login first
        register_data = {
            "email": "logout@example.com",
            "password": "TestPassword123"
        }
        register_response = await client.post("/api/v1/auth/register", json=register_data)
        assert register_response.status_code == 201
        
        login_data = {
            "email": "logout@example.com",
            "password": "TestPassword123"
        }
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        # Logout
        response = await client.post("/api/v1/auth/logout")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        
        # Check that cookies are cleared (would need to inspect actual cookie behavior)
    
    async def test_auth_status_authenticated(self, client: AsyncClient):
        """Test auth status when authenticated."""
        # Register and login
        register_data = {
            "email": "status@example.com",
            "password": "TestPassword123"
        }
        await client.post("/api/v1/auth/register", json=register_data)
        
        login_data = {
            "email": "status@example.com",
            "password": "TestPassword123"
        }
        await client.post("/api/v1/auth/login", json=login_data)
        
        # Check status
        response = await client.get("/api/v1/auth/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True
        assert "user" in data
        assert data["user"]["email"] == register_data["email"]
    
    async def test_auth_status_unauthenticated(self, client: AsyncClient):
        """Test auth status when not authenticated."""
        response = await client.get("/api/v1/auth/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is False
