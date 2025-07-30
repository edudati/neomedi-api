from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base

class UserAssistant(Base):
    """Modelo para assistentes de usuários"""
    __tablename__ = "user_assistants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="assistant")
    assistant_clinics = relationship("AssistantClinic", back_populates="assistant")
    assistant_professionals = relationship("AssistantProfessional", back_populates="assistant")

    def __repr__(self):
        return f"<UserAssistant(id={self.id}, user_id={self.user_id})>"

class AssistantClinic(Base):
    """Tabela auxiliar para relacionar assistentes com clínicas"""
    __tablename__ = "assistant_clinics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    assistant_id = Column(UUID(as_uuid=True), ForeignKey("user_assistants.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    is_admin = Column(Boolean, default=False)  # Permissão de administração para a clínica
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    assistant = relationship("UserAssistant", back_populates="assistant_clinics")
    company = relationship("Company", back_populates="assistant_clinics")

    def __repr__(self):
        return f"<AssistantClinic(assistant_id={self.assistant_id}, company_id={self.company_id}, is_admin={self.is_admin})>"

class AssistantProfessional(Base):
    """Tabela auxiliar para relacionar assistentes com profissionais"""
    __tablename__ = "assistant_professionals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    assistant_id = Column(UUID(as_uuid=True), ForeignKey("user_assistants.id"), nullable=False)
    professional_id = Column(UUID(as_uuid=True), ForeignKey("professionals.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    assistant = relationship("UserAssistant", back_populates="assistant_professionals")
    professional = relationship("Professional", back_populates="assistant_professionals")

    def __repr__(self):
        return f"<AssistantProfessional(assistant_id={self.assistant_id}, professional_id={self.professional_id})>" 