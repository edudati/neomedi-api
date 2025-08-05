"""
DecisionSupport Repository Implementation - Implementação concreta do repositório de DecisionSupport
Mapeia entidades DecisionSupport para SQLAlchemy models e vice-versa.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from ..interfaces import IDecisionSupportRepository
from ...entities.decision_support import DecisionSupport
from ...models.decision_support_model import DecisionSupportModel


class DecisionSupportRepository(IDecisionSupportRepository):
    """Implementação concreta do repositório de DecisionSupport"""
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, decision_support: DecisionSupport) -> DecisionSupport:
        """Cria um novo decision support no banco de dados"""
        model = DecisionSupportModel(
            id=decision_support.id,
            record_id=decision_support.record_id,
            visit_id=decision_support.visit_id,
            professional_id=decision_support.professional_id,
            sentiment_summary=decision_support.sentiment_summary,
            symptom_summary=decision_support.symptom_summary,
            goal_summary=decision_support.goal_summary,
            practice_summary=decision_support.practice_summary,
            insight_summary=decision_support.insight_summary,
            suggested_conduct=decision_support.suggested_conduct,
            evidence_summary=decision_support.evidence_summary,
            llm_model=decision_support.llm_model,
            created_at=decision_support.created_at
        )
        
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        
        return self._model_to_entity(model)
    
    async def get_by_id(self, decision_support_id: UUID) -> Optional[DecisionSupport]:
        """Busca decision support por ID"""
        stmt = select(DecisionSupportModel).where(DecisionSupportModel.id == decision_support_id)
        result = self._db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._model_to_entity(model)
        return None
    
    async def get_by_visit_id(self, visit_id: UUID) -> Optional[DecisionSupport]:
        """Busca decision support por visit ID"""
        stmt = select(DecisionSupportModel).where(DecisionSupportModel.visit_id == visit_id)
        result = self._db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._model_to_entity(model)
        return None
    
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[DecisionSupport]:
        """Busca decision supports por record ID com paginação"""
        stmt = (
            select(DecisionSupportModel)
            .where(DecisionSupportModel.record_id == record_id)
            .order_by(desc(DecisionSupportModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = self._db.execute(stmt)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, decision_support: DecisionSupport) -> DecisionSupport:
        """Atualiza um decision support existente"""
        stmt = select(DecisionSupportModel).where(DecisionSupportModel.id == decision_support.id)
        result = self._db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"DecisionSupport {decision_support.id} não encontrado")
        
        # Atualizar campos
        model.sentiment_summary = decision_support.sentiment_summary
        model.symptom_summary = decision_support.symptom_summary
        model.goal_summary = decision_support.goal_summary
        model.practice_summary = decision_support.practice_summary
        model.insight_summary = decision_support.insight_summary
        model.suggested_conduct = decision_support.suggested_conduct
        model.evidence_summary = decision_support.evidence_summary
        
        self._db.commit()
        self._db.refresh(model)
        
        return self._model_to_entity(model)
    
    def _model_to_entity(self, model: DecisionSupportModel) -> DecisionSupport:
        """Converte DecisionSupportModel para entidade DecisionSupport"""
        return DecisionSupport(
            record_id=model.record_id,
            visit_id=model.visit_id,
            professional_id=model.professional_id,
            llm_model=model.llm_model,
            sentiment_summary=model.sentiment_summary,
            symptom_summary=model.symptom_summary,
            goal_summary=model.goal_summary,
            practice_summary=model.practice_summary,
            insight_summary=model.insight_summary,
            suggested_conduct=model.suggested_conduct,
            evidence_summary=model.evidence_summary,
            decision_support_id=model.id,
            created_at=model.created_at
        )