from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.user import User, UserRole
from app.models.auth_user import AuthUser
from app.models.address import Address
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_current_user
from .company import CompanyService


class UserService:
    """Serviço para gerenciar usuários do sistema"""

    @staticmethod
    def create_user(db: Session, auth_user: AuthUser, role: UserRole, **user_fields) -> User:
        user = User(
            auth_user_id=auth_user.id,
            name=auth_user.display_name,
            email=auth_user.email,  # Garantir que o email seja preenchido
            role=role,
            is_verified=False,
            is_active=True,
            has_access=True,  # Garantir que has_access seja True
            **user_fields
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """Buscar usuário por ID"""
        return db.query(User).filter(
            and_(
                User.id == user_id,
                User.is_deleted == False
            )
        ).first()

    @staticmethod
    def get_user_by_auth_user_id(db: Session, auth_user_id: int) -> Optional[User]:
        """Buscar usuário por auth_user_id"""
        return db.query(User).filter(
            and_(
                User.auth_user_id == auth_user_id,
                User.is_deleted == False
            )
        ).first()

    @staticmethod
    def get_users(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """Listar usuários com filtros opcionais"""
        query = db.query(User).filter(User.is_deleted == False)
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """Atualizar usuário"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        # Sempre garantir que email e profile_picture_url estejam sincronizados com AuthUser
        auth_user = db.query(AuthUser).filter(AuthUser.id == db_user.auth_user_id).first()
        if auth_user:
            db_user.email = auth_user.email
            db_user.profile_picture_url = auth_user.picture
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> bool:
        """Deletar usuário (soft delete)"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False
        
        db_user.is_deleted = True
        db_user.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def suspend_user(db: Session, user_id: UUID) -> Optional[User]:
        """Suspender usuário"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        db_user.is_active = False
        db_user.suspended_at = datetime.utcnow()
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def activate_user(db: Session, user_id: UUID) -> Optional[User]:
        """Ativar usuário"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        db_user.is_active = True
        db_user.suspended_at = None
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def verify_user(db: Session, user_id: UUID) -> Optional[User]:
        """Verificar usuário"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        db_user.is_verified = True
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_with_auth(db: Session, user_id: UUID) -> Optional[dict]:
        """Buscar usuário com dados de autenticação"""
        db_user = db.query(User).join(AuthUser).filter(
            and_(
                User.id == user_id,
                User.is_deleted == False
            )
        ).first()
        
        if not db_user:
            return None
        
        # Buscar endereço do usuário
        address_data = None
        if db_user.address:
            address_data = {
                "id": db_user.address.id,
                "street": db_user.address.street,
                "number": db_user.address.number,
                "complement": db_user.address.complement,
                "neighbourhood": db_user.address.neighbourhood,
                "city": db_user.address.city,
                "state": db_user.address.state,
                "zip_code": db_user.address.zip_code,
                "country": db_user.address.country,
                "latitude": db_user.address.latitude,
                "longitude": db_user.address.longitude
            }
        
        return {
            "id": db_user.id,
            "auth_user_id": db_user.auth_user_id,
            "name": db_user.name,
            "email": db_user.email,
            "profile_picture_url": db_user.picture,
            "phone": db_user.phone,
            "birth_date": db_user.birth_date,
            "gender": db_user.gender.value if db_user.gender else None,
            "is_active": db_user.is_active,
            "is_deleted": db_user.is_deleted,
            "is_verified": db_user.is_verified,
            "has_access": db_user.has_access,
            "role": db_user.role.value,
            "social_media": db_user.social_media,
            "suspended_at": db_user.suspended_at,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at,
            "auth_user": {
                "id": db_user.auth_user.id,
                "email": db_user.auth_user.email,
                "firebase_uid": db_user.auth_user.firebase_uid,
                "display_name": db_user.auth_user.display_name,
                "email_verified": db_user.auth_user.email_verified,
                "picture": db_user.auth_user.picture
            },
            "address": address_data
        } 