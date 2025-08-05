"""
DecisionSupport Routes - FastAPI Controllers para DecisionSupport
Implementa endpoints REST para gerenciamento de suporte à decisão.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from ..schemas import (
    DecisionSupportCreateRequest,
    DecisionSupportUpdateRequest,
    DecisionSupportResponse
)
from ..use_cases import (
    CreateDecisionSupportUseCase,
    GetDecisionSupportByVisitUseCase,
    UpdateDecisionSupportUseCase
)
from ..repositories import DecisionSupportRepository, RecordRepository, VisitRepository

router = APIRouter()


def get_decision_support_repository(db: Session = Depends(get_db)) -> DecisionSupportRepository:
    """Dependency para obter instância do repositório de decision support"""
    return DecisionSupportRepository(db)


def get_record_repository(db: Session = Depends(get_db)) -> RecordRepository:
    """Dependency para obter instância do repositório de records"""
    return RecordRepository(db)


def get_visit_repository(db: Session = Depends(get_db)) -> VisitRepository:
    """Dependency para obter instância do repositório de visits"""
    return VisitRepository(db)


@router.post("/", response_model=DecisionSupportResponse, status_code=status.HTTP_201_CREATED)
async def create_decision_support(
    request: DecisionSupportCreateRequest,
    current_user: dict = Depends(get_current_user),
    decision_support_repo: DecisionSupportRepository = Depends(get_decision_support_repository),
    record_repo: RecordRepository = Depends(get_record_repository),
    visit_repo: VisitRepository = Depends(get_visit_repository)
):
    """
    Cria um novo suporte à decisão
    
    - **record_id**: ID do prontuário (obrigatório)
    - **visit_id**: ID do atendimento (obrigatório)
    - **professional_id**: ID do profissional (obrigatório)
    - **llm_model**: Modelo LLM utilizado (obrigatório, 1-100 caracteres)
    - Campos de análise LLM opcionais: sentiment_summary, symptom_summary, etc.
    
    **Importante**: Relacionamento 1:1 com atendimento - apenas um suporte por visit.
    """
    try:
        use_case = CreateDecisionSupportUseCase(decision_support_repo, record_repo, visit_repo)
        decision_support = await use_case.execute(
            record_id=request.record_id,
            visit_id=request.visit_id,
            professional_id=request.professional_id,
            llm_model=request.llm_model,
            sentiment_summary=request.sentiment_summary,
            symptom_summary=request.symptom_summary,
            goal_summary=request.goal_summary,
            practice_summary=request.practice_summary,
            insight_summary=request.insight_summary,
            suggested_conduct=request.suggested_conduct,
            evidence_summary=request.evidence_summary
        )
        
        return DecisionSupportResponse(
            id=decision_support.id,
            record_id=decision_support.record_id,
            visit_id=decision_support.visit_id,
            professional_id=decision_support.professional_id,
            sentiment_summary=decision_support.sentiment_summary,
            symptom_summary=decision_support.symptom_summary,
            goal_summary=decision_support.goal_summary,
            practice_summary=decision_support.practice_summary,
            insight_summary=decision_support.insight_summary,
            suggested_conduct=decision_support.suggested_conduct,
            evidence_summary=decision_support.evidence_summary,
            llm_model=decision_support.llm_model,
            created_at=decision_support.created_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/visit/{visit_id}", response_model=DecisionSupportResponse)
async def get_decision_support_by_visit(
    visit_id: UUID,
    current_user: dict = Depends(get_current_user),
    decision_support_repo: DecisionSupportRepository = Depends(get_decision_support_repository)
):
    """
    Busca suporte à decisão por ID do atendimento
    
    - **visit_id**: ID do atendimento
    
    **Relacionamento 1:1**: Cada atendimento pode ter apenas um suporte à decisão.
    """
    try:
        use_case = GetDecisionSupportByVisitUseCase(decision_support_repo)
        decision_support = await use_case.execute(visit_id)
        
        if not decision_support:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum suporte à decisão encontrado para o atendimento {visit_id}"
            )
        
        return DecisionSupportResponse(
            id=decision_support.id,
            record_id=decision_support.record_id,
            visit_id=decision_support.visit_id,
            professional_id=decision_support.professional_id,
            sentiment_summary=decision_support.sentiment_summary,
            symptom_summary=decision_support.symptom_summary,
            goal_summary=decision_support.goal_summary,
            practice_summary=decision_support.practice_summary,
            insight_summary=decision_support.insight_summary,
            suggested_conduct=decision_support.suggested_conduct,
            evidence_summary=decision_support.evidence_summary,
            llm_model=decision_support.llm_model,
            created_at=decision_support.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/record/{record_id}", response_model=List[DecisionSupportResponse])
async def get_decision_supports_by_record(
    record_id: UUID,
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    current_user: dict = Depends(get_current_user),
    decision_support_repo: DecisionSupportRepository = Depends(get_decision_support_repository)
):
    """
    Busca suportes à decisão de um prontuário com paginação
    
    - **record_id**: ID do prontuário
    - **limit**: Limite de resultados (1-100, padrão: 50)
    - **offset**: Offset para paginação (padrão: 0)
    
    **Retorna**: Lista de todos os suportes à decisão do prontuário (um por atendimento).
    """
    try:
        use_case = GetDecisionSupportByVisitUseCase(decision_support_repo)
        decision_supports = await use_case.execute_by_record(record_id, limit, offset)
        
        return [
            DecisionSupportResponse(
                id=decision_support.id,
                record_id=decision_support.record_id,
                visit_id=decision_support.visit_id,
                professional_id=decision_support.professional_id,
                sentiment_summary=decision_support.sentiment_summary,
                symptom_summary=decision_support.symptom_summary,
                goal_summary=decision_support.goal_summary,
                practice_summary=decision_support.practice_summary,
                insight_summary=decision_support.insight_summary,
                suggested_conduct=decision_support.suggested_conduct,
                evidence_summary=decision_support.evidence_summary,
                llm_model=decision_support.llm_model,
                created_at=decision_support.created_at
            )
            for decision_support in decision_supports
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.put("/{decision_support_id}", response_model=DecisionSupportResponse)
async def update_decision_support(
    decision_support_id: UUID,
    request: DecisionSupportUpdateRequest,
    current_user: dict = Depends(get_current_user),
    decision_support_repo: DecisionSupportRepository = Depends(get_decision_support_repository)
):
    """
    Atualiza dados de um suporte à decisão existente
    
    - **decision_support_id**: ID do suporte à decisão
    - Todos os campos de análise são opcionais (atualização parcial)
    
    **Campos atualizáveis**:
    - sentiment_summary, symptom_summary, goal_summary
    - practice_summary, insight_summary
    - suggested_conduct, evidence_summary
    """
    try:
        use_case = UpdateDecisionSupportUseCase(decision_support_repo)
        decision_support = await use_case.execute(
            decision_support_id=decision_support_id,
            sentiment_summary=request.sentiment_summary,
            symptom_summary=request.symptom_summary,
            goal_summary=request.goal_summary,
            practice_summary=request.practice_summary,
            insight_summary=request.insight_summary,
            suggested_conduct=request.suggested_conduct,
            evidence_summary=request.evidence_summary
        )
        
        return DecisionSupportResponse(
            id=decision_support.id,
            record_id=decision_support.record_id,
            visit_id=decision_support.visit_id,
            professional_id=decision_support.professional_id,
            sentiment_summary=decision_support.sentiment_summary,
            symptom_summary=decision_support.symptom_summary,
            goal_summary=decision_support.goal_summary,
            practice_summary=decision_support.practice_summary,
            insight_summary=decision_support.insight_summary,
            suggested_conduct=decision_support.suggested_conduct,
            evidence_summary=decision_support.evidence_summary,
            llm_model=decision_support.llm_model,
            created_at=decision_support.created_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )