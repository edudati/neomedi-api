"""
Record Repository Implementation - Implementação concreta do repositório de Records
Mapeia entidades Record para SQLAlchemy models e vice-versa.
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..interfaces import IRecordRepository
from ...entities.record import Record
from ...models.record_model import RecordModel


class RecordRepository(IRecordRepository):
    """
    Implementação concreta do repositório de Records
    
    Converte entre entidades Record (domínio) e RecordModel (infraestrutura).
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, record: Record) -> Record:
        """Cria um novo record no banco de dados"""
        # Converter entidade para model
        record_model = RecordModel(
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
        
        # Persistir no banco
        self._db.add(record_model)
        self._db.commit()
        self._db.refresh(record_model)
        
        # Converter model para entidade
        return self._model_to_entity(record_model)
    
    async def get_by_id(self, record_id: UUID) -> Optional[Record]:
        """Busca record por ID"""
        stmt = select(RecordModel).where(RecordModel.id == record_id)
        result = self._db.execute(stmt)
        record_model = result.scalar_one_or_none()
        
        if record_model:
            return self._model_to_entity(record_model)
        return None
    
    async def get_by_patient_id(self, patient_id: UUID, skip: int = 0, limit: int = 100) -> List[Record]:
        """Busca records por ID do paciente com paginação"""
        stmt = select(RecordModel).where(RecordModel.patient_id == patient_id).offset(skip).limit(limit).order_by(RecordModel.created_at.desc())
        result = self._db.execute(stmt)
        record_models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in record_models]
    
    async def update(self, record: Record) -> Record:
        """Atualiza um record existente"""
        stmt = select(RecordModel).where(RecordModel.id == record.id)
        result = self._db.execute(stmt)
        record_model = result.scalar_one_or_none()
        
        if not record_model:
            raise ValueError(f"Record {record.id} não encontrado")
        
        # Atualizar campos do model
        record_model.clinical_history = record.clinical_history
        record_model.surgical_history = record.surgical_history
        record_model.family_history = record.family_history
        record_model.habits = record.habits
        record_model.allergies = record.allergies
        record_model.current_medications = record.current_medications
        record_model.last_diagnoses = record.last_diagnoses
        record_model.tags = record.tags
        record_model.updated_at = record.updated_at
        
        # Persistir mudanças
        self._db.commit()
        self._db.refresh(record_model)
        
        # Converter model para entidade
        return self._model_to_entity(record_model)
    
    async def exists_for_patient(self, patient_id: UUID) -> bool:
        """Verifica se já existe record para o paciente"""
        stmt = select(RecordModel.id).where(RecordModel.patient_id == patient_id)
        result = self._db.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    def _model_to_entity(self, model: RecordModel) -> Record:
        """Converte RecordModel para entidade Record"""
        return Record(
            patient_id=model.patient_id,
            professional_id=model.professional_id,
            company_id=model.company_id,
            clinical_history=model.clinical_history,
            surgical_history=model.surgical_history,
            family_history=model.family_history,
            habits=model.habits,
            allergies=model.allergies,
            current_medications=model.current_medications,
            last_diagnoses=model.last_diagnoses,
            tags=model.tags or [],
            record_id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )