from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.address import Address
from app.models.user import User
from app.schemas.address import AddressCreate, AddressUpdate


class AddressService:
    """Serviço para gerenciar endereços"""

    @staticmethod
    def create_address(db: Session, address_data: AddressCreate) -> Address:
        """Criar novo endereço"""
        db_address = Address(**address_data.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

    @staticmethod
    def get_address_by_id(db: Session, address_id: UUID) -> Optional[Address]:
        """Buscar endereço por ID"""
        return db.query(Address).filter(Address.id == address_id).first()

    @staticmethod
    def get_address_by_user_id(db: Session, user_id: UUID) -> Optional[Address]:
        """Buscar endereço por user_id"""
        return db.query(Address).filter(Address.user_id == user_id).first()

    @staticmethod
    def get_addresses(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        city: Optional[str] = None,
        state: Optional[str] = None
    ) -> List[Address]:
        """Listar endereços com filtros opcionais"""
        query = db.query(Address)
        
        if city:
            query = query.filter(Address.city.ilike(f"%{city}%"))
        
        if state:
            query = query.filter(Address.state.ilike(f"%{state}%"))
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_address(db: Session, address_id: UUID, address_data: AddressUpdate) -> Optional[Address]:
        """Atualizar endereço"""
        db_address = AddressService.get_address_by_id(db, address_id)
        if not db_address:
            return None
        
        update_data = address_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_address, field, value)
        
        db.commit()
        db.refresh(db_address)
        return db_address

    @staticmethod
    def delete_address(db: Session, address_id: UUID) -> bool:
        """Deletar endereço"""
        db_address = AddressService.get_address_by_id(db, address_id)
        if not db_address:
            return False
        
        db.delete(db_address)
        db.commit()
        return True

    @staticmethod
    def create_or_update_user_address(db: Session, user_id: UUID, address_data: AddressUpdate) -> Optional[Address]:
        """Criar ou atualizar endereço do usuário"""
        # Verificar se já existe endereço para o usuário
        existing_address = AddressService.get_address_by_user_id(db, user_id)
        
        if existing_address:
            # Atualizar endereço existente
            return AddressService.update_address(db, existing_address.id, address_data)
        else:
            # Criar novo endereço
            create_data = AddressCreate(
                user_id=user_id,
                **address_data.dict(exclude_unset=True)
            )
            return AddressService.create_address(db, create_data)

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