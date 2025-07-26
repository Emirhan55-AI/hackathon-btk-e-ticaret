from typing import Optional
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer
import uuid
import logging

from app.core.security import verify_token
from app.features.auth.domain.entities import User
from app.features.auth.application.use_cases import GetCurrentUserUseCase
from app.core.di_simple import get_container

logger = logging.getLogger("app.features.auth.infrastructure.dependencies")

# HTTP Bearer security scheme (for Authorization header)
security = HTTPBearer(auto_error=False)


async def get_token_from_cookie_or_header(
    authorization: Optional[str] = Depends(security),
    access_token: Optional[str] = Cookie(None)
) -> Optional[str]:
    """Extract token from cookie or Authorization header."""
    # Priority: Cookie first, then Authorization header
    if access_token:
        return access_token
    
    if authorization and authorization.credentials:
        return authorization.credentials
    
    return None


async def get_current_user_optional(
    token: Optional[str] = Depends(get_token_from_cookie_or_header)
) -> Optional[User]:
    """Get current user if token is valid, otherwise return None."""
    if not token:
        return None
    
    try:
        # Verify token
        payload = verify_token(token, token_type="access")
        if not payload:
            return None
        
        # Extract user ID
        user_id_str = payload.get("sub")
        if not user_id_str:
            return None
        
        user_id = uuid.UUID(user_id_str)
        
        # Get user from repository
        container = get_container()
        use_case = container.get_current_user_usecase()
        user = await use_case.execute(user_id)
        
        return user
        
    except Exception as e:
        logger.warning(f"Token validation failed: {e}")
        return None


async def get_current_user(
    token: Optional[str] = Depends(get_token_from_cookie_or_header)
) -> User:
    """Get current authenticated user (required)."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Verify token
        payload = verify_token(token, token_type="access")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extract user ID
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = uuid.UUID(user_id_str)
        
        # Get user from repository
        container = get_container()
        use_case = container.get_current_user_usecase()
        user = await use_case.execute(user_id)
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_refresh_token(
    refresh_token: Optional[str] = Cookie(None)
) -> str:
    """Get refresh token from cookie."""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required"
        )
    
    # Verify refresh token
    payload = verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    return refresh_token


async def get_user_id_from_refresh_token(
    refresh_token: str = Depends(get_refresh_token)
) -> uuid.UUID:
    """Extract user ID from refresh token."""
    try:
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return uuid.UUID(user_id_str)
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token"
        )
    except Exception as e:
        logger.error(f"Refresh token validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed"
        )
