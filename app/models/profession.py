from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base


class Profession(Base):
    """Modelo para profissões de saúde"""
    __tablename__ = "professions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, unique=True)  # Ex: "Psicólogo", "Médico", "Terapeuta Ocupacional"
    cbo_code = Column(String, nullable=True)  # Código CBO
    council_type = Column(String, nullable=True)  # Ex: CRM, CRP, CREFITO
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    professional_professions = relationship("ProfessionalProfession", back_populates="profession")

    def __repr__(self):
        return f"<Profession(id={self.id}, name='{self.name}', council_type='{self.council_type}')>"


class ProfessionalProfession(Base):
    """Tabela auxiliar para relacionar profissionais com profissões"""
    __tablename__ = "professional_professions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    professional_id = Column(UUID(as_uuid=True), ForeignKey("professionals.id"), nullable=False)
    profession_id = Column(UUID(as_uuid=True), ForeignKey("professions.id"), nullable=False)
    council_number = Column(String, nullable=True)  # Número do conselho
    council_uf = Column(String, nullable=True)  # UF do conselho
    rqe_type = Column(String, nullable=True)  # Registro de especialista
    is_primary = Column(Boolean, default=False)  # Se é a profissão principal
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    professional = relationship("Professional", back_populates="professions")
    profession = relationship("Profession", back_populates="professional_professions")

    def __repr__(self):
        return f"<ProfessionalProfession(professional_id={self.professional_id}, profession_id={self.profession_id}, is_primary={self.is_primary})>" 