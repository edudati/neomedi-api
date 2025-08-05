"""
Exam Use Cases - Casos de uso para gerenciamento de exames
Implementa a lógica de aplicação para operações com exams.
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from ..entities.exam import Exam, ExamType
from ..repositories.interfaces import IExamRepository, IRecordRepository, IVisitRepository


class CreateExamUseCase:
    """Caso de uso para criar um novo exame"""
    
    def __init__(
        self, 
        exam_repository: IExamRepository,
        record_repository: IRecordRepository,
        visit_repository: IVisitRepository
    ):
        self._exam_repository = exam_repository
        self._record_repository = record_repository
        self._visit_repository = visit_repository
    
    async def execute(
        self,
        record_id: UUID,
        exam_type: ExamType,
        name: str,
        requested_at: datetime,
        visit_id: Optional[UUID] = None,
        result_text: Optional[str] = None,
        result_file: Optional[str] = None
    ) -> Exam:
        """
        Cria um novo exame
        
        Args:
            record_id: ID do prontuário
            exam_type: Tipo do exame
            name: Nome do exame
            requested_at: Data de solicitação
            visit_id: ID do atendimento (opcional)
            result_text: Resultado em texto
            result_file: Arquivo de resultado
            
        Returns:
            Exam: Exame criado
            
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
        
        # Criar novo exame
        exam = Exam(
            record_id=record_id,
            exam_type=exam_type,
            name=name,
            requested_at=requested_at,
            visit_id=visit_id,
            result_text=result_text,
            result_file=result_file
        )
        
        # Persistir no repositório
        return await self._exam_repository.create(exam)


class GetExamsByRecordUseCase:
    """Caso de uso para buscar exames de um prontuário"""
    
    def __init__(self, exam_repository: IExamRepository):
        self._exam_repository = exam_repository
    
    async def execute(
        self, 
        record_id: UUID, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[Exam]:
        """
        Busca exames de um prontuário com paginação
        
        Args:
            record_id: ID do prontuário
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[Exam]: Lista de exames
        """
        return await self._exam_repository.get_by_record_id(record_id, limit, offset)
    
    async def execute_by_visit(self, visit_id: UUID) -> List[Exam]:
        """
        Busca exames vinculados a um atendimento
        
        Args:
            visit_id: ID do atendimento
            
        Returns:
            List[Exam]: Lista de exames do atendimento
        """
        return await self._exam_repository.get_by_visit_id(visit_id)
    
    async def execute_by_type(self, record_id: UUID, exam_type: ExamType) -> List[Exam]:
        """
        Busca exames por tipo
        
        Args:
            record_id: ID do prontuário
            exam_type: Tipo de exame
            
        Returns:
            List[Exam]: Lista de exames do tipo especificado
        """
        return await self._exam_repository.get_by_type(record_id, exam_type)


class UpdateExamResultsUseCase:
    """Caso de uso para atualizar resultados de um exame"""
    
    def __init__(self, exam_repository: IExamRepository):
        self._exam_repository = exam_repository
    
    async def execute(
        self,
        exam_id: UUID,
        result_text: Optional[str] = None,
        result_file: Optional[str] = None
    ) -> Exam:
        """
        Atualiza resultados de um exame existente
        
        Args:
            exam_id: ID do exame
            result_text: Resultado em texto
            result_file: Arquivo de resultado
            
        Returns:
            Exam: Exame atualizado
            
        Raises:
            ValueError: Se o exame não existe
        """
        # Buscar exame existente
        exam = await self._exam_repository.get_by_id(exam_id)
        if not exam:
            raise ValueError(f"Exame {exam_id} não encontrado")
        
        # Atualizar resultados
        if result_text is not None or result_file is not None:
            exam.add_results(result_text, result_file)
        
        # Persistir alterações
        return await self._exam_repository.update(exam)