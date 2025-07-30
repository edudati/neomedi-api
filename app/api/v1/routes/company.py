from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.v1.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.models.company import Company
from app.schemas.company import CompanyUpdate, CompanyResponse, CompanyWithAddressResponse
from app.services.company_service import CompanyService

router = APIRouter()


@router.get("/{company_id}", response_model=CompanyWithAddressResponse)
def get_company(
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar company por ID"""
    company_data = CompanyService.get_company_with_address(db, company_id)
    if not company_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company não encontrada"
        )
    
    return company_data


@router.get("/user/{user_id}", response_model=CompanyWithAddressResponse)
def get_company_by_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar company por user_id"""
    company_data = CompanyService.get_company_by_user_id(db, user_id)
    if not company_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company não encontrada para este usuário"
        )
    
    # Buscar dados completos com endereço
    company_with_address = CompanyService.get_company_with_address(db, company_data.id)
    return company_with_address


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar company - apenas o proprietário admin pode editar"""
    # Verificar se o usuário tem permissão para editar a company
    if not CompanyService.can_user_edit_company(db, company_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar esta company"
        )
    
    # Atualizar a company
    updated_company = CompanyService.update_company(
        db=db,
        company_id=company_id,
        company_data=company_data,
        current_user_id=current_user.id
    )
    
    if not updated_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company não encontrada"
        )
    
    return updated_company


@router.get("/", response_model=List[CompanyResponse])
def list_companies(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    is_visible: bool = None,
    is_public: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar companies com filtros opcionais"""
    companies = CompanyService.get_companies(
        db=db,
        skip=skip,
        limit=limit,
        is_active=is_active,
        is_visible=is_visible,
        is_public=is_public
    )
    
    return companies 