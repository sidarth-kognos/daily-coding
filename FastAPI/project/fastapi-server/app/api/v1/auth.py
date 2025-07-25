from fastapi import APIRouter, Depends, HTTPException, status, Request
from datetime import timedelta
from typing import Any
import json

from app.core.grpc_client import get_grpc_client, get_redis
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest, OAuthCallback
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
    user_create: UserCreate,
    grpc_client = Depends(get_grpc_client)
):
    """Register a new user"""
    user_service = UserService(grpc_client.get_stub())
    
    # Check if user already exists
    existing_email = await user_service.get_user_by_email(user_create.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    existing_username = await user_service.get_user_by_username(user_create.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = await user_service.create_user(user_create)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    login_data: LoginRequest,
    grpc_client = Depends(get_grpc_client),
    redis = Depends(get_redis)
):
    """Login user and create session"""
    user_service = UserService(grpc_client.get_stub())
    session_service = SessionService(grpc_client.get_stub(), redis)
    
    # Authenticate user
    user = await user_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Create session
    await session_service.create_session(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    grpc_client = Depends(get_grpc_client),
    redis = Depends(get_redis)
):
    """Refresh access token"""
    try:
        payload = decode_token(refresh_data.refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )
        
        # Update session with new access token
        session_service = SessionService(grpc_client.get_stub(), redis)
        await session_service.create_session(
            user_id=int(user_id),
            access_token=access_token,
            refresh_token=refresh_data.refresh_token
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_data.refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
async def logout(
    request: Request,
    current_user = Depends(get_current_user),
    grpc_client = Depends(get_grpc_client),
    redis = Depends(get_redis)
):
    """Logout user and invalidate session"""
    # Get token from request
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = auth_header.split(" ")[1]
    
    # Invalidate session
    session_service = SessionService(grpc_client.get_stub(), redis)
    await session_service.invalidate_session(current_user.id, token)
    
    return {"message": "Successfully logged out"}


@router.post("/logout-all")
async def logout_all(
    current_user = Depends(get_current_user),
    grpc_client = Depends(get_grpc_client),
    redis = Depends(get_redis)
):
    """Logout from all sessions"""
    session_service = SessionService(grpc_client.get_stub(), redis)
    await session_service.invalidate_all_user_sessions(current_user.id)
    
    return {"message": "Successfully logged out from all sessions"}


@router.get("/oauth/login")
async def oauth_login():
    """Redirect to OAuth provider"""
    auth_service = AuthService(None)  # No gRPC needed for URL generation
    auth_url = await auth_service.get_oauth_authorization_url()
    return {"authorization_url": auth_url}


@router.post("/oauth/callback", response_model=Token)
async def oauth_callback(
    request: Request,
    oauth_data: OAuthCallback,
    grpc_client = Depends(get_grpc_client),
    redis = Depends(get_redis)
):
    """Handle OAuth callback"""
    auth_service = AuthService(grpc_client.get_stub())
    session_service = SessionService(grpc_client.get_stub(), redis)
    
    try:
        # Authenticate user via OAuth
        user = await auth_service.authenticate_oauth_user(oauth_data.code)
        
        # Create tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Create session and store tokens
        session = await session_service.create_session(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None
        )
        
        # Store additional session data in Redis
        session_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id
        }
        await redis.setex(
            f"session_data:{session.id}",
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            json.dumps(session_data)
        )
        
        return {
            "session_id": str(session.id),
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )
