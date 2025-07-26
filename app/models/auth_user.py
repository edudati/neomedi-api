from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class AuthUser(Base):
    """Modelo para usuários de autenticação"""
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False)
    picture = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento com User
    user = relationship("User", back_populates="auth_user", uselist=False)

    def __repr__(self):
        return f"<AuthUser(id={self.id}, email='{self.email}', firebase_uid='{self.firebase_uid}')>" 