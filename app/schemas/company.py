from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class CompanyBase(BaseModel):
    """Schema base para Company"""
    name: str
    legal_name: str
    legal_id: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool = True
    is_visible: bool = True
    is_public: bool = False


class CompanyCreate(CompanyBase):
    """Schema para criação de Company"""
    user_id: UUID


class CompanyUpdate(BaseModel):
    """Schema para atualização de Company"""
    name: Optional[str] = None
    legal_name: Optional[str] = None
    legal_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    is_visible: Optional[bool] = None
    is_public: Optional[bool] = None


class CompanyResponse(CompanyBase):
    """Schema para resposta de Company"""
    id: UUID
    user_id: UUID
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyWithAddressResponse(CompanyResponse):
    """Schema para resposta de Company com dados do endereço"""
    address: Optional[dict] = None

    class Config:
        from_attributes = True 