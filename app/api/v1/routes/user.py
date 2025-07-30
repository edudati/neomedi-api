from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserBasicResponse, UserWithAuthResponse, UserUpdate
from app.schemas.address import AddressUpdate
from app.services.user_service import UserService
from app.services.address_service import AddressService

router = APIRouter()


@router.get("/profile", response_model=UserBasicResponse)
async def get_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna dados básicos do usuário atual (sem endereço).
    """
    # Buscar usuário no banco usando o user_uid do JWT
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    user_data = UserService.get_user_with_auth(db, UUID(user_id))
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Remover dados de endereço para retornar apenas dados básicos
    user_data.pop("address", None)
    
    return user_data


@router.get("/profile/complete", response_model=UserWithAuthResponse)
async def get_user_profile_complete(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna dados completos do usuário atual (com endereço).
    """
    # Buscar usuário no banco usando o user_uid do JWT
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    user_data = UserService.get_user_with_auth(db, UUID(user_id))
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user_data


@router.put("/profile", response_model=UserBasicResponse)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza dados básicos do usuário atual (nome, telefone, etc.).
    """
    # Buscar usuário no banco usando o user_uid do JWT
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # Atualizar usuário
    updated_user = UserService.update_user(db, UUID(user_id), user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Retornar dados atualizados
    user_data_response = UserService.get_user_with_auth(db, UUID(user_id))
    user_data_response.pop("address", None)  # Remover endereço para retornar dados básicos
    
    return user_data_response


@router.put("/address", response_model=UserWithAuthResponse)
async def update_user_address(
    address_data: AddressUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza ou cria endereço do usuário atual.
    """
    # Buscar usuário no banco usando o user_uid do JWT
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # Criar ou atualizar endereço
    updated_address = AddressService.create_or_update_user_address(db, UUID(user_id), address_data)
    if not updated_address:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar endereço"
        )
    
    # Retornar dados completos atualizados
    user_data_response = UserService.get_user_with_auth(db, UUID(user_id))
    
    return user_data_response 