from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Generator, Dict, Any

from app.db.database import get_db
from app.models.user import User
from app.services.user_service import UserService
from app.core.security import get_current_user as get_current_user_from_token


def get_current_user() -> Dict[str, Any]:
    """
    Dependência para obter o usuário atual autenticado
    """
    return get_current_user_from_token


def get_db_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependência para obter o usuário atual do banco de dados
    """
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user_uid não encontrado no token"
        )
    
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user
