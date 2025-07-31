from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base

class ClientProfessionalCompany(Base):
    __tablename__ = "client_professional_company"

    client_id = Column(UUID(as_uuid=True), ForeignKey("user_clients.user_id"), primary_key=True)
    professional_id = Column(UUID(as_uuid=True), ForeignKey("user_professionals.user_id"), primary_key=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), primary_key=True)

    client = relationship("UserClient")
    professional = relationship("UserProfessional")
    company = relationship("Company")