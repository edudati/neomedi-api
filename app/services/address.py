from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.address import Address
from app.models.user import User
from app.schemas.address import AddressCreate, AddressUpdate, UserAddressUpdate, CompanyAddressUpdate
from app.models.user import UserRole


class AddressService:
    """Serviço para gerenciar endereços"""

    @staticmethod
    def add_address(db: Session, address_data: AddressCreate, current_user):
        # Permissão
        if current_user.role != UserRole.PROFESSIONAL:
            raise PermissionError("Apenas profissionais podem adicionar endereços.")
        # Validação de destino
        if bool(address_data.user_id) == bool(address_data.company_id):
            raise ValueError("Informe user_id OU company_id, nunca ambos ou nenhum.")
        address = Address(**address_data.dict())
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def edit_address(db: Session, address_id: UUID, address_update: AddressUpdate, current_user):
        if current_user.role != UserRole.PROFESSIONAL:
            raise PermissionError("Apenas profissionais podem editar endereços.")
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise ValueError("Endereço não encontrado.")
        # Não permite mudar user_id/company_id
        update_data = address_update.dict(exclude_unset=True, exclude={"user_id", "company_id"})
        for field, value in update_data.items():
            setattr(address, field, value)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def delete_address(db: Session, address_id: UUID, current_user):
        if current_user.role != UserRole.PROFESSIONAL:
            raise PermissionError("Apenas profissionais podem remover endereços.")
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise ValueError("Endereço não encontrado.")
        # Se for address de company, garantir que a empresa terá pelo menos um address
        if address.company_id:
            company_addresses = db.query(Address).filter(Address.company_id == address.company_id).count()
            if company_addresses <= 1:
                raise ValueError("A empresa deve ter pelo menos um endereço.")
        db.delete(address)
        db.commit()
        return True

    @staticmethod
    def create_address(db: Session, *, user_id=None, company_id=None, **address_fields) -> Address:
        # Garante que apenas user_id OU company_id seja preenchido
        if bool(user_id) == bool(company_id):
            raise ValueError("Informe user_id OU company_id, nunca ambos ou nenhum.")
        address = Address(user_id=user_id, company_id=company_id, **address_fields)
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def create_or_update_user_address(db: Session, user_id: UUID, address_data: UserAddressUpdate) -> Optional[Address]:
        """Criar ou atualizar endereço do usuário"""
        # Verificar se já existe endereço para o usuário
        existing_address = db.query(Address).filter(Address.user_id == user_id).first()
        
        if existing_address:
            # Atualizar endereço existente
            update_data = address_data.dict(exclude_unset=True, exclude={"user_id", "company_id"})
            for field, value in update_data.items():
                setattr(existing_address, field, value)
            db.commit()
            db.refresh(existing_address)
            return existing_address
        else:
            # Criar novo endereço
            address_fields = address_data.dict(exclude_unset=True, exclude={"user_id", "company_id"})
            return AddressService.create_address(db, user_id=user_id, **address_fields)

    @staticmethod
    def create_or_update_company_address(db: Session, company_id: UUID, address_data: CompanyAddressUpdate) -> Optional[Address]:
        """Criar ou atualizar endereço da empresa"""
        # Verificar se já existe endereço para a empresa
        existing_address = db.query(Address).filter(Address.company_id == company_id).first()
        
        if existing_address:
            # Atualizar endereço existente
            update_data = address_data.dict(exclude_unset=True, exclude={"company_id"})
            for field, value in update_data.items():
                setattr(existing_address, field, value)
            db.commit()
            db.refresh(existing_address)
            return existing_address
        else:
            # Criar novo endereço
            address_fields = address_data.dict(exclude_unset=True, exclude={"company_id"})
            return AddressService.create_address(db, company_id=company_id, **address_fields)

    @staticmethod
    def get_address_with_user(db: Session, address_id: UUID) -> Optional[dict]:
        """Buscar endereço com dados do usuário"""
        db_address = db.query(Address).join(User).filter(Address.id == address_id).first()
        
        if not db_address:
            return None
        
        return {
            "id": db_address.id,
            "user_id": db_address.user_id,
            "street": db_address.street,
            "number": db_address.number,
            "complement": db_address.complement,
            "neighbourhood": db_address.neighbourhood,
            "city": db_address.city,
            "state": db_address.state,
            "zip_code": db_address.zip_code,
            "country": db_address.country,
            "latitude": db_address.latitude,
            "longitude": db_address.longitude,
            "user": {
                "id": db_address.user.id,
                "name": db_address.user.name,
                "role": db_address.user.role.value,
                "is_active": db_address.user.is_active
            }
        } 