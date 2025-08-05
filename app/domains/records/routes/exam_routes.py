"""
Exam Routes - FastAPI Controllers para Exams
Implementa endpoints REST para gerenciamento de exames.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from ..schemas import (
    ExamCreateRequest,
    ExamUpdateRequest,
    ExamResponse,
    ExamTypeResponse
)
from ..use_cases import (
    CreateExamUseCase,
    GetExamsByRecordUseCase,
    UpdateExamResultsUseCase
)
from ..repositories import ExamRepository, RecordRepository, VisitRepository
from ..entities.exam import ExamType

router = APIRouter()


def get_exam_repository(db: Session = Depends(get_db)) -> ExamRepository:
    """Dependency para obter instância do repositório de exams"""
    return ExamRepository(db)


def get_record_repository(db: Session = Depends(get_db)) -> RecordRepository:
    """Dependency para obter instância do repositório de records"""
    return RecordRepository(db)


def get_visit_repository(db: Session = Depends(get_db)) -> VisitRepository:
    """Dependency para obter instância do repositório de visits"""
    return VisitRepository(db)


@router.post("/", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
async def create_exam(
    request: ExamCreateRequest,
    current_user: dict = Depends(get_current_user),
    exam_repo: ExamRepository = Depends(get_exam_repository),
    record_repo: RecordRepository = Depends(get_record_repository),
    visit_repo: VisitRepository = Depends(get_visit_repository)
):
    """
    Cria um novo exame
    
    - **record_id**: ID do prontuário (obrigatório)
    - **type**: Tipo do exame - clinical, laboratory ou image (obrigatório)
    - **name**: Nome do exame (obrigatório, 1-200 caracteres)
    - **requested_at**: Data de solicitação (obrigatória)
    - **visit_id**: ID do atendimento (opcional)
    - **result_text**: Resultado em texto (opcional)
    - **result_file**: Link/path do arquivo de resultado (opcional)
    """
    try:
        # Converter enum da API para entidade
        exam_type_mapping = {
            ExamTypeResponse.CLINICAL: ExamType.CLINICAL,
            ExamTypeResponse.LABORATORY: ExamType.LABORATORY,
            ExamTypeResponse.IMAGE: ExamType.IMAGE
        }
        entity_exam_type = exam_type_mapping[request.type]
        
        use_case = CreateExamUseCase(exam_repo, record_repo, visit_repo)
        exam = await use_case.execute(
            record_id=request.record_id,
            exam_type=entity_exam_type,
            name=request.name,
            requested_at=request.requested_at,
            visit_id=request.visit_id,
            result_text=request.result_text,
            result_file=request.result_file
        )
        
        # Converter enum da entidade para API
        api_exam_type_mapping = {
            ExamType.CLINICAL: ExamTypeResponse.CLINICAL,
            ExamType.LABORATORY: ExamTypeResponse.LABORATORY,
            ExamType.IMAGE: ExamTypeResponse.IMAGE
        }
        
        return ExamResponse(
            id=exam.id,
            record_id=exam.record_id,
            visit_id=exam.visit_id,
            type=api_exam_type_mapping[exam.type],
            name=exam.name,
            requested_at=exam.requested_at,
            result_text=exam.result_text,
            result_file=exam.result_file,
            created_at=exam.created_at
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


@router.get("/record/{record_id}", response_model=List[ExamResponse])
async def get_exams_by_record(
    record_id: UUID,
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    exam_type: ExamTypeResponse = Query(None, description="Filtrar por tipo de exame"),
    current_user: dict = Depends(get_current_user),
    exam_repo: ExamRepository = Depends(get_exam_repository)
):
    """
    Busca exames de um prontuário com paginação e filtros
    
    - **record_id**: ID do prontuário
    - **limit**: Limite de resultados (1-100, padrão: 50)
    - **offset**: Offset para paginação (padrão: 0)
    - **exam_type**: Filtrar por tipo de exame (opcional)
    """
    try:
        use_case = GetExamsByRecordUseCase(exam_repo)
        
        # Se tipo especificado, filtrar por tipo
        if exam_type:
            exam_type_mapping = {
                ExamTypeResponse.CLINICAL: ExamType.CLINICAL,
                ExamTypeResponse.LABORATORY: ExamType.LABORATORY,
                ExamTypeResponse.IMAGE: ExamType.IMAGE
            }
            entity_exam_type = exam_type_mapping[exam_type]
            exams = await use_case.execute_by_type(record_id, entity_exam_type)
        else:
            exams = await use_case.execute(record_id, limit, offset)
        
        # Converter enum da entidade para API
        api_exam_type_mapping = {
            ExamType.CLINICAL: ExamTypeResponse.CLINICAL,
            ExamType.LABORATORY: ExamTypeResponse.LABORATORY,
            ExamType.IMAGE: ExamTypeResponse.IMAGE
        }
        
        return [
            ExamResponse(
                id=exam.id,
                record_id=exam.record_id,
                visit_id=exam.visit_id,
                type=api_exam_type_mapping[exam.type],
                name=exam.name,
                requested_at=exam.requested_at,
                result_text=exam.result_text,
                result_file=exam.result_file,
                created_at=exam.created_at
            )
            for exam in exams
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/visit/{visit_id}", response_model=List[ExamResponse])
async def get_exams_by_visit(
    visit_id: UUID,
    current_user: dict = Depends(get_current_user),
    exam_repo: ExamRepository = Depends(get_exam_repository)
):
    """
    Busca exames vinculados a um atendimento
    
    - **visit_id**: ID do atendimento
    """
    try:
        use_case = GetExamsByRecordUseCase(exam_repo)
        exams = await use_case.execute_by_visit(visit_id)
        
        # Converter enum da entidade para API
        api_exam_type_mapping = {
            ExamType.CLINICAL: ExamTypeResponse.CLINICAL,
            ExamType.LABORATORY: ExamTypeResponse.LABORATORY,
            ExamType.IMAGE: ExamTypeResponse.IMAGE
        }
        
        return [
            ExamResponse(
                id=exam.id,
                record_id=exam.record_id,
                visit_id=exam.visit_id,
                type=api_exam_type_mapping[exam.type],
                name=exam.name,
                requested_at=exam.requested_at,
                result_text=exam.result_text,
                result_file=exam.result_file,
                created_at=exam.created_at
            )
            for exam in exams
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam_results(
    exam_id: UUID,
    request: ExamUpdateRequest,
    current_user: dict = Depends(get_current_user),
    exam_repo: ExamRepository = Depends(get_exam_repository)
):
    """
    Atualiza resultados de um exame existente
    
    - **exam_id**: ID do exame
    - **result_text**: Resultado em texto (opcional)
    - **result_file**: Link/path do arquivo de resultado (opcional)
    """
    try:
        use_case = UpdateExamResultsUseCase(exam_repo)
        exam = await use_case.execute(
            exam_id=exam_id,
            result_text=request.result_text,
            result_file=request.result_file
        )
        
        # Converter enum da entidade para API
        api_exam_type_mapping = {
            ExamType.CLINICAL: ExamTypeResponse.CLINICAL,
            ExamType.LABORATORY: ExamTypeResponse.LABORATORY,
            ExamType.IMAGE: ExamTypeResponse.IMAGE
        }
        
        return ExamResponse(
            id=exam.id,
            record_id=exam.record_id,
            visit_id=exam.visit_id,
            type=api_exam_type_mapping[exam.type],
            name=exam.name,
            requested_at=exam.requested_at,
            result_text=exam.result_text,
            result_file=exam.result_file,
            created_at=exam.created_at
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