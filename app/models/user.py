from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid
from app.db.database import Base
from .enums import UserRole, Gender


class User(Base):
    """Model to user system"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    auth_user_id = Column(Integer, ForeignKey("auth_users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    gender = Column(Enum(Gender, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    has_access = Column(Boolean, default=False)
    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=UserRole.CLIENT)
    social_media = Column(JSONB, nullable=True)
    suspended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    auth_user = relationship("AuthUser", back_populates="user")
    address = relationship("Address", back_populates="user", uselist=False)
    professional = relationship("UserProfessional", back_populates="user", uselist=False)
    client = relationship("UserClient", back_populates="user", uselist=False)



    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', role='{self.role.value}')>"
