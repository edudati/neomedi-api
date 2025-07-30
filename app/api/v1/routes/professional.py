from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.v1.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.models.professional import Professional
from app.schemas.professional import ProfessionalCreate, ProfessionalUpdate, ProfessionalResponse, ProfessionalWithDetailsResponse
from app.schemas.specialty import SpecialtyCreate, SpecialtyResponse, ProfessionalSpecialtyCreate
from app.schemas.profession import ProfessionResponse, ProfessionalProfessionCreate, ProfessionalProfessionUpdate, ProfessionalProfessionResponse
from app.services.professional_service import ProfessionalService, SpecialtyService, ProfessionService

router = APIRouter()


# Rotas para Professional
@router.post("/", response_model=ProfessionalResponse)
def create_professional(
    professional_data: ProfessionalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar novo profissional"""
    # Verificar se o usuário já tem um perfil profissional
    existing = ProfessionalService.get_professional_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui um perfil profissional"
        )
    
    # Verificar se o usuário tem role PROFESSIONAL
    if current_user.role != UserRole.PROFESSIONAL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas usuários com role PROFESSIONAL podem criar perfil profissional"
        )
    
    professional_data.user_id = current_user.id
    professional = ProfessionalService.create_professional(db, professional_data)
    return professional


@router.get("/{professional_id}", response_model=ProfessionalWithDetailsResponse)
def get_professional(
    professional_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar profissional por ID com detalhes"""
    professional_data = ProfessionalService.get_professional_with_details(db, professional_id)
    if not professional_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )
    
    return professional_data


@router.get("/user/{user_id}", response_model=ProfessionalWithDetailsResponse)
def get_professional_by_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar profissional por user_id"""
    professional = ProfessionalService.get_professional_by_user_id(db, user_id)
    if not professional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado para este usuário"
        )
    
    professional_data = ProfessionalService.get_professional_with_details(db, professional.id)
    return professional_data


@router.put("/{professional_id}", response_model=ProfessionalResponse)
def update_professional(
    professional_id: UUID,
    professional_data: ProfessionalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar profissional"""
    # Verificar se o usuário é o proprietário do perfil
    professional = ProfessionalService.get_professional_by_id(db, professional_id)
    if not professional or professional.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este perfil"
        )
    
    updated_professional = ProfessionalService.update_professional(
        db, professional_id, professional_data
    )
    
    if not updated_professional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )
    
    return updated_professional


@router.get("/", response_model=List[ProfessionalResponse])
def list_professionals(
    skip: int = 0,
    limit: int = 100,
    profile_completed: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar profissionais com filtros opcionais"""
    professionals = ProfessionalService.get_professionals(
        db=db,
        skip=skip,
        limit=limit,
        profile_completed=profile_completed
    )
    
    return professionals


# Rotas para Specialty
@router.post("/specialties", response_model=SpecialtyResponse)
def create_specialty(
    specialty_data: SpecialtyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar nova especialidade"""
    specialty_data.created_by = current_user.id
    try:
        specialty = SpecialtyService.create_specialty(db, specialty_data)
        return specialty
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/specialties", response_model=List[SpecialtyResponse])
def list_specialties(
    skip: int = 0,
    limit: int = 100,
    is_public: bool = None,
    is_visible: bool = None,
    category: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar especialidades com filtros opcionais"""
    specialties = SpecialtyService.get_specialties(
        db=db,
        skip=skip,
        limit=limit,
        is_public=is_public,
        is_visible=is_visible,
        category=category
    )
    
    return specialties


@router.get("/specialties/{specialty_id}", response_model=SpecialtyResponse)
def get_specialty(
    specialty_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar especialidade por ID"""
    specialty = SpecialtyService.get_specialty_by_id(db, specialty_id)
    if not specialty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Especialidade não encontrada"
        )
    
    return specialty


@router.get("/specialties/slug/{slug}", response_model=SpecialtyResponse)
def get_specialty_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar especialidade por slug"""
    specialty = SpecialtyService.get_specialty_by_slug(db, slug)
    if not specialty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Especialidade não encontrada"
        )
    
    return specialty


@router.post("/{professional_id}/specialties", response_model=dict)
def add_specialty_to_professional(
    professional_id: UUID,
    specialty_data: ProfessionalSpecialtyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Adicionar especialidade ao profissional"""
    # Verificar se o usuário é o proprietário do perfil
    professional = ProfessionalService.get_professional_by_id(db, professional_id)
    if not professional or professional.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este perfil"
        )
    
    professional_specialty = SpecialtyService.add_specialty_to_professional(
        db, professional_id, specialty_data.specialty_id
    )
    
    if not professional_specialty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao adicionar especialidade"
        )
    
    return {"message": "Especialidade adicionada com sucesso"}


