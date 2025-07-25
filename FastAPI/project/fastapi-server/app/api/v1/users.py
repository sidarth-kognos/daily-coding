from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from app.core.grpc_client import get_grpc_client
from app.core.dependencies import get_current_user, get_current_superuser
from app.schemas.user import UserResponse, UserUpdate, User
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    grpc_client = Depends(get_grpc_client)
):
    """Update current user information"""
    user_service = UserService(grpc_client.get_stub())
    
    # Check if email/username already exists for other users
    if user_update.email and user_update.email != current_user.email:
        existing_user = await user_service.get_user_by_email(user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    if user_update.username and user_update.username != current_user.username:
        existing_user = await user_service.get_user_by_username(user_update.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    updated_user = await user_service.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(updated_user)


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_superuser),
    grpc_client = Depends(get_grpc_client)
):
    """List all users (superuser only)"""
    user_service = UserService(grpc_client.get_stub())
    users = await user_service.get_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    grpc_client = Depends(get_grpc_client)
):
    """Get user by ID (superuser only)"""
    user_service = UserService(grpc_client.get_stub())
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_superuser),
    grpc_client = Depends(get_grpc_client)
):
    """Update user by ID (superuser only)"""
    user_service = UserService(grpc_client.get_stub())
    
    # Check if email/username already exists for other users
    if user_update.email:
        existing_user = await user_service.get_user_by_email(user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    if user_update.username:
        existing_user = await user_service.get_user_by_username(user_update.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    updated_user = await user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    grpc_client = Depends(get_grpc_client)
):
    """Delete user by ID (superuser only)"""
    user_service = UserService(grpc_client.get_stub())
    
    if not await user_service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}
