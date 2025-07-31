from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import UUID

from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.company import CompanyResponse, CompanyWithAddressResponse, CompanyUpdate, CompanyCreateWithAddress
from typing import List
from app.schemas.address import CompanyAddressUpdate
from app.services.company import CompanyService
from app.services.address import AddressService

router = APIRouter()


@router.post("/", response_model=CompanyWithAddressResponse)
async def create_company(
    company_data: CompanyCreateWithAddress,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova empresa para o usuário professional atual.
    """
    # Buscar usuário no banco usando o user_uid do JWT
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    try:
        # Criar company com validação
        company = CompanyService.create_company_with_validation(
            db, 
            company_data, 
            UUID(user_id)
        )
        
        # Retornar dados completos da company criada
        company_response = CompanyService.get_company_with_address(db, company.id)
        
        return company_response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.get("/", response_model=List[CompanyWithAddressResponse])
async def get_user_companies(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna todas as empresas do usuário atual.
    """
    # Buscar usuário no banco usando o user_uid do JWT
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    companies = CompanyService.get_companies_by_user_id(db, UUID(user_id))
    
    return companies


@router.get("/{company_id}", response_model=CompanyWithAddressResponse)
async def get_company_by_id(
    company_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna dados completos de uma empresa específica.
    """
    # Verificar se o usuário tem permissão para acessar esta empresa
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    company_data = CompanyService.get_company_with_address(db, company_id)
    if not company_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    # Verificar se o usuário é o proprietário da empresa
    if company_data["user_id"] != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar esta empresa"
        )
    
    return company_data


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company_by_id(
    company_id: UUID,
    company_data: CompanyUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza dados de uma empresa específica.
    """
    # Verificar se o usuário tem permissão para editar esta empresa
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # Atualizar empresa
    updated_company = CompanyService.update_company(db, company_id, company_data, UUID(user_id))
    if not updated_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada ou sem permissão para editar"
        )
    
    # Retornar dados atualizados
    company_data_response = CompanyService.get_company_with_address(db, company_id)
    company_data_response.pop("address", None)  # Remover endereço para retornar dados básicos
    
    return company_data_response


@router.put("/{company_id}/address", response_model=CompanyWithAddressResponse)
async def update_company_address_by_id(
    company_id: UUID,
    address_data: CompanyAddressUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza ou cria endereço de uma empresa específica.
    """
    # Verificar se o usuário tem permissão para editar esta empresa
    user_id = current_user.get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_uid não encontrado no token"
        )
    
    # Verificar se a empresa existe e se o usuário é o proprietário
    company = CompanyService.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    if company.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar esta empresa"
        )
    
    # Criar ou atualizar endereço da empresa
    updated_address = AddressService.create_or_update_company_address(db, company_id, address_data)
    if not updated_address:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar endereço"
        )
    
    # Retornar dados completos atualizados
    company_data_response = CompanyService.get_company_with_address(db, company_id)
    
    return company_data_response


 