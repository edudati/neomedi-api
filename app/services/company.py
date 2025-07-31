from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.company import Company
from app.models.user import User, UserRole
from app.models.address import Address
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyCreateWithAddress
from app.core.security import get_current_user


class CompanyService:
    """Serviço para gerenciar empresas do sistema"""

    @staticmethod
    def create_company_with_validation(db: Session, company_data: CompanyCreateWithAddress, user_professional_id: UUID) -> Company:
        """
        Criar company com validação de perfil professional e lógica de endereço
        """
        # Validar se o usuário existe e é professional
        user = db.query(User).filter(
            and_(
                User.id == user_professional_id,
                User.is_deleted == False
            )
        ).first()
        
        if not user:
            raise ValueError("Usuário não encontrado")
        
        if user.role != UserRole.PROFESSIONAL:
            raise ValueError("Apenas usuários com perfil professional podem criar empresas")
        
        # Criar a company
        company = Company(
            name=company_data.name,
            description=company_data.description,
            email=company_data.email,
            phone=company_data.phone,
            social_media=company_data.social_media,
            is_virtual=company_data.is_virtual,
            is_active=company_data.is_active,
            user_professional_id=user_professional_id
        )
        
        db.add(company)
        db.commit()
        db.refresh(company)
        
        # Criar endereço apenas se is_virtual = False e address foi fornecido
        if not company_data.is_virtual and company_data.address:
            from app.services.address import AddressService
            AddressService.create_address(
                db, 
                company_id=company.id, 
                **company_data.address.dict()
            )
        
        return company

    @staticmethod
    def create_company(db: Session, name: str, user_professional_id: UUID, address_fields=None, **company_fields) -> Company:
        company = Company(
            name=name,
            user_professional_id=user_professional_id,
            **company_fields
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        if address_fields is None:
            address_fields = {}
        from app.services.address import AddressService
        AddressService.create_address(db, company_id=company.id, **address_fields)
        return company

    @staticmethod
    def get_company_by_id(db: Session, company_id: UUID) -> Optional[Company]:
        """Buscar company por ID"""
        return db.query(Company).filter(
            Company.id == company_id
        ).first()

    @staticmethod
    def get_company_by_user_id(db: Session, user_id: UUID) -> Optional[Company]:
        """Buscar company por user_id"""
        return db.query(Company).filter(
            Company.user_professional_id == user_id
        ).first()

    @staticmethod
    def get_companies_by_user_id(db: Session, user_id: UUID) -> List[dict]:
        """Buscar todas as companies por user_id com endereços"""
        companies = db.query(Company).filter(
            Company.user_professional_id == user_id
        ).all()
        
        result = []
        for company in companies:
            # Buscar endereço da company
            address_data = None
            company_address = db.query(Address).filter(Address.company_id == company.id).first()
            if company_address:
                address_data = {
                    "id": company_address.id,
                    "street": company_address.street,
                    "number": company_address.number,
                    "complement": company_address.complement,
                    "neighbourhood": company_address.neighbourhood,
                    "city": company_address.city,
                    "state": company_address.state,
                    "zip_code": company_address.zip_code,
                    "country": company_address.country,
                    "latitude": company_address.latitude,
                    "longitude": company_address.longitude
                }
            
            result.append({
                "id": company.id,
                "user_id": company.user_professional_id,
                "name": company.name,
                "description": company.description,
                "email": company.email,
                "phone": company.phone,
                "social_media": company.social_media,
                "is_virtual": company.is_virtual,
                "is_active": company.is_active,
                "address": address_data
            })
        
        return result

    @staticmethod
    def get_company_by_user_id_with_address(db: Session, user_id: UUID) -> Optional[dict]:
        """Buscar company por user_id com dados do endereço"""
        db_company = db.query(Company).filter(
            Company.user_professional_id == user_id
        ).first()
        
        if not db_company:
            return None
        
        # Buscar endereço da company (se existir)
        address_data = None
        company_address = db.query(Address).filter(Address.company_id == db_company.id).first()
        if company_address:
            address_data = {
                "id": company_address.id,
                "street": company_address.street,
                "number": company_address.number,
                "complement": company_address.complement,
                "neighbourhood": company_address.neighbourhood,
                "city": company_address.city,
                "state": company_address.state,
                "zip_code": company_address.zip_code,
                "country": company_address.country,
                "latitude": company_address.latitude,
                "longitude": company_address.longitude
            }
        
        return {
            "id": db_company.id,
            "user_id": db_company.user_professional_id,
            "name": db_company.name,
            "description": db_company.description,
            "email": db_company.email,
            "phone": db_company.phone,
            "social_media": db_company.social_media,
            "is_virtual": db_company.is_virtual,
            "is_active": db_company.is_active,
            "address": address_data
        }

    @staticmethod
    def get_company_address_by_user_id(db: Session, user_id: UUID) -> Optional[dict]:
        """Buscar endereço da company através do user_id"""
        # Primeiro buscar a company do usuário
        db_company = db.query(Company).filter(
            Company.user_professional_id == user_id
        ).first()
        
        if not db_company:
            return None
        
        # Buscar endereço da company
        address = db.query(Address).filter(Address.company_id == db_company.id).first()
        if not address:
            return None
        
        return {
            "id": address.id,
            "street": address.street,
            "number": address.number,
            "complement": address.complement,
            "neighbourhood": address.neighbourhood,
            "city": address.city,
            "state": address.state,
            "zip_code": address.zip_code,
            "country": address.country,
            "latitude": address.latitude,
            "longitude": address.longitude,
            "company_id": address.company_id
        }

    @staticmethod
    def get_company_address_by_company_id(db: Session, company_id: UUID) -> Optional[dict]:
        """Buscar endereço da company por company_id"""
        address = db.query(Address).filter(Address.company_id == company_id).first()
        if not address:
            return None
        
        return {
            "id": address.id,
            "street": address.street,
            "number": address.number,
            "complement": address.complement,
            "neighbourhood": address.neighbourhood,
            "city": address.city,
            "state": address.state,
            "zip_code": address.zip_code,
            "country": address.country,
            "latitude": address.latitude,
            "longitude": address.longitude,
            "company_id": address.company_id
        }

    @staticmethod
    def update_company_address(db: Session, company_id: UUID, address_data: dict) -> Optional[dict]:
        """Atualizar endereço da company"""
        # Buscar endereço existente da company
        existing_address = db.query(Address).filter(Address.company_id == company_id).first()
        
        if existing_address:
            # Atualizar endereço existente
            for field, value in address_data.items():
                if hasattr(existing_address, field):
                    setattr(existing_address, field, value)
            db.commit()
            db.refresh(existing_address)
            address = existing_address
        else:
            # Criar novo endereço para a company
            address_data["company_id"] = company_id
            new_address = Address(**address_data)
            db.add(new_address)
            db.commit()
            db.refresh(new_address)
            address = new_address
        
        return {
            "id": address.id,
            "street": address.street,
            "number": address.number,
            "complement": address.complement,
            "neighbourhood": address.neighbourhood,
            "city": address.city,
            "state": address.state,
            "zip_code": address.zip_code,
            "country": address.country,
            "latitude": address.latitude,
            "longitude": address.longitude,
            "company_id": address.company_id
        }

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
        query = db.query(Company)
        
        if is_active is not None:
            query = query.filter(Company.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_company(db: Session, company_id: UUID, company_data: CompanyUpdate, current_user_id: UUID) -> Optional[Company]:
        """Atualizar company - apenas o proprietário pode editar"""
        db_company = CompanyService.get_company_by_id(db, company_id)
        if not db_company:
            return None
        
        # Verificar se o usuário atual é o proprietário da company
        if db_company.user_professional_id != current_user_id:
            return None
        
        update_data = company_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_company, field, value)
        

        db.commit()
        db.refresh(db_company)
        return db_company

    @staticmethod
    def get_company_with_address(db: Session, company_id: UUID) -> Optional[dict]:
        """Buscar company com dados do endereço"""
        db_company = db.query(Company).filter(
            Company.id == company_id
        ).first()
        
        if not db_company:
            return None
        
        # Buscar endereço da company
        address_data = None
        company_address = db.query(Address).filter(Address.company_id == company_id).first()
        if company_address:
            address_data = {
                "id": company_address.id,
                "street": company_address.street,
                "number": company_address.number,
                "complement": company_address.complement,
                "neighbourhood": company_address.neighbourhood,
                "city": company_address.city,
                "state": company_address.state,
                "zip_code": company_address.zip_code,
                "country": company_address.country,
                "latitude": company_address.latitude,
                "longitude": company_address.longitude
            }
        
        return {
            "id": db_company.id,
            "user_id": db_company.user_professional_id,
            "name": db_company.name,
            "description": db_company.description,
            "email": db_company.email,
            "phone": db_company.phone,
            "social_media": db_company.social_media,
            "is_virtual": db_company.is_virtual,
            "is_active": db_company.is_active,
            "address": address_data
        }

    @staticmethod
    def can_user_edit_company(db: Session, company_id: UUID, user_id: UUID) -> bool:
        """Verificar se o usuário pode editar a company"""
        db_company = CompanyService.get_company_by_id(db, company_id)
        if not db_company:
            return False
        
        # Verificar se o usuário é o proprietário da company
        if db_company.user_professional_id != user_id:
            return False
        
        # Verificar se o usuário tem role ADMIN
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user or db_user.role != UserRole.ADMIN:
            return False
        
        return True 