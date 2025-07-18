from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from typing import Optional


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Cria um novo usuário no banco de dados"""
        db_user = User(
            email=user_data.email,
            firebase_uid=user_data.firebase_uid
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_firebase_uid(db: Session, firebase_uid: str) -> Optional[User]:
        """Busca usuário por firebase_uid"""
        return db.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    @staticmethod
    def user_exists(db: Session, email: str, firebase_uid: str) -> bool:
        """Verifica se usuário já existe por email ou firebase_uid"""
        existing_user = db.query(User).filter(
            (User.email == email) | (User.firebase_uid == firebase_uid)
        ).first()
        return existing_user is not None
    
    @staticmethod
    def get_existing_user_info(db: Session, email: str, firebase_uid: str) -> dict:
        """Retorna informações sobre usuário existente"""
        user_by_email = db.query(User).filter(User.email == email).first()
        user_by_uid = db.query(User).filter(User.firebase_uid == firebase_uid).first()
        
        if user_by_email is not None and user_by_uid is not None and user_by_email.id != user_by_uid.id:
            return {"error": "Email e firebase_uid já existem em usuários diferentes"}
        elif user_by_email is not None:
            return {"error": "Email já existe", "existing_uid": user_by_email.firebase_uid}
        elif user_by_uid is not None:
            return {"error": "Firebase UID já existe", "existing_email": user_by_uid.email}
        
        return {"error": None}
    
    @staticmethod
    def update_last_login(db: Session, user_id: int) -> None:
        """Atualiza o último login do usuário"""
        # TODO: Implementar atualização do last_login
        pass 