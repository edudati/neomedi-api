from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

# Base schemas
class UserAssistantBase(BaseModel):
    """Schema base para UserAssistant"""
    pass

class AssistantClinicBase(BaseModel):
    """Schema base para AssistantClinic"""
    company_id: UUID4
    is_admin: bool = False

class AssistantProfessionalBase(BaseModel):
    """Schema base para AssistantProfessional"""
    professional_id: UUID4

# Create schemas
class UserAssistantCreate(UserAssistantBase):
    """Schema para criação de UserAssistant"""
    user_id: UUID4

class AssistantClinicCreate(AssistantClinicBase):
    """Schema para criação de AssistantClinic"""
    pass

class AssistantProfessionalCreate(AssistantProfessionalBase):
    """Schema para criação de AssistantProfessional"""
    pass

# Update schemas
class UserAssistantUpdate(UserAssistantBase):
    """Schema para atualização de UserAssistant"""
    pass

class AssistantClinicUpdate(BaseModel):
    """Schema para atualização de AssistantClinic"""
    is_admin: Optional[bool] = None

class AssistantProfessionalUpdate(AssistantProfessionalBase):
    """Schema para atualização de AssistantProfessional"""
    pass

# Response schemas
class UserAssistantResponse(UserAssistantBase):
    """Schema de resposta para UserAssistant"""
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssistantClinicResponse(AssistantClinicBase):
    """Schema de resposta para AssistantClinic"""
    id: UUID4
    assistant_id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssistantProfessionalResponse(AssistantProfessionalBase):
    """Schema de resposta para AssistantProfessional"""
    id: UUID4
    assistant_id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Detailed response schemas
class UserAssistantWithDetailsResponse(UserAssistantResponse):
    """Schema de resposta detalhada para UserAssistant"""
    assistant_clinics: List[AssistantClinicResponse] = []
    assistant_professionals: List[AssistantProfessionalResponse] = []

    class Config:
        from_attributes = True

class AssistantClinicWithDetailsResponse(AssistantClinicResponse):
    """Schema de resposta detalhada para AssistantClinic"""
    company_name: Optional[str] = None
    company_legal_name: Optional[str] = None

    class Config:
        from_attributes = True

class AssistantProfessionalWithDetailsResponse(AssistantProfessionalResponse):
    """Schema de resposta detalhada para AssistantProfessional"""
    professional_treatment_title: Optional[str] = None
    professional_user_name: Optional[str] = None

    class Config:
        from_attributes = True 