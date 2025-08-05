"""
FollowUp Use Cases - Casos de uso para gerenciamento de evoluções rápidas
Implementa a lógica de aplicação para operações com follow-ups.
"""
from typing import Optional, List
from uuid import UUID

from ..entities.follow_up import FollowUp
from ..repositories.interfaces import IFollowUpRepository, IRecordRepository, IVisitRepository


class CreateFollowUpUseCase:
    """Caso de uso para criar uma nova evolução rápida"""
    
    def __init__(
        self, 
        follow_up_repository: IFollowUpRepository,
        record_repository: IRecordRepository,
        visit_repository: IVisitRepository
    ):
        self._follow_up_repository = follow_up_repository
        self._record_repository = record_repository
        self._visit_repository = visit_repository
    
    async def execute(
        self,
        record_id: UUID,
        note: str,
        visit_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None
    ) -> FollowUp:
        """
        Cria uma nova evolução rápida
        
        Args:
            record_id: ID do prontuário
            note: Nota da evolução (obrigatória)
            visit_id: ID do atendimento (opcional)
            tags: Tags de categorização
            
        Returns:
            FollowUp: Evolução criada
            
        Raises:
            ValueError: Se o prontuário não existe ou visit_id inválido
        """
        # Verificar se o prontuário existe
        record = await self._record_repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Prontuário {record_id} não encontrado")
        
        # Verificar se visit_id existe (se fornecido)
        if visit_id:
            visit = await self._visit_repository.get_by_id(visit_id)
            if not visit:
                raise ValueError(f"Atendimento {visit_id} não encontrado")
            # Verificar se o atendimento pertence ao mesmo prontuário
            if visit.record_id != record_id:
                raise ValueError(f"Atendimento {visit_id} não pertence ao prontuário {record_id}")
        
        # Criar nova evolução
        follow_up = FollowUp(
            record_id=record_id,
            note=note,
            visit_id=visit_id,
            tags=tags
        )
        
        # Persistir no repositório
        return await self._follow_up_repository.create(follow_up)


class GetFollowUpsByRecordUseCase:
    """Caso de uso para buscar evoluções de um prontuário"""
    
    def __init__(self, follow_up_repository: IFollowUpRepository):
        self._follow_up_repository = follow_up_repository
    
    async def execute(
        self, 
        record_id: UUID, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[FollowUp]:
        """
        Busca evoluções de um prontuário com paginação
        
        Args:
            record_id: ID do prontuário
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[FollowUp]: Lista de evoluções
        """
        return await self._follow_up_repository.get_by_record_id(record_id, limit, offset)
    
    async def execute_by_visit(self, visit_id: UUID) -> List[FollowUp]:
        """
        Busca evoluções vinculadas a um atendimento
        
        Args:
            visit_id: ID do atendimento
            
        Returns:
            List[FollowUp]: Lista de evoluções do atendimento
        """
        return await self._follow_up_repository.get_by_visit_id(visit_id)


class UpdateFollowUpUseCase:
    """Caso de uso para atualizar uma evolução rápida"""
    
    def __init__(self, follow_up_repository: IFollowUpRepository):
        self._follow_up_repository = follow_up_repository
    
    async def execute(
        self,
        follow_up_id: UUID,
        note: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> FollowUp:
        """
        Atualiza dados de uma evolução existente
        
        Args:
            follow_up_id: ID da evolução
            note: Nova nota
            tags: Novas tags
            
        Returns:
            FollowUp: Evolução atualizada
            
        Raises:
            ValueError: Se a evolução não existe
        """
        # Buscar evolução existente
        follow_up = await self._follow_up_repository.get_by_id(follow_up_id)
        if not follow_up:
            raise ValueError(f"Evolução {follow_up_id} não encontrada")
        
        # Atualizar campos fornecidos
        if note is not None:
            follow_up.update_note(note)
        
        if tags is not None:
            follow_up.update_tags(tags)
        
        # Persistir alterações
        return await self._follow_up_repository.update(follow_up)