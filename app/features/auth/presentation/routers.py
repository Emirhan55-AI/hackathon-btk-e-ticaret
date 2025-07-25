from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.responses import JSONResponse
from typing import Optional
import uuid
import logging

from app.features.auth.application.schemas import (
    UserCreate, UserLogin, UserResponse, Token, UserUpdate
)
from app.features.auth.application.use_cases import (
    RegisterUseCase, LoginUseCase, LogoutUseCase, 
    RefreshTokenUseCase, GetCurrentUserUseCase, UpdateUserUseCase
)
from app.features.auth.presentation.dependencies import (
    get_current_user, get_current_user_optional, get_user_id_from_refresh_token
)
from app.core.config import settings
from app.core.security import create_csrf_token
from app.core.di import get_container

logger = logging.getLogger("app.features.auth.presentation.routers")

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user."""
    try:
        container = get_container()
        use_case = container.register_usecase()
        
        user = await use_case.execute(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        
        return UserResponse.from_orm(user)
        
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        # Re-raise to let exception handler deal with it
        raise


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, response: Response):
    """Login user and set authentication cookies."""
    try:
        container = get_container()
        use_case = container.login_usecase()
        
        user, access_token, refresh_token = await use_case.execute(
            email=user_credentials.email,
            password=user_credentials.password
        )
        
        # Create CSRF token for double-submit cookie pattern
        csrf_token = create_csrf_token()
        
        # Set HTTP-only cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=True,
            secure=not settings.debug,  # Use secure cookies in production
            samesite="lax"
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            httponly=True,
            secure=not settings.debug,
            samesite="lax"
        )
        
        # Set CSRF token cookie (not HTTP-only, readable by JavaScript)
        response.set_cookie(
            key="csrf_token",
            value=csrf_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=False,
            secure=not settings.debug,
            samesite="lax"
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
        
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise


@router.post("/logout")
async def logout(
    response: Response,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Logout user and clear authentication cookies."""
    try:
        if current_user:
            container = get_container()
            use_case = container.logout_usecase()
            await use_case.execute(current_user.id)
        
        # Clear all authentication cookies
        response.delete_cookie(key="access_token", samesite="lax")
        response.delete_cookie(key="refresh_token", samesite="lax")
        response.delete_cookie(key="csrf_token", samesite="lax")
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        # Even if logout fails, clear cookies
        response.delete_cookie(key="access_token", samesite="lax")
        response.delete_cookie(key="refresh_token", samesite="lax")
        response.delete_cookie(key="csrf_token", samesite="lax")
        
        return {"message": "Logged out"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
    response: Response,
    user_id: uuid.UUID = Depends(get_user_id_from_refresh_token)
):
    """Refresh access token using refresh token."""
    try:
        container = get_container()
        use_case = container.refresh_token_usecase()
        
        new_access_token = await use_case.execute(user_id)
        
        # Create new CSRF token
        csrf_token = create_csrf_token()
        
        # Update access token cookie
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=True,
            secure=not settings.debug,
            samesite="lax"
        )
        
        # Update CSRF token cookie
        response.set_cookie(
            key="csrf_token",
            value=csrf_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=False,
            secure=not settings.debug,
            samesite="lax"
        )
        
        return Token(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
        
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current user information."""
    try:
        container = get_container()
        use_case = container.update_user_usecase()
        
        updated_user = await use_case.execute(
            user_id=current_user.id,
            full_name=user_update.full_name
        )
        
        return UserResponse.from_orm(updated_user)
        
    except Exception as e:
        logger.error(f"User update failed: {e}")
        raise


@router.get("/status")
async def auth_status(current_user: Optional[dict] = Depends(get_current_user_optional)):
    """Check authentication status."""
    if current_user:
        return {
            "authenticated": True,
            "user": {
                "id": str(current_user.id),
                "email": current_user.email,
                "full_name": current_user.full_name
            }
        }
    else:
        return {"authenticated": False}
