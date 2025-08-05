"""
DecisionSupport Use Cases - Casos de uso para gerenciamento de suporte à decisão
Implementa a lógica de aplicação para operações com decision support.
"""
from typing import Optional, List
from uuid import UUID

from ..entities.decision_support import DecisionSupport
from ..repositories.interfaces import IDecisionSupportRepository, IRecordRepository, IVisitRepository


class CreateDecisionSupportUseCase:
    """Caso de uso para criar um novo suporte à decisão"""
    
    def __init__(
        self, 
        decision_support_repository: IDecisionSupportRepository,
        record_repository: IRecordRepository,
        visit_repository: IVisitRepository
    ):
        self._decision_support_repository = decision_support_repository
        self._record_repository = record_repository
        self._visit_repository = visit_repository
    
    async def execute(
        self,
        record_id: UUID,
        visit_id: UUID,
        professional_id: UUID,
        llm_model: str,
        sentiment_summary: Optional[str] = None,
        symptom_summary: Optional[str] = None,
        goal_summary: Optional[str] = None,
        practice_summary: Optional[str] = None,
        insight_summary: Optional[str] = None,
        suggested_conduct: Optional[str] = None,
        evidence_summary: Optional[str] = None
    ) -> DecisionSupport:
        """
        Cria um novo suporte à decisão
        
        Args:
            record_id: ID do prontuário
            visit_id: ID do atendimento
            professional_id: ID do profissional
            llm_model: Modelo LLM utilizado
            sentiment_summary: Resumo de sentimentos
            symptom_summary: Resumo de sintomas
            goal_summary: Resumo de objetivos
            practice_summary: Resumo de práticas
            insight_summary: Resumo de insights
            suggested_conduct: Conduta sugerida
            evidence_summary: Resumo de evidências
            
        Returns:
            DecisionSupport: Suporte à decisão criado
            
        Raises:
            ValueError: Se prontuário, atendimento não existem ou já existe suporte para a visit
        """
        # Verificar se o prontuário existe
        record = await self._record_repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Prontuário {record_id} não encontrado")
        
        # Verificar se o atendimento existe
        visit = await self._visit_repository.get_by_id(visit_id)
        if not visit:
            raise ValueError(f"Atendimento {visit_id} não encontrado")
        
        # Verificar se o atendimento pertence ao prontuário
        if visit.record_id != record_id:
            raise ValueError(f"Atendimento {visit_id} não pertence ao prontuário {record_id}")
        
        # Verificar se já existe suporte à decisão para esta visit (1:1)
        existing_support = await self._decision_support_repository.get_by_visit_id(visit_id)
        if existing_support:
            raise ValueError(f"Já existe suporte à decisão para o atendimento {visit_id}")
        
        # Criar novo suporte à decisão
        decision_support = DecisionSupport(
            record_id=record_id,
            visit_id=visit_id,
            professional_id=professional_id,
            llm_model=llm_model,
            sentiment_summary=sentiment_summary,
            symptom_summary=symptom_summary,
            goal_summary=goal_summary,
            practice_summary=practice_summary,
            insight_summary=insight_summary,
            suggested_conduct=suggested_conduct,
            evidence_summary=evidence_summary
        )
        
        # Persistir no repositório
        return await self._decision_support_repository.create(decision_support)


class GetDecisionSupportByVisitUseCase:
    """Caso de uso para buscar suporte à decisão por atendimento"""
    
    def __init__(self, decision_support_repository: IDecisionSupportRepository):
        self._decision_support_repository = decision_support_repository
    
    async def execute(self, visit_id: UUID) -> Optional[DecisionSupport]:
        """
        Busca suporte à decisão por ID do atendimento
        
        Args:
            visit_id: ID do atendimento
            
        Returns:
            Optional[DecisionSupport]: Suporte à decisão encontrado ou None
        """
        return await self._decision_support_repository.get_by_visit_id(visit_id)
    
    async def execute_by_record(
        self, 
        record_id: UUID, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[DecisionSupport]:
        """
        Busca suportes à decisão de um prontuário com paginação
        
        Args:
            record_id: ID do prontuário
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[DecisionSupport]: Lista de suportes à decisão
        """
        return await self._decision_support_repository.get_by_record_id(record_id, limit, offset)


class UpdateDecisionSupportUseCase:
    """Caso de uso para atualizar um suporte à decisão"""
    
    def __init__(self, decision_support_repository: IDecisionSupportRepository):
        self._decision_support_repository = decision_support_repository
    
    async def execute(
        self,
        decision_support_id: UUID,
        sentiment_summary: Optional[str] = None,
        symptom_summary: Optional[str] = None,
        goal_summary: Optional[str] = None,
        practice_summary: Optional[str] = None,
        insight_summary: Optional[str] = None,
        suggested_conduct: Optional[str] = None,
        evidence_summary: Optional[str] = None
    ) -> DecisionSupport:
        """
        Atualiza dados de um suporte à decisão existente
        
        Args:
            decision_support_id: ID do suporte à decisão
            sentiment_summary: Resumo de sentimentos
            symptom_summary: Resumo de sintomas
            goal_summary: Resumo de objetivos
            practice_summary: Resumo de práticas
            insight_summary: Resumo de insights
            suggested_conduct: Conduta sugerida
            evidence_summary: Resumo de evidências
            
        Returns:
            DecisionSupport: Suporte à decisão atualizado
            
        Raises:
            ValueError: Se o suporte à decisão não existe
        """
        # Buscar suporte à decisão existente
        decision_support = await self._decision_support_repository.get_by_id(decision_support_id)
        if not decision_support:
            raise ValueError(f"Suporte à decisão {decision_support_id} não encontrado")
        
        # Atualizar campos fornecidos
        if sentiment_summary is not None:
            decision_support.update_sentiment_summary(sentiment_summary)
        
        if symptom_summary is not None:
            decision_support.update_symptom_summary(symptom_summary)
        
        if goal_summary is not None:
            decision_support.update_goal_summary(goal_summary)
        
        if practice_summary is not None:
            decision_support.update_practice_summary(practice_summary)
        
        if insight_summary is not None:
            decision_support.update_insight_summary(insight_summary)
        
        if suggested_conduct is not None:
            decision_support.update_suggested_conduct(suggested_conduct)
        
        if evidence_summary is not None:
            decision_support.update_evidence_summary(evidence_summary)
        
        # Persistir alterações
        return await self._decision_support_repository.update(decision_support)