from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class FirebaseTokenRequest(BaseModel):
    """Schema para requisição de token Firebase"""
    firebase_token: str


class JWTTokenResponse(BaseModel):
    """Schema para resposta de token JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]


class RefreshTokenRequest(BaseModel):
    """Schema para requisição de refresh token"""
    refresh_token: str


class UserInfo(BaseModel):
    """Schema para informações do usuário"""
    uid: str
    email: EmailStr
    email_verified: bool
    name: Optional[str] = None
    picture: Optional[str] = None


class LoginResponse(BaseModel):
    """Schema para resposta de login"""
    success: bool
    message: str
    data: Optional[JWTTokenResponse] = None


class LogoutResponse(BaseModel):
    """Schema para resposta de logout"""
    success: bool
    message: str


class TokenValidationResponse(BaseModel):
    """Schema para resposta de validação de token"""
    valid: bool
    user: Optional[UserInfo] = None
    message: Optional[str] = None 