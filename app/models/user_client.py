from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class UserClient(Base):
    """Extended model for client users"""
    __tablename__ = "user_clients"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="client")

    def __repr__(self):
        return f"<UserClient(user_id={self.user_id})>"
