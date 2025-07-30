from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ProfessionalBase(BaseModel):
    """Schema base para Professional"""
    treatment_title: str
    profile_completed: bool = False
    bio: Optional[str] = None


class ProfessionalCreate(ProfessionalBase):
    """Schema para criação de Professional"""
    user_id: UUID


class ProfessionalUpdate(BaseModel):
    """Schema para atualização de Professional"""
    treatment_title: Optional[str] = None
    profile_completed: Optional[bool] = None
    bio: Optional[str] = None


class ProfessionalResponse(ProfessionalBase):
    """Schema para resposta de Professional"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProfessionalWithUserResponse(ProfessionalResponse):
    """Schema para resposta de Professional com dados do usuário"""
    user: dict  # Dados básicos do User

    class Config:
        from_attributes = True


class ProfessionalWithDetailsResponse(ProfessionalWithUserResponse):
    """Schema para resposta de Professional com especialidades e profissões"""
    specialties: List[dict] = []
    professions: List[dict] = []

    class Config:
        from_attributes = True 