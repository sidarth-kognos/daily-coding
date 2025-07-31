import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.base_client import OAuthError
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas.user import User


class AuthService:
    def __init__(self, grpc_stub):
        self.grpc_stub = grpc_stub
        if grpc_stub:
            self.user_service = UserService(grpc_stub)
        
        self.oauth = OAuth()
        self.oauth.register(
            name='oauth2',
            client_id=settings.OAUTH2_CLIENT_ID,
            client_secret=settings.OAUTH2_CLIENT_SECRET,
            server_metadata_url=f"{settings.OAUTH2_PROVIDER_URL}/.well-known/openid-configuration",
            client_kwargs={
                'scope': settings.OAUTH2_SCOPE
            }
        )

    async def get_oauth_authorization_url(self, state: str = None) -> str:
        """Generate OAuth authorization URL"""
        try:
            return await self.oauth.oauth2.authorize_redirect(
                redirect_uri=settings.OAUTH2_REDIRECT_URI,
                state=state
            )
        except OAuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def authenticate_oauth_user(self, code: str) -> User:
        """Authenticate user via OAuth flow"""
        try:
            token = await self.oauth.oauth2.authorize_access_token(code)
            user_info = await self.oauth.oauth2.parse_id_token(token)
            
            email = user_info.get('email')
            oauth_id = user_info.get('sub')
            full_name = user_info.get('name')
            username = user_info.get('preferred_username') or email.split('@')[0]

            if not email or not oauth_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient user information from OAuth provider"
                )

            existing_user = await self.user_service.get_user_by_email(email)
            if existing_user:
                if not existing_user.oauth_id:
                    existing_user.oauth_provider = "oauth2"
                    existing_user.oauth_id = oauth_id
                return existing_user
            else:
                return await self.user_service.create_oauth_user(
                    email=email,
                    username=username,
                    full_name=full_name,
                    oauth_provider="oauth2",
                    oauth_id=oauth_id
                )

        except OAuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
