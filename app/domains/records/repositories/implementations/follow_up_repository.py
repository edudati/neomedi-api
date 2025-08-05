"""
FollowUp Repository Implementation - Implementação concreta do repositório de FollowUps
Mapeia entidades FollowUp para SQLAlchemy models e vice-versa.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from ..interfaces import IFollowUpRepository
from ...entities.follow_up import FollowUp
from ...models.follow_up_model import FollowUpModel


class FollowUpRepository(IFollowUpRepository):
    """Implementação concreta do repositório de FollowUps"""
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, follow_up: FollowUp) -> FollowUp:
        """Cria um novo follow-up no banco de dados"""
        follow_up_model = FollowUpModel(
            id=follow_up.id,
            record_id=follow_up.record_id,
            visit_id=follow_up.visit_id,
            note=follow_up.note,
            tags=follow_up.tags,
            created_at=follow_up.created_at
        )
        
        self._db.add(follow_up_model)
        self._db.commit()
        self._db.refresh(follow_up_model)
        
        return self._model_to_entity(follow_up_model)
    
    async def get_by_id(self, follow_up_id: UUID) -> Optional[FollowUp]:
        """Busca follow-up por ID"""
        stmt = select(FollowUpModel).where(FollowUpModel.id == follow_up_id)
        result = self._db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._model_to_entity(model)
        return None
    
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[FollowUp]:
        """Busca follow-ups por record ID com paginação"""
        stmt = (
            select(FollowUpModel)
            .where(FollowUpModel.record_id == record_id)
            .order_by(desc(FollowUpModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = self._db.execute(stmt)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_visit_id(self, visit_id: UUID) -> List[FollowUp]:
        """Busca follow-ups por visit ID"""
        stmt = (
            select(FollowUpModel)
            .where(FollowUpModel.visit_id == visit_id)
            .order_by(desc(FollowUpModel.created_at))
        )
        result = self._db.execute(stmt)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, follow_up: FollowUp) -> FollowUp:
        """Atualiza um follow-up existente"""
        stmt = select(FollowUpModel).where(FollowUpModel.id == follow_up.id)
        result = self._db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"FollowUp {follow_up.id} não encontrado")
        
        model.note = follow_up.note
        model.tags = follow_up.tags
        
        self._db.commit()
        self._db.refresh(model)
        
        return self._model_to_entity(model)
    
    def _model_to_entity(self, model: FollowUpModel) -> FollowUp:
        """Converte FollowUpModel para entidade FollowUp"""
        return FollowUp(
            record_id=model.record_id,
            note=model.note,
            visit_id=model.visit_id,
            tags=model.tags or [],
            follow_up_id=model.id,
            created_at=model.created_at
        )