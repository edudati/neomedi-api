from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
from uuid import UUID


class UserRole(str, Enum):
    """Enum para roles de usuário"""
    SUPER = "super"
    ADMIN = "admin"
    MANAGER = "manager"
    PROFESSIONAL = "professional"
    ASSISTANT = "assistant"
    CLIENT = "client"


class UserBase(BaseModel):
    """Schema base para User"""
    name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    role: UserRole = UserRole.CLIENT


class UserCreate(UserBase):
    """Schema para criação de User"""
    auth_user_id: int


class UserUpdate(BaseModel):
    """Schema para atualização de User"""
    name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role: Optional[UserRole] = None
    suspended_at: Optional[datetime] = None


class UserResponse(UserBase):
    """Schema para resposta de User"""
    id: UUID
    auth_user_id: int
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