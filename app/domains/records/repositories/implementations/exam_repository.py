"""
Exam Repository Implementation - Implementação concreta do repositório de Exams
Mapeia entidades Exam para SQLAlchemy models e vice-versa.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from ..interfaces import IExamRepository
from ...entities.exam import Exam, ExamType
from ...models.exam_model import ExamModel, ExamTypeEnum


class ExamRepository(IExamRepository):
    """Implementação concreta do repositório de Exams"""
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, exam: Exam) -> Exam:
        """Cria um novo exam no banco de dados"""
        exam_model = ExamModel(
            id=exam.id,
            record_id=exam.record_id,
            visit_id=exam.visit_id,
            type=self._entity_type_to_enum(exam.type),
            name=exam.name,
            requested_at=exam.requested_at,
            result_text=exam.result_text,
            result_file=exam.result_file,
            created_at=exam.created_at
        )
        
        self._db.add(exam_model)
        self._db.commit()
        self._db.refresh(exam_model)
        
        return self._model_to_entity(exam_model)
    
    async def get_by_id(self, exam_id: UUID) -> Optional[Exam]:
        """Busca exam por ID"""
        stmt = select(ExamModel).where(ExamModel.id == exam_id)
        result = self._db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._model_to_entity(model)
        return None
    
    async def get_by_record_id(self, record_id: UUID, limit: int = 50, offset: int = 0) -> List[Exam]:
        """Busca exams por record ID com paginação"""
        stmt = (
            select(ExamModel)
            .where(ExamModel.record_id == record_id)
            .order_by(desc(ExamModel.requested_at))
            .limit(limit)
            .offset(offset)
        )
        result = self._db.execute(stmt)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_visit_id(self, visit_id: UUID) -> List[Exam]:
        """Busca exams por visit ID"""
        stmt = (
            select(ExamModel)
            .where(ExamModel.visit_id == visit_id)
            .order_by(desc(ExamModel.requested_at))
        )
        result = self._db.execute(stmt)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_type(self, record_id: UUID, exam_type: ExamType) -> List[Exam]:
        """Busca exams por tipo"""
        type_enum = self._entity_type_to_enum(exam_type)
        stmt = (
            select(ExamModel)
            .where(ExamModel.record_id == record_id)
            .where(ExamModel.type == type_enum)
            .order_by(desc(ExamModel.requested_at))
        )
        result = self._db.execute(stmt)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, exam: Exam) -> Exam:
        """Atualiza um exam existente"""
        stmt = select(ExamModel).where(ExamModel.id == exam.id)
        result = self._db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Exam {exam.id} não encontrado")
        
        model.result_text = exam.result_text
        model.result_file = exam.result_file
        
        self._db.commit()
        self._db.refresh(model)
        
        return self._model_to_entity(model)
    
    def _model_to_entity(self, model: ExamModel) -> Exam:
        """Converte ExamModel para entidade Exam"""
        return Exam(
            record_id=model.record_id,
            exam_type=self._enum_to_entity_type(model.type),
            name=model.name,
            requested_at=model.requested_at,
            visit_id=model.visit_id,
            result_text=model.result_text,
            result_file=model.result_file,
            exam_id=model.id,
            created_at=model.created_at
        )
    
    def _entity_type_to_enum(self, entity_type: ExamType) -> ExamTypeEnum:
        """Converte ExamType (entidade) para ExamTypeEnum (model)"""
        mapping = {
            ExamType.CLINICAL: ExamTypeEnum.CLINICAL,
            ExamType.LABORATORY: ExamTypeEnum.LABORATORY,
            ExamType.IMAGE: ExamTypeEnum.IMAGE
        }
        return mapping[entity_type]
    
    def _enum_to_entity_type(self, enum_type: ExamTypeEnum) -> ExamType:
        """Converte ExamTypeEnum (model) para ExamType (entidade)"""
        mapping = {
            ExamTypeEnum.CLINICAL: ExamType.CLINICAL,
            ExamTypeEnum.LABORATORY: ExamType.LABORATORY,
            ExamTypeEnum.IMAGE: ExamType.IMAGE
        }
        return mapping[enum_type]