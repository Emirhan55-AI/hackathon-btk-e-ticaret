from abc import ABC, abstractmethod
from typing import Optional
import uuid
from app.features.auth.domain.entities import User


class AuthRepository(ABC):
    """Abstract repository interface for authentication operations."""
    
    @abstractmethod
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        pass
    
    @abstractmethod
    async def create_user(self, user: User, hashed_password: str) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    async def update_user(self, user: User) -> User:
        """Update existing user."""
        pass
    
    @abstractmethod
    async def delete_user(self, user_id: uuid.UUID) -> bool:
        """Delete user by ID."""
        pass
    
    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        pass
    
    @abstractmethod
    async def get_user_credentials(self, email: str) -> Optional[dict]:
        """Get user credentials (including hashed password) for authentication."""
        pass
