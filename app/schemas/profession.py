from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ProfessionBase(BaseModel):
    """Schema base para Profession"""
    name: str
    cbo_code: Optional[str] = None
    council_type: Optional[str] = None
    is_active: bool = True


class ProfessionCreate(ProfessionBase):
    """Schema para criação de Profession"""
    pass


class ProfessionUpdate(BaseModel):
    """Schema para atualização de Profession"""
    name: Optional[str] = None
    cbo_code: Optional[str] = None
    council_type: Optional[str] = None
    is_active: Optional[bool] = None


class ProfessionResponse(ProfessionBase):
    """Schema para resposta de Profession"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProfessionalProfessionCreate(BaseModel):
    """Schema para associar profissional a profissão"""
    professional_id: UUID
    profession_id: UUID
    council_number: Optional[str] = None
    council_uf: Optional[str] = None
    rqe_type: Optional[str] = None
    is_primary: bool = False


class ProfessionalProfessionUpdate(BaseModel):
    """Schema para atualização de ProfessionalProfession"""
    council_number: Optional[str] = None
    council_uf: Optional[str] = None
    rqe_type: Optional[str] = None
    is_primary: Optional[bool] = None


class ProfessionalProfessionResponse(BaseModel):
    """Schema para resposta de ProfessionalProfession"""
    id: UUID
    professional_id: UUID
    profession_id: UUID
    profession: ProfessionResponse
    council_number: Optional[str] = None
    council_uf: Optional[str] = None
    rqe_type: Optional[str] = None
    is_primary: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 