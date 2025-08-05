"""
Visit Model - SQLAlchemy Model para Atendimentos
Mapeia a entidade Visit para tabela do banco de dados.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base


class VisitModel(Base):
    """
    Modelo SQLAlchemy para Visits (Atendimentos)
    
    Representa a tabela visits no banco de dados.
    Mapeia a entidade Visit para persistência.
    """
    __tablename__ = "visits"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    record_id = Column(UUID(as_uuid=True), ForeignKey("records.id"), nullable=False, index=True)
    professional_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    
    # Clinical Data
    main_complaint = Column(String, nullable=True, default="")
    current_illness_history = Column(String, nullable=True, default="")
    past_history = Column(String, nullable=True, default="")
    physical_exam = Column(String, nullable=True, default="")
    diagnostic_hypothesis = Column(String, nullable=True, default="")
    procedures = Column(String, nullable=True, default="")
    prescription = Column(String, nullable=True, default="")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    record = relationship("RecordModel", back_populates="visits")
    # professional = relationship("User", back_populates="visits")
    # company = relationship("Company", back_populates="visits")
    
    # Child relationships
    follow_ups = relationship("FollowUpModel", back_populates="visit", cascade="all, delete-orphan")
    exams = relationship("ExamModel", back_populates="visit", cascade="all, delete-orphan")
    decision_support = relationship("DecisionSupportModel", back_populates="visit", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<VisitModel(id={self.id}, record_id={self.record_id})>"