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
    - **professional_id**: ID do profissional criador (obrigatório)
    - **company_id**: ID da clínica (opcional)
    - Outros campos clínicos opcionais
    """
    try:
        # Usar o use case para criar o record
        use_case = CreateRecordUseCase(record_repo)
        record = await use_case.execute(
            patient_id=request.patient_id,
            professional_id=request.professional_id,
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


@router.get("/patient/{patient_id}", response_model=RecordResponse)
async def get_record_by_patient(
    patient_id: UUID,
    current_user: dict = Depends(get_current_user),
    record_repo: RecordRepository = Depends(get_record_repository)
):
    """
    Busca prontuário por ID do paciente
    
    - **patient_id**: ID do paciente
    """
    try:
        use_case = GetRecordUseCase(record_repo)
        record = await use_case.execute_by_patient_id(patient_id)
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prontuário para paciente {patient_id} não encontrado"
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