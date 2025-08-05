"""
Visit Schemas - Pydantic DTOs para validação de Visits
Define schemas para requisições e respostas da API de atendimentos.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class VisitCreateRequest(BaseModel):
    """Schema para criação de atendimento"""
    patient_id: UUID = Field(..., description="ID do paciente (para buscar o record automaticamente)")
    professional_id: Optional[UUID] = Field(None, description="ID do profissional (opcional, obtido do JWT se não fornecido)")
    company_id: Optional[UUID] = Field(None, description="ID da clínica (opcional)")
    main_complaint: Optional[str] = Field(None, description="Queixa principal")
    current_illness_history: Optional[str] = Field(None, description="História da moléstia atual (HMA)")
    past_history: Optional[str] = Field(None, description="Histórico e antecedentes")
    physical_exam: Optional[str] = Field(None, description="Exame físico")
    diagnostic_hypothesis: Optional[str] = Field(None, description="Hipótese diagnóstica")
    procedures: Optional[str] = Field(None, description="Condutas ou evoluções aplicadas")
    prescription: Optional[str] = Field(None, description="Prescrição ou recomendações")

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_id": "123e4567-e89b-12d3-a456-426614174002",
                "main_complaint": "Dor de cabeça há 3 dias",
                "current_illness_history": "Paciente relata cefaleia intensa iniciada há 3 dias",
                "past_history": "Hipertensão arterial em uso de Losartana",
                "physical_exam": "PA: 140x90 mmHg, FC: 80 bpm, Tax: 36.5°C",
                "diagnostic_hypothesis": "Cefaleia tensional",
                "procedures": "Orientações sobre controle da pressão arterial",
                "prescription": "Dipirona 500mg se dor, retorno em 7 dias"
            }
        }


class VisitUpdateRequest(BaseModel):
    """Schema para atualização de atendimento"""
    main_complaint: Optional[str] = Field(None, description="Queixa principal")
    current_illness_history: Optional[str] = Field(None, description="História da moléstia atual (HMA)")
    past_history: Optional[str] = Field(None, description="Histórico e antecedentes")
    physical_exam: Optional[str] = Field(None, description="Exame físico")
    diagnostic_hypothesis: Optional[str] = Field(None, description="Hipótese diagnóstica")
    procedures: Optional[str] = Field(None, description="Condutas ou evoluções aplicadas")
    prescription: Optional[str] = Field(None, description="Prescrição ou recomendações")

    class Config:
        json_schema_extra = {
            "example": {
                "diagnostic_hypothesis": "Cefaleia secundária à hipertensão",
                "procedures": "Ajuste medicamentoso, orientações dietéticas",
                "prescription": "Losartana 100mg 1x/dia, Dipirona 500mg se dor"
            }
        }


class VisitResponse(BaseModel):
    """Schema para resposta de atendimento"""
    id: UUID
    record_id: UUID
    professional_id: UUID
    company_id: Optional[UUID]
    main_complaint: str
    current_illness_history: str
    past_history: str
    physical_exam: str
    diagnostic_hypothesis: str
    procedures: str
    prescription: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "record_id": "123e4567-e89b-12d3-a456-426614174001",
                "professional_id": "123e4567-e89b-12d3-a456-426614174002",
                "company_id": "123e4567-e89b-12d3-a456-426614174003",
                "main_complaint": "Dor de cabeça há 3 dias",
                "current_illness_history": "Paciente relata cefaleia intensa iniciada há 3 dias",
                "past_history": "Hipertensão arterial em uso de Losartana",
                "physical_exam": "PA: 140x90 mmHg, FC: 80 bpm, Tax: 36.5°C",
                "diagnostic_hypothesis": "Cefaleia tensional",
                "procedures": "Orientações sobre controle da pressão arterial",
                "prescription": "Dipirona 500mg se dor, retorno em 7 dias",
                "created_at": "2025-01-27T10:00:00Z",
                "updated_at": "2025-01-27T15:30:00Z"
            }
        }