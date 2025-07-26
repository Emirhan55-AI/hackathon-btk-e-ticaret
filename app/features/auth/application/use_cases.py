from typing import Optional, Tuple
import uuid
import logging

from app.features.auth.domain.repositories import AuthRepository
from app.features.auth.domain.entities import User
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.core.exceptions import AuthenticationError, ConflictError, NotFoundError, ValidationError

logger = logging.getLogger("app.features.auth.application.use_cases")


class RegisterUseCase:
    """Use case for user registration."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def execute(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        """Register a new user."""
        try:
            # Check if email already exists
            if await self.repository.email_exists(email):
                raise ConflictError("Email already registered")
            
            # Create user entity
            user = User.create_new(email=email, full_name=full_name)
            
            # Hash password
            hashed_password = get_password_hash(password)
            
            # Save to repository
            created_user = await self.repository.create_user(user, hashed_password)
            
            logger.info(f"User registered successfully: {created_user.email}")
            return created_user
            
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Registration failed for {email}: {e}")
            raise ValidationError("Registration failed")


class LoginUseCase:
    """Use case for user login."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def execute(self, email: str, password: str) -> Tuple[User, str, str]:
        """Authenticate user and return tokens."""
        try:
            # Get user by email
            user = await self.repository.get_user_by_email(email)
            if not user:
                raise AuthenticationError("Invalid email or password")
            
            # Check if user is active
            if not user.is_active:
                raise AuthenticationError("Account is deactivated")
            
            # For now, we'll skip email verification requirement
            # In production, you might want to check user.is_verified
            
            # Get user model to access hashed password
            # Note: This is a design consideration - we need the hashed password
            # We might need to modify the repository to return this securely
            user_with_password = await self._get_user_with_password(email)
            if not user_with_password:
                raise AuthenticationError("Invalid email or password")
            
            # Verify password
            if not verify_password(password, user_with_password["hashed_password"]):
                raise AuthenticationError("Invalid email or password")
            
            # Create tokens
            token_data = {"sub": str(user.id), "email": user.email}
            access_token = create_access_token(token_data)
            refresh_token = create_refresh_token(token_data)
            
            logger.info(f"User logged in successfully: {user.email}")
            return user, access_token, refresh_token
            
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Login failed for {email}: {e}")
            raise AuthenticationError("Login failed")
    
    async def _get_user_with_password(self, email: str) -> Optional[dict]:
        """Get user with hashed password - this would need repository method."""
        # This is a temporary solution - in a real implementation,
        # we'd add a method to the repository to get the hashed password securely
        # For now, we'll assume the repository has this capability
        try:
            # This would be implemented in the repository
            return await self.repository.get_user_credentials(email)
        except AttributeError:
            # Fallback - we need to implement this method in repository
            logger.warning("Repository doesn't implement get_user_credentials method")
            return None


class LogoutUseCase:
    """Use case for user logout."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def execute(self, user_id: uuid.UUID) -> bool:
        """Logout user (invalidate tokens)."""
        try:
            # In a real implementation, you might want to:
            # 1. Add tokens to a blacklist
            # 2. Update user's last_logout timestamp
            # 3. Invalidate all user sessions
            
            # For now, we'll just verify the user exists
            user = await self.repository.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            
            logger.info(f"User logged out successfully: {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Logout failed for user {user_id}: {e}")
            return False


class RefreshTokenUseCase:
    """Use case for refreshing access tokens."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def execute(self, user_id: uuid.UUID) -> str:
        """Generate new access token."""
        try:
            # Get user
            user = await self.repository.get_user_by_id(user_id)
            if not user:
                raise AuthenticationError("Invalid refresh token")
            
            # Check if user is still active
            if not user.is_active:
                raise AuthenticationError("Account is deactivated")
            
            # Create new access token
            token_data = {"sub": str(user.id), "email": user.email}
            access_token = create_access_token(token_data)
            
            logger.info(f"Access token refreshed for user: {user.email}")
            return access_token
            
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Token refresh failed for user {user_id}: {e}")
            raise AuthenticationError("Token refresh failed")


class GetCurrentUserUseCase:
    """Use case for getting current authenticated user."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def execute(self, user_id: uuid.UUID) -> User:
        """Get current user by ID."""
        try:
            user = await self.repository.get_user_by_id(user_id)
            if not user:
                raise AuthenticationError("User not found")
            
            if not user.is_active:
                raise AuthenticationError("Account is deactivated")
            
            return user
            
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Get current user failed for {user_id}: {e}")
            raise AuthenticationError("Failed to get current user")


class UpdateUserUseCase:
    """Use case for updating user information."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def execute(self, user_id: uuid.UUID, full_name: Optional[str] = None) -> User:
        """Update user information."""
        try:
            # Get current user
            user = await self.repository.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            
            # Update fields
            if full_name is not None:
                user.full_name = full_name
            
            # Save changes
            updated_user = await self.repository.update_user(user)
            
            logger.info(f"User updated successfully: {updated_user.email}")
            return updated_user
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"User update failed for {user_id}: {e}")
            raise ValidationError("User update failed")
