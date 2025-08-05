"""
DecisionSupport Model - SQLAlchemy Model para Suporte à Decisão
Mapeia a entidade DecisionSupport para tabela do banco de dados.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base


class DecisionSupportModel(Base):
    """
    Modelo SQLAlchemy para DecisionSupport (Suporte à Decisão)
    
    Representa a tabela decision_supports no banco de dados.
    Mapeia a entidade DecisionSupport para persistência.
    """
    __tablename__ = "decision_supports"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    record_id = Column(UUID(as_uuid=True), ForeignKey("records.id"), nullable=False, index=True)
    visit_id = Column(UUID(as_uuid=True), ForeignKey("visits.id"), nullable=False, unique=True, index=True)
    professional_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # LLM Analysis Summaries
    sentiment_summary = Column(String, nullable=True)
    symptom_summary = Column(String, nullable=True)
    goal_summary = Column(String, nullable=True)
    practice_summary = Column(String, nullable=True)
    insight_summary = Column(String, nullable=True)
    
    # LLM Suggestions
    suggested_conduct = Column(String, nullable=True)
    evidence_summary = Column(String, nullable=True)
    
    # LLM Metadata
    llm_model = Column(String, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    record = relationship("RecordModel", back_populates="decision_supports")
    visit = relationship("VisitModel", back_populates="decision_support")
    # professional = relationship("User", back_populates="decision_supports")
    
    def __repr__(self):
        return f"<DecisionSupportModel(id={self.id}, visit_id={self.visit_id}, model='{self.llm_model}')>"