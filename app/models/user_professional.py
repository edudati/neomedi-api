from sqlalchemy import Column, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class UserProfessional(Base):
    """Extended model for professional users"""
    __tablename__ = "user_professionals"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    bio = Column(Text, nullable=True)
    license_number = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)      # visível em buscas
    is_available = Column(Boolean, default=True)   # aceita agendamentos

    # Relationships
    user = relationship("User", back_populates="professional")

    def __repr__(self):
        return f"<UserProfessional(user_id={self.user_id}, public={self.is_public}, available={self.is_available})>"
