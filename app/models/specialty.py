from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base


class Specialty(Base):
    """Modelo para especialidades médicas"""
    __tablename__ = "specialties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, unique=True)  # Nome da especialidade
    slug = Column(String, nullable=False, unique=True)  # Slug para URL
    category = Column(String, nullable=True)  # Categoria da especialidade
    description = Column(String, nullable=True)  # Descrição opcional
    is_public = Column(Boolean, default=True)  # Se é uma especialidade pública/curada
    is_visible = Column(Boolean, default=True)  # Se é visível para seleção
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Quem criou
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    created_by_user = relationship("User", back_populates="created_specialties")
    professional_specialties = relationship("ProfessionalSpecialty", back_populates="specialty")

    def __repr__(self):
        return f"<Specialty(id={self.id}, name='{self.name}', is_public={self.is_public})>"


class ProfessionalSpecialty(Base):
    """Tabela auxiliar para relacionar profissionais com especialidades"""
    __tablename__ = "professional_specialties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    professional_id = Column(UUID(as_uuid=True), ForeignKey("professionals.id"), nullable=False)
    specialty_id = Column(UUID(as_uuid=True), ForeignKey("specialties.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    professional = relationship("Professional", back_populates="specialties")
    specialty = relationship("Specialty", back_populates="professional_specialties")

    def __repr__(self):
        return f"<ProfessionalSpecialty(professional_id={self.professional_id}, specialty_id={self.specialty_id})>" 