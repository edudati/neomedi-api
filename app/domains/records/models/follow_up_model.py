"""
FollowUp Model - SQLAlchemy Model para Evoluções Rápidas
Mapeia a entidade FollowUp para tabela do banco de dados.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base


class FollowUpModel(Base):
    """
    Modelo SQLAlchemy para FollowUps (Evoluções Rápidas)
    
    Representa a tabela follow_ups no banco de dados.
    Mapeia a entidade FollowUp para persistência.
    """
    __tablename__ = "follow_ups"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    record_id = Column(UUID(as_uuid=True), ForeignKey("records.id"), nullable=False, index=True)
    visit_id = Column(UUID(as_uuid=True), ForeignKey("visits.id"), nullable=True, index=True)
    
    # Data
    note = Column(String, nullable=False)
    tags = Column(JSONB, nullable=True, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    record = relationship("RecordModel", back_populates="follow_ups")
    visit = relationship("VisitModel", back_populates="follow_ups")
    
    def __repr__(self):
        return f"<FollowUpModel(id={self.id}, record_id={self.record_id})>"