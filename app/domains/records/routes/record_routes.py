"""
Record Routes - FastAPI Controllers para Records
Implementa endpoints REST para gerenciamento de prontuários.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from ..schemas import (
    RecordCreateRequest,
    RecordUpdateRequest, 
    RecordResponse
)
from ..use_cases import (
    CreateRecordUseCase,
    GetRecordUseCase,
    UpdateRecordUseCase
)
from ..repositories import RecordRepository

router = APIRouter()


def get_record_repository(db: Session = Depends(get_db)) -> RecordRepository:
    """Dependency para obter instância do repositório de records"""
    return RecordRepository(db)


@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    request: RecordCreateRequest,
    current_user: dict = Depends(get_current_user),
    record_repo: RecordRepository = Depends(get_record_repository)
):
    """
    Cria um novo prontuário para um paciente
    
    - **patient_id**: ID do paciente (obrigatório)
    - **company_id**: ID da clínica (opcional)
    - professional_id: Obtido automaticamente do usuário logado
    - Outros campos clínicos opcionais
    """
    try:
        # Pegar professional_id do JWT do usuário logado
        professional_id = current_user.get("user_uid")
        if not professional_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_uid não encontrado no token"
            )
        
        # Usar o use case para criar o record
        use_case = CreateRecordUseCase(record_repo)
        record = await use_case.execute(
            patient_id=request.patient_id,
            professional_id=UUID(professional_id),
            company_id=request.company_id,
            clinical_history=request.clinical_history,
            surgical_history=request.surgical_history,
            family_history=request.family_history,
            habits=request.habits,
            allergies=request.allergies,
            current_medications=request.current_medications,
            last_diagnoses=request.last_diagnoses,
            tags=request.tags
        )
        
        # Converter entidade para schema de resposta
        return RecordResponse(
            id=record.id,
            patient_id=record.patient_id,
            professional_id=record.professional_id,
            company_id=record.company_id,
            clinical_history=record.clinical_history,
            surgical_history=record.surgical_history,
            family_history=record.family_history,
            habits=record.habits,
            allergies=record.allergies,
            current_medications=record.current_medications,
            last_diagnoses=record.last_diagnoses,
            tags=record.tags,
            created_at=record.created_at,
            updated_at=record.updated_at
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


@router.get("/{record_id}", response_model=RecordResponse)
async def get_record(
    record_id: UUID,
    current_user: dict = Depends(get_current_user),
    record_repo: RecordRepository = Depends(get_record_repository)
):
    """
    Busca um prontuário por ID
    
    - **record_id**: ID do prontuário
    """
    try:
        use_case = GetRecordUseCase(record_repo)
        record = await use_case.execute_by_id(record_id)
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prontuário {record_id} não encontrado"
            )
        
        return RecordResponse(
            id=record.id,
            patient_id=record.patient_id,
            professional_id=record.professional_id,
            company_id=record.company_id,
            clinical_history=record.clinical_history,
            surgical_history=record.surgical_history,
            family_history=record.family_history,
            habits=record.habits,
            allergies=record.allergies,
            current_medications=record.current_medications,
            last_diagnoses=record.last_diagnoses,
            tags=record.tags,
            created_at=record.created_at,
            updated_at=record.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/patient/{patient_id}", response_model=List[RecordResponse])
async def get_records_by_patient(
    patient_id: UUID,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar"),
    current_user: dict = Depends(get_current_user),
    record_repo: RecordRepository = Depends(get_record_repository)
):
    """
    Busca prontuários por ID do paciente com paginação
    
    - **patient_id**: ID do paciente
    - **skip**: Número de registros para pular (paginação)
    - **limit**: Número máximo de registros para retornar (máx: 1000)
    """
    try:
        use_case = GetRecordUseCase(record_repo)
        records = await use_case.execute_by_patient_id(patient_id, skip, limit)
        
        return [
            RecordResponse(
                id=record.id,
                patient_id=record.patient_id,
                professional_id=record.professional_id,
                company_id=record.company_id,
                clinical_history=record.clinical_history,
                surgical_history=record.surgical_history,
                family_history=record.family_history,
                habits=record.habits,
                allergies=record.allergies,
                current_medications=record.current_medications,
                last_diagnoses=record.last_diagnoses,
                tags=record.tags,
                created_at=record.created_at,
                updated_at=record.updated_at
            )
            for record in records
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.put("/{record_id}", response_model=RecordResponse)
async def update_record(
    record_id: UUID,
    request: RecordUpdateRequest,
    current_user: dict = Depends(get_current_user),
    record_repo: RecordRepository = Depends(get_record_repository)
):
    """
    Atualiza dados de um prontuário existente
    
    - **record_id**: ID do prontuário
    - Todos os campos são opcionais (atualização parcial)
    """
    try:
        use_case = UpdateRecordUseCase(record_repo)
        record = await use_case.execute(
            record_id=record_id,
            clinical_history=request.clinical_history,
            surgical_history=request.surgical_history,
            family_history=request.family_history,
            habits=request.habits,
            allergies=request.allergies,
            current_medications=request.current_medications,
            last_diagnoses=request.last_diagnoses,
            tags=request.tags
        )
        
        return RecordResponse(
            id=record.id,
            patient_id=record.patient_id,
            professional_id=record.professional_id,
            company_id=record.company_id,
            clinical_history=record.clinical_history,
            surgical_history=record.surgical_history,
            family_history=record.family_history,
            habits=record.habits,
            allergies=record.allergies,
            current_medications=record.current_medications,
            last_diagnoses=record.last_diagnoses,
            tags=record.tags,
            created_at=record.created_at,
            updated_at=record.updated_at
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