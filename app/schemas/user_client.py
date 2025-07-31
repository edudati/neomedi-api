from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.enums import UserRole, Gender


class UserClientBase(BaseModel):
    """Schema base para UserClient"""
    notes: Optional[str] = None


class UserClientCreate(BaseModel):
    """Schema para criação de UserClient"""
    name: str  # Nome do novo client (enviado pelo front)
    firebase_token: str  # Token do Firebase para criar AuthUser do client


class UserClientUpdate(BaseModel):
    """Schema para atualização de UserClient"""
    notes: Optional[str] = None


class UserClientResponse(UserClientBase):
    """Schema para resposta de UserClient"""
    user_id: UUID
    user: dict  # Dados do User associado

    class Config:
        from_attributes = True


class UserClientWithAuthResponse(UserClientResponse):
    """Schema para resposta de UserClient com dados de autenticação"""
    user: dict  # Dados completos do User com AuthUser
    address: Optional[dict] = None  # Dados do endereço (se existir)

    class Config:
        from_attributes = True


class CreateClientRequest(BaseModel):
    """Schema para request de criação de client"""
    name: str  # Nome do novo client
    firebase_token: str  # Token do Firebase para criar AuthUser do client
    company_id: UUID  # ID da company onde o client será criado


class CreateClientResponse(BaseModel):
    """Schema para resposta de criação de client"""
    success: bool
    message: str
    client_id: UUID
    client_data: Optional[dict] = None
