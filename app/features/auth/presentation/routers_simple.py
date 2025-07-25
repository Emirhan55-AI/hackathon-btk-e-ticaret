from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Form, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.domain.entities import User
from app.features.auth.application.schemas import (
    UserCreate, UserResponse, UserUpdate, Token as TokenResponse
)
from app.features.auth.application.use_cases import (
    RegisterUseCase, LoginUseCase, LogoutUseCase, 
    RefreshTokenUseCase, GetCurrentUserUseCase, UpdateUserUseCase
)
from app.features.auth.infrastructure.repositories import SqlAlchemyUserRepository
from app.features.auth.presentation.dependencies import (
    get_current_user, get_current_user_optional, get_user_id_from_refresh_token, get_user_repository
)
from app.core.config import settings
from app.core.security import create_csrf_token
from app.core.database import get_db_session

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    user_repository: SqlAlchemyUserRepository = Depends(get_user_repository)
):
    """Register a new user."""
    try:
        use_case = RegisterUseCase(user_repository)
        user = await use_case.execute(user_data)
        return UserResponse.from_entity(user)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: SqlAlchemyUserRepository = Depends(get_user_repository)
):
    """Login user and set authentication cookies."""
    try:
        use_case = LoginUseCase(user_repository)
        token_data = await use_case.execute(form_data.username, form_data.password)
        
        # Set HTTP-only cookies
        response.set_cookie(
            key="access_token",
            value=token_data.access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=True,
            secure=not settings.debug,
            samesite="lax"
        )
        
        response.set_cookie(
            key="refresh_token", 
            value=token_data.refresh_token,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            httponly=True,
            secure=not settings.debug,
            samesite="lax"
        )
        
        # Create CSRF token
        csrf_token = create_csrf_token(token_data.user.id)
        
        return {
            "message": "Login successful",
            "user": UserResponse.from_entity(token_data.user).dict(),
            "csrf_token": csrf_token
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout")
async def logout(
    response: Response,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Logout user and clear authentication cookies."""
    
    # Always clear cookies, even if user is not authenticated
    response.delete_cookie(key="access_token", httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)
    
    if current_user:
        # Could implement token blacklisting here if needed
        message = f"User {current_user.email} logged out successfully"
    else:
        message = "Logged out successfully"
    
    return {"message": message}


@router.post("/refresh")
async def refresh_access_token(
    response: Response,
    user_id: str = Depends(get_user_id_from_refresh_token),
    user_repository: SqlAlchemyUserRepository = Depends(get_user_repository)
):
    """Refresh access token using refresh token."""
    try:
        use_case = RefreshTokenUseCase(user_repository)
        token_data = await use_case.execute(user_id)
        
        # Set new access token cookie
        response.set_cookie(
            key="access_token",
            value=token_data.access_token,
            max_age=settings.access_token_expire_minutes * 60,
            httponly=True,
            secure=not settings.debug,
            samesite="lax"
        )
        
        return {
            "message": "Token refreshed successfully",
            "user": UserResponse.from_entity(token_data.user).dict()
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse.from_entity(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_repository: SqlAlchemyUserRepository = Depends(get_user_repository)
):
    """Update current user information."""
    try:
        use_case = UpdateUserUseCase(user_repository)
        updated_user = await use_case.execute(current_user.id, user_data)
        return UserResponse.from_entity(updated_user)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/status")
async def auth_status(current_user: Optional[User] = Depends(get_current_user_optional)):
    """Check authentication status."""
    if current_user:
        return {
            "authenticated": True,
            "user": UserResponse.from_entity(current_user).dict()
        }
    else:
        return {"authenticated": False}
