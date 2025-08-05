"""
DecisionSupport Schemas - Pydantic DTOs para validação de DecisionSupport
Define schemas para requisições e respostas da API de suporte à decisão.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class DecisionSupportCreateRequest(BaseModel):
    """Schema para criação de suporte à decisão"""
    record_id: UUID = Field(..., description="ID do prontuário")
    visit_id: UUID = Field(..., description="ID do atendimento")
    professional_id: UUID = Field(..., description="ID do profissional")
    llm_model: str = Field(..., min_length=1, max_length=100, description="Modelo LLM utilizado")
    sentiment_summary: Optional[str] = Field(None, description="Resumo da nuvem de sentimentos")
    symptom_summary: Optional[str] = Field(None, description="Resumo da nuvem de sintomas percebidos")
    goal_summary: Optional[str] = Field(None, description="Resumo da nuvem de intenções ou objetivos")
    practice_summary: Optional[str] = Field(None, description="Resumo da nuvem de experiências ou práticas")
    insight_summary: Optional[str] = Field(None, description="Resumo da nuvem de insights ou autoavaliações")
    suggested_conduct: Optional[str] = Field(None, description="Conduta sugerida pelo LLM")
    evidence_summary: Optional[str] = Field(None, description="Resumo de literatura ou protocolos usados")

    class Config:
        json_schema_extra = {
            "example": {
                "record_id": "123e4567-e89b-12d3-a456-426614174000",
                "visit_id": "123e4567-e89b-12d3-a456-426614174001",
                "professional_id": "123e4567-e89b-12d3-a456-426614174002",
                "llm_model": "gpt-4o",
                "sentiment_summary": "Paciente apresenta ansiedade leve relacionada aos sintomas",
                "symptom_summary": "Cefaleia intensa, tensão muscular, alterações do sono",
                "goal_summary": "Busca alívio da dor e melhora da qualidade de vida",
                "practice_summary": "Paciente pratica exercícios regularmente, não fuma",
                "insight_summary": "Reconhece relação entre estresse e sintomas",
                "suggested_conduct": "Manter medicação atual, adicionar técnicas de relaxamento",
                "evidence_summary": "Diretrizes da SBC para hipertensão arterial 2021"
            }
        }


class DecisionSupportUpdateRequest(BaseModel):
    """Schema para atualização de suporte à decisão"""
    sentiment_summary: Optional[str] = Field(None, description="Resumo da nuvem de sentimentos")
    symptom_summary: Optional[str] = Field(None, description="Resumo da nuvem de sintomas percebidos")
    goal_summary: Optional[str] = Field(None, description="Resumo da nuvem de intenções ou objetivos")
    practice_summary: Optional[str] = Field(None, description="Resumo da nuvem de experiências ou práticas")
    insight_summary: Optional[str] = Field(None, description="Resumo da nuvem de insights ou autoavaliações")
    suggested_conduct: Optional[str] = Field(None, description="Conduta sugerida pelo LLM")
    evidence_summary: Optional[str] = Field(None, description="Resumo de literatura ou protocolos usados")

    class Config:
        json_schema_extra = {
            "example": {
                "suggested_conduct": "Manter Losartana 50mg, adicionar meditação 10min/dia, retorno 15 dias",
                "evidence_summary": "Evidências mostram benefício da meditação em hipertensão (JAHA 2017)"
            }
        }


class DecisionSupportResponse(BaseModel):
    """Schema para resposta de suporte à decisão"""
    id: UUID
    record_id: UUID
    visit_id: UUID
    professional_id: UUID
    sentiment_summary: Optional[str]
    symptom_summary: Optional[str]
    goal_summary: Optional[str]
    practice_summary: Optional[str]
    insight_summary: Optional[str]
    suggested_conduct: Optional[str]
    evidence_summary: Optional[str]
    llm_model: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "record_id": "123e4567-e89b-12d3-a456-426614174001",
                "visit_id": "123e4567-e89b-12d3-a456-426614174002",
                "professional_id": "123e4567-e89b-12d3-a456-426614174003",
                "sentiment_summary": "Paciente apresenta ansiedade leve relacionada aos sintomas",
                "symptom_summary": "Cefaleia intensa, tensão muscular, alterações do sono",
                "goal_summary": "Busca alívio da dor e melhora da qualidade de vida",
                "practice_summary": "Paciente pratica exercícios regularmente, não fuma",
                "insight_summary": "Reconhece relação entre estresse e sintomas",
                "suggested_conduct": "Manter medicação atual, adicionar técnicas de relaxamento",
                "evidence_summary": "Diretrizes da SBC para hipertensão arterial 2021",
                "llm_model": "gpt-4o",
                "created_at": "2025-01-27T10:00:00Z"
            }
        }