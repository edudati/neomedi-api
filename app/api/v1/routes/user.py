from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserBasicResponse, UserWithAuthResponse, UserUpdate
from app.schemas.address import UserAddressUpdate
from app.schemas.user_client import CreateClientRequest, CreateClientResponse
from app.services.user import UserService
from app.services.address import AddressService
from app.services.user_client import UserClientService

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
    address_data: UserAddressUpdate,
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


@router.post("/clients", response_model=CreateClientResponse)
async def create_user_client(
    request: CreateClientRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Criar novo usuário CLIENT.
    
    Requer autenticação de um professional.
    O professional_id vem do JWT do usuário autenticado.
    """
    try:
        # Validar se o usuário autenticado é um professional
        user_role = current_user.get("role")
        if user_role != "professional":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas professionals podem criar clients"
            )
        
        # Pegar o user_id do professional do JWT
        professional_user_id = current_user.get("user_uid")
        if not professional_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_uid não encontrado no token"
            )
        
        # Criar user_client usando o serviço
        result = UserClientService.create_user_client(
            db=db,
            professional_user_id=UUID(professional_user_id),
            company_id=request.company_id,
            client_name=request.name,
            firebase_token=request.firebase_token
        )
        
        return CreateClientResponse(
            success=result["success"],
            message=result["message"],
            client_id=result["client_id"],
            client_data=result["client_data"]
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        ) 