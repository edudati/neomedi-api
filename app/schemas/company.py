from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from .address import AddressCreateForCompany


class CompanyBase(BaseModel):
    """Schema base para Company"""
    name: str
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    social_media: Optional[dict] = None
    is_virtual: bool = False
    is_active: bool = True


class CompanyCreate(CompanyBase):
    """Schema para criação de Company"""
    user_id: UUID


class CompanyCreateWithAddress(CompanyBase):
    """Schema para criação de Company com endereço opcional"""
    address: Optional[AddressCreateForCompany] = None


class CompanyUpdate(BaseModel):
    """Schema para atualização de Company"""
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    social_media: Optional[dict] = None
    is_virtual: Optional[bool] = None
    is_active: Optional[bool] = None


class CompanyResponse(CompanyBase):
    """Schema para resposta de Company"""
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class CompanyWithAddressResponse(CompanyResponse):
    """Schema para resposta de Company com dados do endereço"""
    address: Optional[dict] = None

    class Config:
        from_attributes = True 