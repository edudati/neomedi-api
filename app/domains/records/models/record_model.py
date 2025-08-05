"""
Record Model - SQLAlchemy Model para Prontuários
Mapeia a entidade Record para tabela do banco de dados.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base


class RecordModel(Base):
    """
    Modelo SQLAlchemy para Records (Prontuários)
    
    Representa a tabela records no banco de dados.
    Mapeia a entidade Record para persistência.
    """
    __tablename__ = "records"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    professional_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    
    # Clinical Data
    clinical_history = Column(String, nullable=True, default="")
    surgical_history = Column(String, nullable=True, default="")
    family_history = Column(String, nullable=True, default="")
    habits = Column(String, nullable=True, default="")
    allergies = Column(String, nullable=True, default="")
    current_medications = Column(String, nullable=True, default="")
    last_diagnoses = Column(String, nullable=True, default="")
    
    # Tags (JSON array)
    tags = Column(JSONB, nullable=True, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    # patient = relationship("User", foreign_keys=[patient_id], back_populates="patient_records")
    # professional = relationship("User", foreign_keys=[professional_id], back_populates="professional_records")
    # company = relationship("Company", back_populates="records")
    
    # Child relationships
    visits = relationship("VisitModel", back_populates="record", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUpModel", back_populates="record", cascade="all, delete-orphan")
    exams = relationship("ExamModel", back_populates="record", cascade="all, delete-orphan")
    decision_supports = relationship("DecisionSupportModel", back_populates="record", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<RecordModel(id={self.id}, patient_id={self.patient_id})>"