from pydantic import BaseSettings, validator
from typing import Optional, Dict, Any
import secrets
import json


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Server"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # gRPC Database Service
    GRPC_DATABASE_HOST: str = "localhost"
    GRPC_DATABASE_PORT: int = 50051
    GRPC_DATABASE_URL: str = None
    
    @validator("GRPC_DATABASE_URL", pre=True, always=True)
    def assemble_grpc_url(cls, v, values):
        if v:
            return v
        return f"{values.get('GRPC_DATABASE_HOST')}:{values.get('GRPC_DATABASE_PORT')}"
    
    # Redis for session management
    REDIS_URL: str = "redis://localhost:6379"
    
    # OAuth2 / IdP Settings
    OAUTH2_PROVIDER_URL: str = "https://your-idp.com"
    OAUTH2_CLIENT_ID: str = ""
    OAUTH2_CLIENT_SECRET: str = ""
    OAUTH2_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    
    # OAuth2 Endpoints
    OAUTH2_AUTHORIZATION_ENDPOINT: str = "/oauth/authorize"
    OAUTH2_TOKEN_ENDPOINT: str = "/oauth/token"
    OAUTH2_USERINFO_ENDPOINT: str = "/userinfo"
    OAUTH2_SCOPE: str = "openid email profile"
    
    # OAuth2 User Info Field Mapping
    OAUTH2_USERINFO_FIELD_MAP: Dict[str, Any] = {
        "email": "email",
        "oauth_id": ["sub", "id"],
        "full_name": "name",
        "username": ["preferred_username", "email"]
    }

    @validator("OAUTH2_USERINFO_FIELD_MAP", pre=True)
    def parse_field_map(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
