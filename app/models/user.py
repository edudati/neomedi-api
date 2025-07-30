from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid
from app.db.database import Base


class UserRole(enum.Enum):
    """Enum para roles de usuário"""
    SUPER = "super"           # Acesso total ao sistema
    ADMIN = "admin"           # Gerencia uma ou mais clínicas
    MANAGER = "manager"       # Coordena equipe local (ex: gerente de unidade)
    PROFESSIONAL = "professional"  # Médicos, terapeutas, psicólogos, etc.
    ASSISTANT = "assistant"   # Responsável por agendamentos e atendimento (ex: secretária)
    CLIENT = "client"         # Paciente/usuário final


class User(Base):
    """Modelo para usuários do sistema"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    auth_user_id = Column(Integer, ForeignKey("auth_users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=UserRole.CLIENT)
    suspended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    auth_user = relationship("AuthUser", back_populates="user")
    address = relationship("Address", back_populates="user", uselist=False)
    companies = relationship("Company", back_populates="user")
    professional = relationship("Professional", back_populates="user", uselist=False)
    assistant = relationship("UserAssistant", back_populates="user", uselist=False)
    created_specialties = relationship("Specialty", back_populates="created_by_user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', role='{self.role.value}')>" 