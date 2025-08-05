"""
Visit Use Cases - Casos de uso para gerenciamento de atendimentos
Implementa a lógica de aplicação para operações com visits.
"""
from typing import Optional, List
from uuid import UUID

from ..entities.visit import Visit
from ..repositories.interfaces import IVisitRepository, IRecordRepository


class CreateVisitUseCase:
    """Caso de uso para criar um novo atendimento"""
    
    def __init__(
        self, 
        visit_repository: IVisitRepository,
        record_repository: IRecordRepository
    ):
        self._visit_repository = visit_repository
        self._record_repository = record_repository
    
    async def execute(
        self,
        record_id: UUID,
        professional_id: UUID,
        company_id: Optional[UUID] = None,
        main_complaint: Optional[str] = None,
        current_illness_history: Optional[str] = None,
        past_history: Optional[str] = None,
        physical_exam: Optional[str] = None,
        diagnostic_hypothesis: Optional[str] = None,
        procedures: Optional[str] = None,
        prescription: Optional[str] = None
    ) -> Visit:
        """
        Cria um novo atendimento
        
        Args:
            record_id: ID do prontuário
            professional_id: ID do profissional
            company_id: ID da clínica (opcional)
            main_complaint: Queixa principal
            current_illness_history: História da moléstia atual
            past_history: Histórico e antecedentes
            physical_exam: Exame físico
            diagnostic_hypothesis: Hipótese diagnóstica
            procedures: Condutas aplicadas
            prescription: Prescrição/recomendações
            
        Returns:
            Visit: Atendimento criado
            
        Raises:
            ValueError: Se o prontuário não existe
        """
        # Verificar se o prontuário existe
        record = await self._record_repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Prontuário {record_id} não encontrado")
        
        # Criar novo atendimento
        visit = Visit(
            record_id=record_id,
            professional_id=professional_id,
            company_id=company_id,
            main_complaint=main_complaint,
            current_illness_history=current_illness_history,
            past_history=past_history,
            physical_exam=physical_exam,
            diagnostic_hypothesis=diagnostic_hypothesis,
            procedures=procedures,
            prescription=prescription
        )
        
        # Persistir no repositório
        return await self._visit_repository.create(visit)


class GetVisitUseCase:
    """Caso de uso para buscar um atendimento"""
    
    def __init__(self, visit_repository: IVisitRepository):
        self._visit_repository = visit_repository
    
    async def execute(self, visit_id: UUID) -> Optional[Visit]:
        """
        Busca atendimento por ID
        
        Args:
            visit_id: ID do atendimento
            
        Returns:
            Optional[Visit]: Atendimento encontrado ou None
        """
        return await self._visit_repository.get_by_id(visit_id)


class GetVisitsByRecordUseCase:
    """Caso de uso para buscar atendimentos de um prontuário"""
    
    def __init__(self, visit_repository: IVisitRepository):
        self._visit_repository = visit_repository
    
    async def execute(
        self, 
        record_id: UUID, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[Visit]:
        """
        Busca atendimentos de um prontuário com paginação
        
        Args:
            record_id: ID do prontuário
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[Visit]: Lista de atendimentos
        """
        return await self._visit_repository.get_by_record_id(record_id, limit, offset)
    
    async def execute_latest(self, record_id: UUID) -> Optional[Visit]:
        """
        Busca o último atendimento de um prontuário
        
        Args:
            record_id: ID do prontuário
            
        Returns:
            Optional[Visit]: Último atendimento ou None
        """
        return await self._visit_repository.get_latest_by_record_id(record_id)


class UpdateVisitUseCase:
    """Caso de uso para atualizar um atendimento"""
    
    def __init__(self, visit_repository: IVisitRepository):
        self._visit_repository = visit_repository
    
    async def execute(
        self,
        visit_id: UUID,
        main_complaint: Optional[str] = None,
        current_illness_history: Optional[str] = None,
        past_history: Optional[str] = None,
        physical_exam: Optional[str] = None,
        diagnostic_hypothesis: Optional[str] = None,
        procedures: Optional[str] = None,
        prescription: Optional[str] = None
    ) -> Visit:
        """
        Atualiza dados de um atendimento existente
        
        Args:
            visit_id: ID do atendimento
            main_complaint: Queixa principal
            current_illness_history: História da moléstia atual
            past_history: Histórico e antecedentes
            physical_exam: Exame físico
            diagnostic_hypothesis: Hipótese diagnóstica
            procedures: Condutas aplicadas
            prescription: Prescrição/recomendações
            
        Returns:
            Visit: Atendimento atualizado
            
        Raises:
            ValueError: Se o atendimento não existe
        """
        # Buscar atendimento existente
        visit = await self._visit_repository.get_by_id(visit_id)
        if not visit:
            raise ValueError(f"Atendimento {visit_id} não encontrado")
        
        # Atualizar campos fornecidos
        if main_complaint is not None:
            visit.update_main_complaint(main_complaint)
        
        if current_illness_history is not None:
            visit.update_current_illness_history(current_illness_history)
        
        if past_history is not None:
            visit.update_past_history(past_history)
        
        if physical_exam is not None:
            visit.update_physical_exam(physical_exam)
        
        if diagnostic_hypothesis is not None:
            visit.update_diagnostic_hypothesis(diagnostic_hypothesis)
        
        if procedures is not None:
            visit.update_procedures(procedures)
        
        if prescription is not None:
            visit.update_prescription(prescription)
        
        # Persistir alterações
        return await self._visit_repository.update(visit)