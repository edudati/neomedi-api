from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.company import Company
from app.models.user import User, UserRole
from app.models.address import Address
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.core.security import get_current_user


class CompanyService:
    """Serviço para gerenciar empresas do sistema"""

    @staticmethod
    def create_company_for_admin(db: Session, user_id: UUID, user_name: str, user_email: str) -> Company:
        """Criar company automaticamente para usuário admin"""
        # Gerar dados padrão para a company
        company_data = {
            "user_id": user_id,
            "name": f"Clínica {user_name}",
            "legal_name": f"Clínica {user_name} Ltda",
            "legal_id": "00000000000000",  # CNPJ placeholder - deve ser atualizado
            "email": user_email,
            "phone": None,
            "is_active": True,
            "is_visible": True,
            "is_public": False
        }
        
        db_company = Company(**company_data)
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company

    @staticmethod
    def get_company_by_id(db: Session, company_id: UUID) -> Optional[Company]:
        """Buscar company por ID"""
        return db.query(Company).filter(
            and_(
                Company.id == company_id,
                Company.is_deleted == False
            )
        ).first()

    @staticmethod
    def get_company_by_user_id(db: Session, user_id: UUID) -> Optional[Company]:
        """Buscar company por user_id"""
        return db.query(Company).filter(
            and_(
                Company.user_id == user_id,
                Company.is_deleted == False
            )
        ).first()

    @staticmethod
    def get_companies(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_visible: Optional[bool] = None,
        is_public: Optional[bool] = None
    ) -> List[Company]:
        """Listar companies com filtros opcionais"""
        query = db.query(Company).filter(Company.is_deleted == False)
        
        if is_active is not None:
            query = query.filter(Company.is_active == is_active)
        
        if is_visible is not None:
            query = query.filter(Company.is_visible == is_visible)
        
        if is_public is not None:
            query = query.filter(Company.is_public == is_public)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_company(db: Session, company_id: UUID, company_data: CompanyUpdate, current_user_id: UUID) -> Optional[Company]:
        """Atualizar company - apenas o proprietário pode editar"""
        db_company = CompanyService.get_company_by_id(db, company_id)
        if not db_company:
            return None
        
        # Verificar se o usuário atual é o proprietário da company
        if db_company.user_id != current_user_id:
            return None
        
        update_data = company_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_company, field, value)
        
        db_company.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_company)
        return db_company

    @staticmethod
    def get_company_with_address(db: Session, company_id: UUID) -> Optional[dict]:
        """Buscar company com dados do endereço"""
        db_company = db.query(Company).join(Address, Company.address_id == Address.id, isouter=True).filter(
            and_(
                Company.id == company_id,
                Company.is_deleted == False
            )
        ).first()
        
        if not db_company:
            return None
        
        # Dados do endereço (se existir)
        address_data = None
        if db_company.address:
            address_data = {
                "id": db_company.address.id,
                "street": db_company.address.street,
                "number": db_company.address.number,
                "complement": db_company.address.complement,
                "neighbourhood": db_company.address.neighbourhood,
                "city": db_company.address.city,
                "state": db_company.address.state,
                "zip_code": db_company.address.zip_code,
                "country": db_company.address.country,
                "latitude": db_company.address.latitude,
                "longitude": db_company.address.longitude
            }
        
        return {
            "id": db_company.id,
            "user_id": db_company.user_id,
            "name": db_company.name,
            "legal_name": db_company.legal_name,
            "legal_id": db_company.legal_id,
            "email": db_company.email,
            "phone": db_company.phone,
            "address_id": db_company.address_id,
            "is_active": db_company.is_active,
            "is_deleted": db_company.is_deleted,
            "is_visible": db_company.is_visible,
            "is_public": db_company.is_public,
            "created_at": db_company.created_at,
            "updated_at": db_company.updated_at,
            "address": address_data
        }

    @staticmethod
    def can_user_edit_company(db: Session, company_id: UUID, user_id: UUID) -> bool:
        """Verificar se o usuário pode editar a company"""
        db_company = CompanyService.get_company_by_id(db, company_id)
        if not db_company:
            return False
        
        # Verificar se o usuário é o proprietário da company
        if db_company.user_id != user_id:
            return False
        
        # Verificar se o usuário tem role ADMIN
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user or db_user.role != UserRole.ADMIN:
            return False
        
        return True 