"""
Exam Model - SQLAlchemy Model para Exames
Mapeia a entidade Exam para tabela do banco de dados.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.db.database import Base


class ExamTypeEnum(enum.Enum):
    """Enum para tipos de exame no banco de dados"""
    CLINICAL = "clinical"
    LABORATORY = "laboratory"
    IMAGE = "image"


class ExamModel(Base):
    """
    Modelo SQLAlchemy para Exams (Exames)
    
    Representa a tabela exams no banco de dados.
    Mapeia a entidade Exam para persistência.
    """
    __tablename__ = "exams"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    record_id = Column(UUID(as_uuid=True), ForeignKey("records.id"), nullable=False, index=True)
    visit_id = Column(UUID(as_uuid=True), ForeignKey("visits.id"), nullable=True, index=True)
    
    # Exam Data
    type = Column(Enum(ExamTypeEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=False, index=True)
    name = Column(String, nullable=False)
    requested_at = Column(DateTime(timezone=True), nullable=False)
    
    # Results
    result_text = Column(String, nullable=True)
    result_file = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    record = relationship("RecordModel", back_populates="exams")
    visit = relationship("VisitModel", back_populates="exams")
    
    def __repr__(self):
        return f"<ExamModel(id={self.id}, name='{self.name}', type={self.type.value})>"