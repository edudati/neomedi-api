from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.enums import UserRole, Gender


class UserBase(BaseModel):
    """Schema base para User"""
    name: str
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[Gender] = None
    is_active: bool = True
    is_verified: bool = False
    has_access: bool = False
    role: UserRole = UserRole.CLIENT
    social_media: Optional[dict] = None


class UserCreate(UserBase):
    """Schema para criação de User"""
    auth_user_id: int
    # email e profile_picture_url não são recebidos aqui, vêm do AuthUser


class UserUpdate(BaseModel):
    """Schema para atualização de User"""
    name: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[Gender] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    has_access: Optional[bool] = None
    role: Optional[UserRole] = None
    social_media: Optional[dict] = None
    suspended_at: Optional[datetime] = None
    # email e profile_picture_url não são recebidos aqui, vêm do AuthUser


class UserResponse(UserBase):
    """Schema para resposta de User"""
    id: UUID
    auth_user_id: int
    email: EmailStr
    picture: Optional[str] = None
    is_deleted: bool
    suspended_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserWithAuthResponse(UserResponse):
    """Schema para resposta de User com dados de autenticação"""
    auth_user: dict  # Dados básicos do AuthUser
    address: Optional[dict] = None  # Dados do endereço (se existir)

    class Config:
        from_attributes = True


class UserBasicResponse(UserResponse):
    """Schema para resposta de User com dados básicos (sem endereço)"""
    auth_user: dict  # Dados básicos do AuthUser

    class Config:
        from_attributes = True 