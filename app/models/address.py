from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.database import Base


class Address(Base):
    """Model to address"""
    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    street = Column(String, nullable=True)
    number = Column(String, nullable=True)
    complement = Column(String, nullable=True)
    neighbourhood = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    country = Column(String, nullable=True, default="Brasil")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Foreign Keys (only one should be filled per address)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, unique=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, unique=True)

    # Relationships
    user = relationship("User", back_populates="address")
    company = relationship("Company", back_populates="address")

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', city='{self.city}')>"
