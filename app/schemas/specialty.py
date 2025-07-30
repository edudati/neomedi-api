from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class SpecialtyBase(BaseModel):
    """Schema base para Specialty"""
    name: str
    slug: str
    category: Optional[str] = None
    description: Optional[str] = None
    is_public: bool = True
    is_visible: bool = True


class SpecialtyCreate(SpecialtyBase):
    """Schema para criação de Specialty"""
    created_by: Optional[UUID] = None


class SpecialtyUpdate(BaseModel):
    """Schema para atualização de Specialty"""
    name: Optional[str] = None
    slug: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    is_visible: Optional[bool] = None


class SpecialtyResponse(SpecialtyBase):
    """Schema para resposta de Specialty"""
    id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProfessionalSpecialtyCreate(BaseModel):
    """Schema para associar profissional a especialidade"""
    professional_id: UUID
    specialty_id: UUID


class ProfessionalSpecialtyResponse(BaseModel):
    """Schema para resposta de ProfessionalSpecialty"""
    id: UUID
    professional_id: UUID
    specialty_id: UUID
    specialty: SpecialtyResponse
    created_at: datetime

    class Config:
        from_attributes = True 