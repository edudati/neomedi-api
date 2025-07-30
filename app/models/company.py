from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base


class Company(Base):
    """Modelo para empresas do sistema"""
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)  # Nome fantasia
    legal_name = Column(String, nullable=False)  # Razão social
    legal_id = Column(String, nullable=False)  # CNPJ
    email = Column(String, nullable=False)  # Email institucional
    phone = Column(String, nullable=True)  # Telefone principal
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="companies")
    address = relationship("Address", back_populates="company")
    assistant_clinics = relationship("AssistantClinic", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', legal_name='{self.legal_name}')>" 