from typing import Optional, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
import logging

from app.features.auth.domain.repositories import AuthRepository
from app.features.auth.domain.entities import User as UserEntity
from app.features.auth.infrastructure.models import User as UserModel

logger = logging.getLogger("app.features.auth.infrastructure.repositories")


class AuthRepositoryImpl(AuthRepository):
    """SQLAlchemy implementation of AuthRepository."""
    
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[UserEntity]:
        """Get user by ID."""
        try:
            async with self.session_factory() as session:
                stmt = select(UserModel).where(UserModel.id == user_id)
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                
                if user_model:
                    return self._model_to_entity(user_model)
                return None
                
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email address."""
        try:
            async with self.session_factory() as session:
                stmt = select(UserModel).where(UserModel.email == email.lower())
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                
                if user_model:
                    return self._model_to_entity(user_model)
                return None
                
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    async def create_user(self, user: UserEntity, hashed_password: str) -> UserEntity:
        """Create a new user."""
        try:
            async with self.session_factory() as session:
                user_model = UserModel(
                    id=user.id,
                    email=user.email,
                    hashed_password=hashed_password,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    is_verified=user.is_verified
                )
                
                session.add(user_model)
                await session.commit()
                await session.refresh(user_model)
                
                return self._model_to_entity(user_model)
                
        except Exception as e:
            logger.error(f"Error creating user {user.email}: {e}")
            raise
    
    async def update_user(self, user: UserEntity) -> UserEntity:
        """Update existing user."""
        try:
            async with self.session_factory() as session:
                stmt = select(UserModel).where(UserModel.id == user.id)
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                
                if not user_model:
                    raise ValueError(f"User with ID {user.id} not found")
                
                # Update fields
                user_model.email = user.email
                user_model.full_name = user.full_name
                user_model.is_active = user.is_active
                user_model.is_verified = user.is_verified
                
                await session.commit()
                await session.refresh(user_model)
                
                return self._model_to_entity(user_model)
                
        except Exception as e:
            logger.error(f"Error updating user {user.id}: {e}")
            raise
    
    async def delete_user(self, user_id: uuid.UUID) -> bool:
        """Delete user by ID."""
        try:
            async with self.session_factory() as session:
                stmt = select(UserModel).where(UserModel.id == user_id)
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                
                if user_model:
                    await session.delete(user_model)
                    await session.commit()
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise
    
    async def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        try:
            async with self.session_factory() as session:
                stmt = select(UserModel.id).where(UserModel.email == email.lower())
                result = await session.execute(stmt)
                return result.scalar_one_or_none() is not None
                
        except Exception as e:
            logger.error(f"Error checking email existence {email}: {e}")
            raise
    
    async def get_user_credentials(self, email: str) -> Optional[dict]:
        """Get user credentials (including hashed password) for authentication."""
        try:
            async with self.session_factory() as session:
                stmt = select(UserModel).where(UserModel.email == email.lower())
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                
                if user_model:
                    return {
                        "user_id": user_model.id,
                        "email": user_model.email,
                        "hashed_password": user_model.hashed_password,
                        "is_active": user_model.is_active,
                        "is_verified": user_model.is_verified
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting user credentials for {email}: {e}")
            raise
    
    def _model_to_entity(self, model: UserModel) -> UserEntity:
        """Convert SQLAlchemy model to domain entity."""
        return UserEntity(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


class SqlAlchemyUserRepository(AuthRepository):
    """SQLAlchemy User Repository with direct session access."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[UserEntity]:
        """Get user by ID."""
        try:
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if user_model:
                return self._model_to_entity(user_model)
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email."""
        try:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if user_model:
                return self._model_to_entity(user_model)
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    async def create_user(self, user: UserEntity, password_hash: str) -> UserEntity:
        """Create a new user."""
        try:
            user_model = UserModel(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                password_hash=password_hash,
                is_active=user.is_active,
                is_verified=user.is_verified
            )
            
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
            
            return self._model_to_entity(user_model)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating user {user.email}: {e}")
            raise
    
    async def update_user(self, user_id: uuid.UUID, **kwargs) -> Optional[UserEntity]:
        """Update user information."""
        try:
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if not user_model:
                return None
            
            for key, value in kwargs.items():
                if hasattr(user_model, key):
                    setattr(user_model, key, value)
            
            await self.session.commit()
            await self.session.refresh(user_model)
            
            return self._model_to_entity(user_model)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            raise
    
    async def get_user_credentials(self, email: str) -> Optional[tuple[UserEntity, str]]:
        """Get user credentials (user entity and password hash)."""
        try:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if user_model:
                user_entity = self._model_to_entity(user_model)
                return user_entity, user_model.password_hash
            return None
            
        except Exception as e:
            logger.error(f"Error getting user credentials for {email}: {e}")
            raise
    
    def _model_to_entity(self, model: UserModel) -> UserEntity:
        """Convert SQLAlchemy model to domain entity."""
        return UserEntity(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
