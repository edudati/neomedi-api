from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import UserRole
from app.schemas.user_client import (
    CreateClientRequest, 
    CreateClientResponse,
    UserClientWithAuthResponse,
    UserClientUpdate
)
from app.services.user_client import UserClientService

router = APIRouter()


@router.post("/", response_model=CreateClientResponse)
async def create_client(
    request: CreateClientRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Criar novo client.
    
    Requer autenticação de um professional.
    O professional_id vem do JWT do usuário autenticado.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Iniciando criação de client - Request: {request}")
        logger.info(f"Current user: {current_user}")
        
        # Validar se o usuário autenticado é um professional
        user_role = current_user.get("role")
        logger.info(f"User role: {user_role}")
        
        if user_role != "professional":
            logger.error(f"Usuário não é professional: {user_role}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas professionals podem criar clients"
            )
        
        # Pegar o user_id do professional do JWT
        professional_user_id = current_user.get("user_uid")
        logger.info(f"Professional user ID: {professional_user_id}")
        
        if not professional_user_id:
            logger.error("user_uid não encontrado no token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_uid não encontrado no token"
            )
        
        # Criar client usando o serviço
        logger.info("Chamando UserClientService.create_user_client...")
        result = UserClientService.create_user_client(
            db=db,
            professional_user_id=UUID(professional_user_id),
            company_id=request.company_id,
            client_name=request.name,
            firebase_token=request.firebase_token
        )
        
        logger.info(f"Client criado com sucesso: {result}")
        
        try:
            logger.info("Criando CreateClientResponse...")
            response = CreateClientResponse(
                success=result["success"],
                message=result["message"],
                client_id=result["client_id"],
                client_data=result["client_data"]
            )
            logger.info("CreateClientResponse criado com sucesso")
            return response
        except Exception as e:
            logger.error(f"Erro ao criar CreateClientResponse: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro na serialização da resposta: {str(e)}"
            )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no endpoint create_client: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/", response_model=List[UserClientWithAuthResponse])
async def get_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar clients do professional autenticado.
    
    Requer autenticação de um professional.
    """
    # Validar se o usuário autenticado é um professional
    user_role = current_user.get("role")
    if user_role != "professional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas professionals podem listar clients"
        )
    
    # Pegar o user_id do professional do JWT
    professional_user_id = current_user.get("user_uid")
    if not professional_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # Buscar clients do professional
    clients = UserClientService.get_clients_by_professional(
        db=db,
        professional_user_id=UUID(professional_user_id),
        skip=skip,
        limit=limit
    )
    
    return clients


@router.get("/{client_id}", response_model=UserClientWithAuthResponse)
async def get_client(
    client_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar client específico por ID.
    
    Requer autenticação de um professional.
    O professional só pode acessar seus próprios clients.
    """
    # Validar se o usuário autenticado é um professional
    user_role = current_user.get("role")
    if user_role != "professional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas professionals podem acessar clients"
        )
    
    # Pegar o user_id do professional do JWT
    professional_user_id = current_user.get("user_uid")
    if not professional_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # Buscar client (com validação de pertencimento ao professional)
    client_data = UserClientService.get_client_with_auth(
        db, 
        client_id, 
        professional_user_id=UUID(professional_user_id)
    )
    if not client_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client não encontrado ou não pertence ao professional"
        )
    
    return client_data


@router.put("/{client_id}/notes", response_model=UserClientWithAuthResponse)
async def update_client_notes(
    client_id: UUID,
    notes_update: UserClientUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualizar notas do client.
    
    Requer autenticação de um professional.
    O professional só pode atualizar seus próprios clients.
    """
    # Validar se o usuário autenticado é um professional
    user_role = current_user.get("role")
    if user_role != "professional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas professionals podem atualizar clients"
        )
    
    # Pegar o user_id do professional do JWT
    professional_user_id = current_user.get("user_uid")
    if not professional_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # Atualizar notas do client (com validação de pertencimento ao professional)
    updated_client = UserClientService.update_client_notes(
        db=db,
        client_id=client_id,
        notes=notes_update.notes,
        professional_user_id=UUID(professional_user_id)
    )
    
    if not updated_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client não encontrado ou não pertence ao professional"
        )
    
    return updated_client


@router.delete("/{client_id}")
async def delete_client(
    client_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletar client (soft delete).
    
    Requer autenticação de um professional.
    O professional só pode deletar seus próprios clients.
    """
    # Validar se o usuário autenticado é um professional
    user_role = current_user.get("role")
    if user_role != "professional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas professionals podem deletar clients"
        )
    
    # Pegar o user_id do professional do JWT
    professional_user_id = current_user.get("user_uid")
    if not professional_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # TODO: Implementar soft delete do client
    # Por enquanto, retornar erro de não implementado
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidade de deletar client ainda não implementada"
    )


 