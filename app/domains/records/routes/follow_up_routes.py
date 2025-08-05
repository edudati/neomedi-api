"""
FollowUp Routes - FastAPI Controllers para FollowUps
Implementa endpoints REST para gerenciamento de evoluções rápidas.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from ..schemas import (
    FollowUpCreateRequest,
    FollowUpUpdateRequest,
    FollowUpResponse
)
from ..use_cases import (
    CreateFollowUpUseCase,
    GetFollowUpsByRecordUseCase,
    UpdateFollowUpUseCase
)
from ..repositories import FollowUpRepository, RecordRepository, VisitRepository

router = APIRouter()


def get_follow_up_repository(db: Session = Depends(get_db)) -> FollowUpRepository:
    """Dependency para obter instância do repositório de follow-ups"""
    return FollowUpRepository(db)


def get_record_repository(db: Session = Depends(get_db)) -> RecordRepository:
    """Dependency para obter instância do repositório de records"""
    return RecordRepository(db)


def get_visit_repository(db: Session = Depends(get_db)) -> VisitRepository:
    """Dependency para obter instância do repositório de visits"""
    return VisitRepository(db)


@router.post("/", response_model=FollowUpResponse, status_code=status.HTTP_201_CREATED)
async def create_follow_up(
    request: FollowUpCreateRequest,
    current_user: dict = Depends(get_current_user),
    follow_up_repo: FollowUpRepository = Depends(get_follow_up_repository),
    record_repo: RecordRepository = Depends(get_record_repository),
    visit_repo: VisitRepository = Depends(get_visit_repository)
):
    """
    Cria uma nova evolução rápida
    
    - **record_id**: ID do prontuário (obrigatório)
    - **note**: Nota da evolução (obrigatória, 1-2000 caracteres)
    - **visit_id**: ID do atendimento (opcional)
    - **tags**: Tags de categorização (opcional)
    """
    try:
        use_case = CreateFollowUpUseCase(follow_up_repo, record_repo, visit_repo)
        follow_up = await use_case.execute(
            record_id=request.record_id,
            note=request.note,
            visit_id=request.visit_id,
            tags=request.tags
        )
        
        return FollowUpResponse(
            id=follow_up.id,
            record_id=follow_up.record_id,
            visit_id=follow_up.visit_id,
            note=follow_up.note,
            tags=follow_up.tags,
            created_at=follow_up.created_at
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


@router.get("/record/{record_id}", response_model=List[FollowUpResponse])
async def get_follow_ups_by_record(
    record_id: UUID,
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    current_user: dict = Depends(get_current_user),
    follow_up_repo: FollowUpRepository = Depends(get_follow_up_repository)
):
    """
    Busca evoluções de um prontuário com paginação
    
    - **record_id**: ID do prontuário
    - **limit**: Limite de resultados (1-100, padrão: 50)
    - **offset**: Offset para paginação (padrão: 0)
    """
    try:
        use_case = GetFollowUpsByRecordUseCase(follow_up_repo)
        follow_ups = await use_case.execute(record_id, limit, offset)
        
        return [
            FollowUpResponse(
                id=follow_up.id,
                record_id=follow_up.record_id,
                visit_id=follow_up.visit_id,
                note=follow_up.note,
                tags=follow_up.tags,
                created_at=follow_up.created_at
            )
            for follow_up in follow_ups
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/visit/{visit_id}", response_model=List[FollowUpResponse])
async def get_follow_ups_by_visit(
    visit_id: UUID,
    current_user: dict = Depends(get_current_user),
    follow_up_repo: FollowUpRepository = Depends(get_follow_up_repository)
):
    """
    Busca evoluções vinculadas a um atendimento
    
    - **visit_id**: ID do atendimento
    """
    try:
        use_case = GetFollowUpsByRecordUseCase(follow_up_repo)
        follow_ups = await use_case.execute_by_visit(visit_id)
        
        return [
            FollowUpResponse(
                id=follow_up.id,
                record_id=follow_up.record_id,
                visit_id=follow_up.visit_id,
                note=follow_up.note,
                tags=follow_up.tags,
                created_at=follow_up.created_at
            )
            for follow_up in follow_ups
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.put("/{follow_up_id}", response_model=FollowUpResponse)
async def update_follow_up(
    follow_up_id: UUID,
    request: FollowUpUpdateRequest,
    current_user: dict = Depends(get_current_user),
    follow_up_repo: FollowUpRepository = Depends(get_follow_up_repository)
):
    """
    Atualiza dados de uma evolução existente
    
    - **follow_up_id**: ID da evolução
    - **note**: Nova nota (opcional, 1-2000 caracteres)
    - **tags**: Novas tags (opcional)
    """
    try:
        use_case = UpdateFollowUpUseCase(follow_up_repo)
        follow_up = await use_case.execute(
            follow_up_id=follow_up_id,
            note=request.note,
            tags=request.tags
        )
        
        return FollowUpResponse(
            id=follow_up.id,
            record_id=follow_up.record_id,
            visit_id=follow_up.visit_id,
            note=follow_up.note,
            tags=follow_up.tags,
            created_at=follow_up.created_at
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