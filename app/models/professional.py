from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base


class Professional(Base):
    """Modelo para profissionais de saúde"""
    __tablename__ = "professionals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    treatment_title = Column(String, nullable=False)  # Título do tratamento
    profile_completed = Column(Boolean, default=False)  # Se o perfil está completo
    bio = Column(String, nullable=True)  # Biografia do profissional
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="professional")
    specialties = relationship("ProfessionalSpecialty", back_populates="professional")
    professions = relationship("ProfessionalProfession", back_populates="professional")
    assistant_professionals = relationship("AssistantProfessional", back_populates="professional")

    def __repr__(self):
        return f"<Professional(id={self.id}, treatment_title='{self.treatment_title}')>" 