from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    session_id: str
    expires_in: int


class TokenData(BaseModel):
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class OAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None
