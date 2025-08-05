"""
Record Use Cases - Casos de uso para gerenciamento de prontuários
Implementa a lógica de aplicação para operações com records.
"""
from typing import Optional, List
from uuid import UUID

from ..entities.record import Record
from ..repositories.interfaces import IRecordRepository


class CreateRecordUseCase:
    """Caso de uso para criar um novo prontuário"""
    
    def __init__(self, record_repository: IRecordRepository):
        self._record_repository = record_repository
    
    async def execute(
        self,
        patient_id: UUID,
        professional_id: UUID,
        company_id: Optional[UUID] = None,
        clinical_history: Optional[str] = None,
        surgical_history: Optional[str] = None,
        family_history: Optional[str] = None,
        habits: Optional[str] = None,
        allergies: Optional[str] = None,
        current_medications: Optional[str] = None,
        last_diagnoses: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Record:
        """
        Cria um novo prontuário para um paciente
        
        Args:
            patient_id: ID do paciente
            professional_id: ID do profissional criador
            company_id: ID da clínica (opcional)
            clinical_history: Histórico clínico
            surgical_history: Histórico cirúrgico
            family_history: Histórico familiar
            habits: Hábitos do paciente
            allergies: Alergias
            current_medications: Medicamentos em uso
            last_diagnoses: Últimos diagnósticos
            tags: Tags de classificação
            
        Returns:
            Record: Prontuário criado
        """
        # Remover validação para permitir múltiplos prontuários por paciente
        
        # Criar novo prontuário
        record = Record(
            patient_id=patient_id,
            professional_id=professional_id,
            company_id=company_id,
            clinical_history=clinical_history,
            surgical_history=surgical_history,
            family_history=family_history,
            habits=habits,
            allergies=allergies,
            current_medications=current_medications,
            last_diagnoses=last_diagnoses,
            tags=tags
        )
        
        # Persistir no repositório
        return await self._record_repository.create(record)


class GetRecordUseCase:
    """Caso de uso para buscar um prontuário"""
    
    def __init__(self, record_repository: IRecordRepository):
        self._record_repository = record_repository
    
    async def execute_by_id(self, record_id: UUID) -> Optional[Record]:
        """
        Busca prontuário por ID
        
        Args:
            record_id: ID do prontuário
            
        Returns:
            Optional[Record]: Prontuário encontrado ou None
        """
        return await self._record_repository.get_by_id(record_id)
    
    async def execute_by_patient_id(self, patient_id: UUID, skip: int = 0, limit: int = 100) -> List[Record]:
        """
        Busca prontuários por ID do paciente com paginação
        
        Args:
            patient_id: ID do paciente
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Record]: Lista de prontuários encontrados
        """
        return await self._record_repository.get_by_patient_id(patient_id, skip, limit)


class UpdateRecordUseCase:
    """Caso de uso para atualizar um prontuário"""
    
    def __init__(self, record_repository: IRecordRepository):
        self._record_repository = record_repository
    
    async def execute(
        self,
        record_id: UUID,
        clinical_history: Optional[str] = None,
        surgical_history: Optional[str] = None,
        family_history: Optional[str] = None,
        habits: Optional[str] = None,
        allergies: Optional[str] = None,
        current_medications: Optional[str] = None,
        last_diagnoses: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Record:
        """
        Atualiza dados de um prontuário existente
        
        Args:
            record_id: ID do prontuário
            clinical_history: Histórico clínico
            surgical_history: Histórico cirúrgico
            family_history: Histórico familiar
            habits: Hábitos do paciente
            allergies: Alergias
            current_medications: Medicamentos em uso
            last_diagnoses: Últimos diagnósticos
            tags: Tags de classificação
            
        Returns:
            Record: Prontuário atualizado
            
        Raises:
            ValueError: Se o prontuário não existe
        """
        # Buscar prontuário existente
        record = await self._record_repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Prontuário {record_id} não encontrado")
        
        # Atualizar campos fornecidos
        if clinical_history is not None:
            record.update_clinical_history(clinical_history)
        
        if surgical_history is not None:
            record.update_surgical_history(surgical_history)
        
        if family_history is not None:
            record.update_family_history(family_history)
        
        if habits is not None:
            record.update_habits(habits)
        
        if allergies is not None:
            record.update_allergies(allergies)
        
        if current_medications is not None:
            record.update_current_medications(current_medications)
        
        if last_diagnoses is not None:
            record.update_last_diagnoses(last_diagnoses)
        
        if tags is not None:
            record.update_tags(tags)
        
        # Persistir alterações
        return await self._record_repository.update(record)