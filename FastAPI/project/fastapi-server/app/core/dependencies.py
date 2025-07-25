from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.core.grpc_client import get_grpc_client, get_redis
from app.core.security import decode_token
from app.schemas.user import User
from app.services.user_service import UserService
from app.services.session_service import SessionService

security = HTTPBearer()


async def get_current_user(
    session_id: str = Header(...),
    grpc_client = Depends(get_grpc_client),
    redis = Depends(get_redis)
) -> User:
    """Dependency to get current authenticated user"""
    session_service = SessionService(grpc_client.get_stub(), redis)
    tokens = await session_service.get_session_tokens(session_id)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    
    # Use access token from session
    payload = decode_token(tokens["access_token"])
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    # Get user from database
    user_service = UserService(grpc_client.get_stub())
    user = await user_service.get_user_by_id(int(user_id))
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to get current superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough permissions"
        )
    return current_user