@router.delete("/{professional_id}/specialties/{specialty_id}")
def remove_specialty_from_professional(
    professional_id: UUID,
    specialty_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remover especialidade do profissional"""
    # Verificar se o usuário é o proprietário do perfil
    professional = ProfessionalService.get_professional_by_id(db, professional_id)
    if not professional or professional.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este perfil"
        )
    
    success = SpecialtyService.remove_specialty_from_professional(
        db, professional_id, specialty_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Especialidade não encontrada para este profissional"
        )
    
    return {"message": "Especialidade removida com sucesso"}


# Rotas para Profession
@router.get("/professions", response_model=List[ProfessionResponse])
def list_professions(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar profissões com filtros opcionais"""
    professions = ProfessionService.get_professions(
        db=db,
        skip=skip,
        limit=limit,
        is_active=is_active
    )
    
    return professions


@router.post("/{professional_id}/professions", response_model=ProfessionalProfessionResponse)
def add_profession_to_professional(
    professional_id: UUID,
    profession_data: ProfessionalProfessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Adicionar profissão ao profissional"""
    # Verificar se o usuário é o proprietário do perfil
    professional = ProfessionalService.get_professional_by_id(db, professional_id)
    if not professional or professional.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este perfil"
        )
    
    profession_data.professional_id = professional_id
    professional_profession = ProfessionService.add_profession_to_professional(
        db, professional_id, profession_data
    )
    
    if not professional_profession:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao adicionar profissão"
        )
    
    return professional_profession


@router.put("/{professional_id}/professions/{profession_id}", response_model=ProfessionalProfessionResponse)
def update_professional_profession(
    professional_id: UUID,
    profession_id: UUID,
    profession_data: ProfessionalProfessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar profissão do profissional"""
    # Verificar se o usuário é o proprietário do perfil
    professional = ProfessionalService.get_professional_by_id(db, professional_id)
    if not professional or professional.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este perfil"
        )
    
    updated_profession = ProfessionService.update_professional_profession(
        db, professional_id, profession_id, profession_data
    )
    
    if not updated_profession:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissão não encontrada para este profissional"
        )
    
    return updated_profession


@router.delete("/{professional_id}/professions/{profession_id}")
def remove_profession_from_professional(
    professional_id: UUID,
    profession_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remover profissão do profissional"""
    # Verificar se o usuário é o proprietário do perfil
    professional = ProfessionalService.get_professional_by_id(db, professional_id)
    if not professional or professional.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este perfil"
        )
    
    success = ProfessionService.remove_profession_from_professional(
        db, professional_id, profession_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissão não encontrada para este profissional"
        )
    
    return {"message": "Profissão removida com sucesso"}


@router.post("/{professional_id}/professions/{profession_id}/primary")
def set_primary_profession(
    professional_id: UUID,
    profession_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Definir profissão como primária"""
    # Verificar se o usuário é o proprietário do perfil
    professional = ProfessionalService.get_professional_by_id(db, professional_id)
    if not professional or professional.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este perfil"
        )
    
    success = ProfessionService.set_primary_profession(
        db, professional_id, profession_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissão não encontrada para este profissional"
        )
    
    return {"message": "Profissão definida como primária com sucesso"} 