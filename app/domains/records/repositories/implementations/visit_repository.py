"""
Visit Repository Implementation - Implementação concreta do repositório de Visits
Mapeia entidades Visit para SQLAlchemy models e vice-versa.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from ..interfaces import IVisitRepository
from ...entities.visit import Visit
from ...models.visit_model import VisitModel


class VisitRepository(IVisitRepository):
    """
    Implementação concreta do repositório de Visits
    
    Converte entre entidades Visit (domínio) e VisitModel (infraestrutura).
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, visit: Visit) -> Visit:
        """Cria uma nova visit no banco de dados"""
        visit_model = VisitModel(
            id=visit.id,
            record_id=visit.record_id,
            professional_id=visit.professional_id,
            company_id=visit.company_id,
            main_complaint=visit.main_complaint,
            current_illness_history=visit.current_illness_history,
            past_history=visit.past_history,
            physical_exam=visit.physical_exam,
            diagnostic_hypothesis=visit.diagnostic_hypothesis,
            procedures=visit.procedures,
            prescription=visit.prescription,
            created_at=visit.created_at,
            updated_at=visit.updated_at
        )
        
        self._db.add(visit_model)
        self._db.commit()
        self._db.refresh(visit_model)
        
        return self._model_to_entity(visit_model)
    
    async def get_by_id(self, visit_id: UUID) -> Optional[Visit]:
        """Busca visit por ID"""
        stmt = select(VisitModel).where(VisitModel.id == visit_id)
        result = self._db.execute(stmt)
        visit_model = result.scalar_one_or_none()
        
        if visit_model:
            return self._model_to_entity(visit_model)
        return None
    
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[Visit]:
        """Busca visits por record ID com paginação"""
        stmt = (
            select(VisitModel)
            .where(VisitModel.record_id == record_id)
            .order_by(desc(VisitModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = self._db.execute(stmt)
        visit_models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in visit_models]
    
    async def update(self, visit: Visit) -> Visit:
        """Atualiza uma visit existente"""
        stmt = select(VisitModel).where(VisitModel.id == visit.id)
        result = self._db.execute(stmt)
        visit_model = result.scalar_one_or_none()
        
        if not visit_model:
            raise ValueError(f"Visit {visit.id} não encontrada")
        
        # Atualizar campos
        visit_model.main_complaint = visit.main_complaint
        visit_model.current_illness_history = visit.current_illness_history
        visit_model.past_history = visit.past_history
        visit_model.physical_exam = visit.physical_exam
        visit_model.diagnostic_hypothesis = visit.diagnostic_hypothesis
        visit_model.procedures = visit.procedures
        visit_model.prescription = visit.prescription
        visit_model.updated_at = visit.updated_at
        
        self._db.commit()
        self._db.refresh(visit_model)
        
        return self._model_to_entity(visit_model)
    
    async def get_latest_by_record_id(self, record_id: UUID) -> Optional[Visit]:
        """Busca a última visit de um record"""
        stmt = (
            select(VisitModel)
            .where(VisitModel.record_id == record_id)
            .order_by(desc(VisitModel.created_at))
            .limit(1)
        )
        result = self._db.execute(stmt)
        visit_model = result.scalar_one_or_none()
        
        if visit_model:
            return self._model_to_entity(visit_model)
        return None
    
    def _model_to_entity(self, model: VisitModel) -> Visit:
        """Converte VisitModel para entidade Visit"""
        return Visit(
            record_id=model.record_id,
            professional_id=model.professional_id,
            company_id=model.company_id,
            main_complaint=model.main_complaint,
            current_illness_history=model.current_illness_history,
            past_history=model.past_history,
            physical_exam=model.physical_exam,
            diagnostic_hypothesis=model.diagnostic_hypothesis,
            procedures=model.procedures,
            prescription=model.prescription,
            visit_id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )