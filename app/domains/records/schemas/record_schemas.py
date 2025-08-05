"""
Record Schemas - Pydantic DTOs para validação de Records
Define schemas para requisições e respostas da API de prontuários.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class RecordCreateRequest(BaseModel):
    """Schema para criação de prontuário"""
    patient_id: UUID = Field(..., description="ID do paciente")
    company_id: Optional[UUID] = Field(None, description="ID da clínica (opcional)")
    clinical_history: Optional[str] = Field(None, description="Histórico clínico")
    surgical_history: Optional[str] = Field(None, description="Histórico cirúrgico")
    family_history: Optional[str] = Field(None, description="Histórico familiar")
    habits: Optional[str] = Field(None, description="Hábitos do paciente")
    allergies: Optional[str] = Field(None, description="Alergias")
    current_medications: Optional[str] = Field(None, description="Medicamentos em uso")
    last_diagnoses: Optional[str] = Field(None, description="Últimos diagnósticos")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags de classificação")

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_id": "123e4567-e89b-12d3-a456-426614174002",
                "clinical_history": "Paciente com histórico de hipertensão",
                "surgical_history": "Apendicectomia em 2018",
                "family_history": "Pai com diabetes tipo 2",
                "habits": "Não fumante, pratica exercícios regularmente",
                "allergies": "Alergia a penicilina",
                "current_medications": "Losartana 50mg 1x/dia",
                "last_diagnoses": "Hipertensão arterial sistêmica",
                "tags": ["hipertensao", "cardiologia"]
            }
        }


class RecordUpdateRequest(BaseModel):
    """Schema para atualização de prontuário"""
    clinical_history: Optional[str] = Field(None, description="Histórico clínico")
    surgical_history: Optional[str] = Field(None, description="Histórico cirúrgico")
    family_history: Optional[str] = Field(None, description="Histórico familiar")
    habits: Optional[str] = Field(None, description="Hábitos do paciente")
    allergies: Optional[str] = Field(None, description="Alergias")
    current_medications: Optional[str] = Field(None, description="Medicamentos em uso")
    last_diagnoses: Optional[str] = Field(None, description="Últimos diagnósticos")
    tags: Optional[List[str]] = Field(None, description="Tags de classificação")

    class Config:
        json_schema_extra = {
            "example": {
                "clinical_history": "Paciente com histórico de hipertensão controlada",
                "current_medications": "Losartana 50mg 1x/dia, Sinvastatina 20mg 1x/dia",
                "tags": ["hipertensao", "cardiologia", "controlada"]
            }
        }


class RecordResponse(BaseModel):
    """Schema para resposta de prontuário"""
    id: UUID
    patient_id: UUID
    professional_id: UUID
    company_id: Optional[UUID]
    clinical_history: str
    surgical_history: str
    family_history: str
    habits: str
    allergies: str
    current_medications: str
    last_diagnoses: str
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "patient_id": "123e4567-e89b-12d3-a456-426614174001",
                "professional_id": "123e4567-e89b-12d3-a456-426614174002",
                "company_id": "123e4567-e89b-12d3-a456-426614174003",
                "clinical_history": "Paciente com histórico de hipertensão",
                "surgical_history": "Apendicectomia em 2018",
                "family_history": "Pai com diabetes tipo 2",
                "habits": "Não fumante, pratica exercícios regularmente",
                "allergies": "Alergia a penicilina",
                "current_medications": "Losartana 50mg 1x/dia",
                "last_diagnoses": "Hipertensão arterial sistêmica",
                "tags": ["hipertensao", "cardiologia"],
                "created_at": "2025-01-27T10:00:00Z",
                "updated_at": "2025-01-27T15:30:00Z"
            }
        }