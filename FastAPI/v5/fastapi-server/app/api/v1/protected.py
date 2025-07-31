from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.core.grpc_client import get_grpc_client, get_redis
from app.core.dependencies import get_current_user, get_current_superuser
from app.schemas.user import User
from app.services.session_service import SessionService

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    grpc_client = Depends(get_grpc_client)
):
    """Protected dashboard endpoint"""
    return {
        "message": f"Welcome to your dashboard, {current_user.full_name or current_user.username}!",
        "user_id": current_user.id,
        "email": current_user.email,
        "last_login": current_user.last_login
    }


@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """Get user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "oauth_provider": current_user.oauth_provider
    }


@router.get("/sessions")
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    grpc_client = Depends(get_grpc_client),
    redis = Depends(get_redis)
):
    """Get all active sessions for current user"""
    session_service = SessionService(grpc_client.get_stub(), redis)
    sessions = await session_service.get_user_sessions(current_user.id, active_only=True)
    
    return {
        "active_sessions": len(sessions),
        "sessions": [
            {
                "id": session.id,
                "created_at": session.created_at,
                "expires_at": session.expires_at,
                "user_agent": session.user_agent,
                "ip_address": session.ip_address
            }
            for session in sessions
        ]
    }


@router.get("/admin/stats")
async def get_admin_stats(
    current_user: User = Depends(get_current_superuser),
    grpc_client = Depends(get_grpc_client)
):
    """Admin only - Get system statistics"""
    # This would need to be implemented with specific gRPC calls
    # to get statistics from the database service
    return {
        "message": "Admin statistics endpoint",
        "note": "Implementation depends on specific gRPC calls for statistics"
    }
