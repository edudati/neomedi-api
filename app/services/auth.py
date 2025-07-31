from sqlalchemy.orm import Session
from app.models.auth_user import AuthUser
from app.models.user import User, UserRole
from app.schemas.auth_user import AuthUserCreate, AuthUserUpdate
from app.schemas.user import UserCreate
from app.core.security import verify_firebase_token, create_jwt_token, create_refresh_token
from typing import Optional, Tuple, Dict, Any


class AuthService:
    """Serviço para operações de autenticação"""

    @staticmethod
    def get_user_by_firebase_uid(db: Session, firebase_uid: str) -> Optional[AuthUser]:
        """Busca usuário pelo Firebase UID"""
        return db.query(AuthUser).filter(AuthUser.firebase_uid == firebase_uid).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[AuthUser]:
        """Busca usuário pelo email"""
        return db.query(AuthUser).filter(AuthUser.email == email).first()

    @staticmethod
    def create_auth_user_from_firebase(db: Session, firebase_token: str) -> AuthUser:
        firebase_data = verify_firebase_token(firebase_token)
        user = db.query(AuthUser).filter(AuthUser.firebase_uid == firebase_data["uid"]).first()
        if user:
            update_data = AuthUserUpdate(
                display_name=firebase_data.get("name") or firebase_data["email"].split("@")[0] or user.display_name,
                email_verified=firebase_data.get("email_verified", user.email_verified),
                picture=firebase_data.get("picture", user.picture)
            )
            for field, value in update_data.dict(exclude_unset=True).items():
                setattr(user, field, value)
            db.commit()
            db.refresh(user)
            return user
        else:
            user_data = AuthUserCreate(
                firebase_uid=firebase_data["uid"],
                email=firebase_data["email"],
                display_name=firebase_data.get("name") or firebase_data["email"].split("@")[0],
                email_verified=firebase_data.get("email_verified", False),
                picture=firebase_data.get("picture")
            )
            db_user = AuthUser(**user_data.dict())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

    @staticmethod
    def update_user(db: Session, user: AuthUser, user_data: AuthUserUpdate) -> AuthUser:
        """Atualiza dados do usuário"""
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def process_firebase_token(db: Session, firebase_token: str) -> Tuple[AuthUser, bool, str, str]:
        """
        Processa token do Firebase e retorna usuário + se é novo usuário + tokens
        """
        # Verificar token do Firebase
        firebase_data = verify_firebase_token(firebase_token)
        # Buscar usuário existente
        user = AuthService.get_user_by_firebase_uid(db, firebase_data["uid"])
        if user:
            # Usuário existe - atualizar dados se necessário
            update_data = AuthUserUpdate(
                display_name=firebase_data.get("name") or firebase_data["email"].split("@")[0] or user.display_name,
                email_verified=firebase_data.get("email_verified", user.email_verified),
                picture=firebase_data.get("picture", user.picture)
            )
            user = AuthService.update_user(db, user, update_data)
            is_new_user = False
        else:
            # Novo usuário - criar
            display_name = firebase_data.get("name") or firebase_data["email"].split("@")[0]
            user_data = AuthUserCreate(
                firebase_uid=firebase_data["uid"],
                email=firebase_data["email"],
                display_name=display_name,
                email_verified=firebase_data.get("email_verified", False),
                picture=firebase_data.get("picture")
            )
            user = AuthService.create_auth_user_from_firebase(db, firebase_token) # Changed to create_auth_user_from_firebase
            is_new_user = True
        # Criar tokens JWT
        access_token, refresh_token = AuthService.create_auth_tokens(user, db)
        return user, is_new_user, access_token, refresh_token

    @staticmethod
    def create_auth_tokens(user: AuthUser, db: Session = None) -> Tuple[str, str]:
        """Cria access token e refresh token para o usuário"""
        # Buscar dados do User relacionado se db for fornecido
        user_system = None
        if db:
            from app.models.user import User
            user_system = db.query(User).filter(User.auth_user_id == user.id).first()
        else:
            user_system = user.user
        
        user_data = {
            "email": user.email,
            "name": user_system.name if user_system else user.display_name,
            "user_uid": str(user_system.id) if user_system else None,
            "role": user_system.role.value if user_system else None
        }
        
        access_token = create_jwt_token(user_data)
        refresh_token = create_refresh_token(user_data)
        
        return access_token, refresh_token 