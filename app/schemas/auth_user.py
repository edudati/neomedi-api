from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class AuthUserBase(BaseModel):
    """Schema base para auth_user"""
    email: EmailStr
    display_name: str
    email_verified: bool = False
    picture: Optional[str] = None


class AuthUserCreate(AuthUserBase):
    """Schema para criar auth_user"""
    firebase_uid: str


class AuthUserUpdate(BaseModel):
    """Schema para atualizar auth_user"""
    display_name: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None


class AuthUserResponse(AuthUserBase):
    """Schema para resposta de auth_user"""
    id: int
    firebase_uid: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SignupRequest(BaseModel):
    """Schema para requisição de signup"""
    firebase_token: str


class SignupResponse(BaseModel):
    """Schema para resposta de signup"""
    success: bool
    message: str
    user: Optional[AuthUserResponse] = None
    is_new_user: bool = False
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class LoginResponse(BaseModel):
    """Schema para resposta de login"""
    success: bool
    message: str
    user: Optional[AuthUserResponse] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None 