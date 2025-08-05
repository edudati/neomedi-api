"""
FollowUp Schemas - Pydantic DTOs para validação de FollowUps
Define schemas para requisições e respostas da API de evoluções rápidas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class FollowUpCreateRequest(BaseModel):
    """Schema para criação de evolução rápida"""
    record_id: UUID = Field(..., description="ID do prontuário")
    note: str = Field(..., min_length=1, max_length=2000, description="Nota da evolução (obrigatória)")
    visit_id: Optional[UUID] = Field(None, description="ID do atendimento (opcional)")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags de categorização")

    class Config:
        json_schema_extra = {
            "example": {
                "record_id": "123e4567-e89b-12d3-a456-426614174000",
                "note": "Paciente retornou relatando melhora da cefaleia após ajuste medicamentoso. Pressão arterial controlada.",
                "visit_id": "123e4567-e89b-12d3-a456-426614174001",
                "tags": ["melhora", "pressao_controlada", "seguimento"]
            }
        }


class FollowUpUpdateRequest(BaseModel):
    """Schema para atualização de evolução rápida"""
    note: Optional[str] = Field(None, min_length=1, max_length=2000, description="Nova nota")
    tags: Optional[List[str]] = Field(None, description="Novas tags")

    class Config:
        json_schema_extra = {
            "example": {
                "note": "Paciente retornou relatando melhora significativa da cefaleia. PA: 130x80 mmHg.",
                "tags": ["melhora_significativa", "pressao_controlada", "seguimento", "sucesso_tratamento"]
            }
        }


class FollowUpResponse(BaseModel):
    """Schema para resposta de evolução rápida"""
    id: UUID
    record_id: UUID
    visit_id: Optional[UUID]
    note: str
    tags: List[str]
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "record_id": "123e4567-e89b-12d3-a456-426614174001",
                "visit_id": "123e4567-e89b-12d3-a456-426614174002",
                "note": "Paciente retornou relatando melhora da cefaleia após ajuste medicamentoso.",
                "tags": ["melhora", "pressao_controlada", "seguimento"],
                "created_at": "2025-01-27T10:00:00Z"
            }
        }