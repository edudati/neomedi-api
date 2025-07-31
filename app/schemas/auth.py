from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class FirebaseTokenRequest(BaseModel):
    """Schema to request Firebase token"""
    firebase_token: str


class JWTTokenResponse(BaseModel):
    """Schema to response JWT token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Schema to request refresh token"""
    refresh_token: str


class UserInfo(BaseModel):
    """Schema to user information"""
    uid: str
    email: EmailStr
    email_verified: bool
    name: Optional[str] = None
    user_uid: Optional[str] = None
    picture: Optional[str] = None





class LogoutResponse(BaseModel):
    """Schema to response logout"""
    success: bool
    message: str


class TokenValidationResponse(BaseModel):
    """Schema to response token validation"""
    valid: bool
    user: Optional[UserInfo] = None
    message: Optional[str] = None 