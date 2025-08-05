"""
Exam Schemas - Pydantic DTOs para validação de Exams
Define schemas para requisições e respostas da API de exames.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum


class ExamTypeResponse(str, Enum):
    """Enum para tipos de exame na API"""
    CLINICAL = "clinical"
    LABORATORY = "laboratory"
    IMAGE = "image"


class ExamCreateRequest(BaseModel):
    """Schema para criação de exame"""
    record_id: UUID = Field(..., description="ID do prontuário")
    type: ExamTypeResponse = Field(..., description="Tipo do exame")
    name: str = Field(..., min_length=1, max_length=200, description="Nome do exame")
    requested_at: datetime = Field(..., description="Data de solicitação")
    visit_id: Optional[UUID] = Field(None, description="ID do atendimento (opcional)")
    result_text: Optional[str] = Field(None, description="Resultado em texto")
    result_file: Optional[str] = Field(None, description="Link/path do arquivo de resultado")

    class Config:
        json_schema_extra = {
            "example": {
                "record_id": "123e4567-e89b-12d3-a456-426614174000",
                "type": "laboratory",
                "name": "Hemograma completo",
                "requested_at": "2025-01-27T09:00:00Z",
                "visit_id": "123e4567-e89b-12d3-a456-426614174001",
                "result_text": "Hb: 14.2 g/dL, Ht: 42%, Leucócitos: 7.500/mm³",
                "result_file": "/files/exams/hemograma_12345.pdf"
            }
        }


class ExamUpdateRequest(BaseModel):
    """Schema para atualização de resultados de exame"""
    result_text: Optional[str] = Field(None, description="Resultado em texto")
    result_file: Optional[str] = Field(None, description="Link/path do arquivo de resultado")

    class Config:
        json_schema_extra = {
            "example": {
                "result_text": "Hb: 14.2 g/dL, Ht: 42%, Leucócitos: 7.500/mm³ - Resultados dentro da normalidade",
                "result_file": "/files/exams/hemograma_12345_revisado.pdf"
            }
        }


class ExamResponse(BaseModel):
    """Schema para resposta de exame"""
    id: UUID
    record_id: UUID
    visit_id: Optional[UUID]
    type: ExamTypeResponse
    name: str
    requested_at: datetime
    result_text: Optional[str]
    result_file: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "record_id": "123e4567-e89b-12d3-a456-426614174001",
                "visit_id": "123e4567-e89b-12d3-a456-426614174002",
                "type": "laboratory",
                "name": "Hemograma completo",
                "requested_at": "2025-01-27T09:00:00Z",
                "result_text": "Hb: 14.2 g/dL, Ht: 42%, Leucócitos: 7.500/mm³",
                "result_file": "/files/exams/hemograma_12345.pdf",
                "created_at": "2025-01-27T10:00:00Z"
            }
        }