from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.database import Base


class Address(Base):
    """Modelo para endereços"""
    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    complement = Column(String, nullable=True)
    neighbourhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Brasil")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relacionamentos
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="address")
    company = relationship("Company", back_populates="address", uselist=False)

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', city='{self.city}')>" 