from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import uuid
from app.db.database import Base


class Company(Base):
    """Model to represent a place of service (can be virtual or physical)"""
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    social_media = Column(JSONB, nullable=True)
    is_virtual = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    address = relationship("Address", back_populates="company", uselist=False)

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', is_virtual={self.is_virtual})>"
