"""
Visit Routes - FastAPI Controllers para Visits
Implementa endpoints REST para gerenciamento de atendimentos.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from ..schemas import (
    VisitCreateRequest,
    VisitUpdateRequest,
    VisitResponse
)
from ..use_cases import (
    CreateVisitUseCase,
    GetVisitUseCase,
    UpdateVisitUseCase,
    GetVisitsByRecordUseCase
)
from ..repositories import VisitRepository, RecordRepository

router = APIRouter()


def get_visit_repository(db: Session = Depends(get_db)) -> VisitRepository:
    """Dependency para obter instância do repositório de visits"""
    return VisitRepository(db)


def get_record_repository(db: Session = Depends(get_db)) -> RecordRepository:
    """Dependency para obter instância do repositório de records"""
    return RecordRepository(db)


@router.post("/", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
async def create_visit(
    request: VisitCreateRequest,
    current_user: dict = Depends(get_current_user),
    visit_repo: VisitRepository = Depends(get_visit_repository),
    record_repo: RecordRepository = Depends(get_record_repository)
):
    """
    Cria um novo atendimento
    
    - **record_id**: ID do prontuário (obrigatório)
    - **professional_id**: ID do profissional (obrigatório)
    - **company_id**: ID da clínica (opcional)
    - Outros campos clínicos opcionais
    """
    try:
        use_case = CreateVisitUseCase(visit_repo, record_repo)
        visit = await use_case.execute(
            record_id=request.record_id,
            professional_id=request.professional_id,
            company_id=request.company_id,
            main_complaint=request.main_complaint,
            current_illness_history=request.current_illness_history,
            past_history=request.past_history,
            physical_exam=request.physical_exam,
            diagnostic_hypothesis=request.diagnostic_hypothesis,
            procedures=request.procedures,
            prescription=request.prescription
        )
        
        return VisitResponse(
            id=visit.id,
            record_id=visit.record_id,
            professional_id=visit.professional_id,
            company_id=visit.company_id,
            main_complaint=visit.main_complaint,
            current_illness_history=visit.current_illness_history,
            past_history=visit.past_history,
            physical_exam=visit.physical_exam,
            diagnostic_hypothesis=visit.diagnostic_hypothesis,
            procedures=visit.procedures,
            prescription=visit.prescription,
            created_at=visit.created_at,
            updated_at=visit.updated_at
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


@router.get("/{visit_id}", response_model=VisitResponse)
async def get_visit(
    visit_id: UUID,
    current_user: dict = Depends(get_current_user),
    visit_repo: VisitRepository = Depends(get_visit_repository)
):
    """
    Busca um atendimento por ID
    
    - **visit_id**: ID do atendimento
    """
    try:
        use_case = GetVisitUseCase(visit_repo)
        visit = await use_case.execute(visit_id)
        
        if not visit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atendimento {visit_id} não encontrado"
            )
        
        return VisitResponse(
            id=visit.id,
            record_id=visit.record_id,
            professional_id=visit.professional_id,
            company_id=visit.company_id,
            main_complaint=visit.main_complaint,
            current_illness_history=visit.current_illness_history,
            past_history=visit.past_history,
            physical_exam=visit.physical_exam,
            diagnostic_hypothesis=visit.diagnostic_hypothesis,
            procedures=visit.procedures,
            prescription=visit.prescription,
            created_at=visit.created_at,
            updated_at=visit.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/record/{record_id}", response_model=List[VisitResponse])
async def get_visits_by_record(
    record_id: UUID,
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    current_user: dict = Depends(get_current_user),
    visit_repo: VisitRepository = Depends(get_visit_repository)
):
    """
    Busca atendimentos de um prontuário com paginação
    
    - **record_id**: ID do prontuário
    - **limit**: Limite de resultados (1-100, padrão: 50)
    - **offset**: Offset para paginação (padrão: 0)
    """
    try:
        use_case = GetVisitsByRecordUseCase(visit_repo)
        visits = await use_case.execute(record_id, limit, offset)
        
        return [
            VisitResponse(
                id=visit.id,
                record_id=visit.record_id,
                professional_id=visit.professional_id,
                company_id=visit.company_id,
                main_complaint=visit.main_complaint,
                current_illness_history=visit.current_illness_history,
                past_history=visit.past_history,
                physical_exam=visit.physical_exam,
                diagnostic_hypothesis=visit.diagnostic_hypothesis,
                procedures=visit.procedures,
                prescription=visit.prescription,
                created_at=visit.created_at,
                updated_at=visit.updated_at
            )
            for visit in visits
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/record/{record_id}/latest", response_model=VisitResponse)
async def get_latest_visit_by_record(
    record_id: UUID,
    current_user: dict = Depends(get_current_user),
    visit_repo: VisitRepository = Depends(get_visit_repository)
):
    """
    Busca o último atendimento de um prontuário
    
    - **record_id**: ID do prontuário
    """
    try:
        use_case = GetVisitsByRecordUseCase(visit_repo)
        visit = await use_case.execute_latest(record_id)
        
        if not visit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum atendimento encontrado para o prontuário {record_id}"
            )
        
        return VisitResponse(
            id=visit.id,
            record_id=visit.record_id,
            professional_id=visit.professional_id,
            company_id=visit.company_id,
            main_complaint=visit.main_complaint,
            current_illness_history=visit.current_illness_history,
            past_history=visit.past_history,
            physical_exam=visit.physical_exam,
            diagnostic_hypothesis=visit.diagnostic_hypothesis,
            procedures=visit.procedures,
            prescription=visit.prescription,
            created_at=visit.created_at,
            updated_at=visit.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.put("/{visit_id}", response_model=VisitResponse)
async def update_visit(
    visit_id: UUID,
    request: VisitUpdateRequest,
    current_user: dict = Depends(get_current_user),
    visit_repo: VisitRepository = Depends(get_visit_repository)
):
    """
    Atualiza dados de um atendimento existente
    
    - **visit_id**: ID do atendimento
    - Todos os campos são opcionais (atualização parcial)
    """
    try:
        use_case = UpdateVisitUseCase(visit_repo)
        visit = await use_case.execute(
            visit_id=visit_id,
            main_complaint=request.main_complaint,
            current_illness_history=request.current_illness_history,
            past_history=request.past_history,
            physical_exam=request.physical_exam,
            diagnostic_hypothesis=request.diagnostic_hypothesis,
            procedures=request.procedures,
            prescription=request.prescription
        )
        
        return VisitResponse(
            id=visit.id,
            record_id=visit.record_id,
            professional_id=visit.professional_id,
            company_id=visit.company_id,
            main_complaint=visit.main_complaint,
            current_illness_history=visit.current_illness_history,
            past_history=visit.past_history,
            physical_exam=visit.physical_exam,
            diagnostic_hypothesis=visit.diagnostic_hypothesis,
            procedures=visit.procedures,
            prescription=visit.prescription,
            created_at=visit.created_at,
            updated_at=visit.updated_at
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