from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.db.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User, UserRole
from app.models.user_assistant import UserAssistant
from app.schemas.user_assistant import (
    UserAssistantCreate, UserAssistantUpdate, UserAssistantResponse, UserAssistantWithDetailsResponse,
    AssistantClinicCreate, AssistantClinicUpdate, AssistantClinicResponse, AssistantClinicWithDetailsResponse,
    AssistantProfessionalCreate, AssistantProfessionalResponse, AssistantProfessionalWithDetailsResponse
)
from app.services.user_assistant_service import UserAssistantService, AssistantClinicService, AssistantProfessionalService

router = APIRouter()

# Endpoints para UserAssistant
@router.post("/", response_model=UserAssistantResponse, status_code=status.HTTP_201_CREATED)
def create_user_assistant(
    user_assistant_data: UserAssistantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria um novo UserAssistant"""
    # Verifica se o usuário atual tem permissão (SUPER ou ADMIN)
    if current_user.role not in [UserRole.SUPER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas usuários SUPER ou ADMIN podem criar UserAssistant"
        )
    
    return UserAssistantService.create_user_assistant(db, user_assistant_data)

@router.get("/{assistant_id}", response_model=UserAssistantResponse)
def get_user_assistant(
    assistant_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca um UserAssistant por ID"""
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem ver
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este UserAssistant"
        )
    
    return user_assistant

@router.get("/user/{user_id}", response_model=UserAssistantResponse)
def get_user_assistant_by_user_id(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca um UserAssistant por user_id"""
    user_assistant = UserAssistantService.get_user_assistant_by_user_id(db, user_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio usuário, SUPER ou ADMIN podem ver
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este UserAssistant"
        )
    
    return user_assistant

@router.get("/{assistant_id}/details", response_model=UserAssistantWithDetailsResponse)
def get_user_assistant_with_details(
    assistant_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Busca um UserAssistant com detalhes das clínicas e profissionais"""
    user_assistant = UserAssistantService.get_user_assistant_with_details(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem ver
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este UserAssistant"
        )
    
    return user_assistant

@router.put("/{assistant_id}", response_model=UserAssistantResponse)
def update_user_assistant(
    assistant_id: uuid.UUID,
    user_assistant_data: UserAssistantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza um UserAssistant"""
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem editar
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar este UserAssistant"
        )
    
    updated_assistant = UserAssistantService.update_user_assistant(db, assistant_id, user_assistant_data)
    if not updated_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    return updated_assistant

@router.delete("/{assistant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_assistant(
    assistant_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove um UserAssistant"""
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas SUPER ou ADMIN podem remover
    if current_user.role not in [UserRole.SUPER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas usuários SUPER ou ADMIN podem remover UserAssistant"
        )
    
    success = UserAssistantService.delete_user_assistant(db, assistant_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )

# Endpoints para AssistantClinic
@router.post("/{assistant_id}/clinics", response_model=AssistantClinicResponse, status_code=status.HTTP_201_CREATED)
def add_clinic_to_assistant(
    assistant_id: uuid.UUID,
    clinic_data: AssistantClinicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Adiciona uma clínica a um assistente"""
    # Verifica se o assistente existe
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem adicionar clínicas
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para adicionar clínicas a este assistente"
        )
    
    return AssistantClinicService.add_clinic_to_assistant(db, assistant_id, clinic_data)

@router.get("/{assistant_id}/clinics", response_model=List[AssistantClinicWithDetailsResponse])
def get_assistant_clinics(
    assistant_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todas as clínicas de um assistente"""
    # Verifica se o assistente existe
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem ver
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para ver as clínicas deste assistente"
        )
    
    return AssistantClinicService.get_assistant_clinics(db, assistant_id)

@router.put("/{assistant_id}/clinics/{company_id}", response_model=AssistantClinicResponse)
def update_assistant_clinic(
    assistant_id: uuid.UUID,
    company_id: uuid.UUID,
    clinic_data: AssistantClinicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza uma associação assistente-clínica"""
    # Verifica se o assistente existe
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem editar
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar as clínicas deste assistente"
        )
    
    updated_clinic = AssistantClinicService.update_assistant_clinic(db, assistant_id, company_id, clinic_data)
    if not updated_clinic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação assistente-clínica não encontrada"
        )
    
    return updated_clinic

@router.delete("/{assistant_id}/clinics/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_clinic_from_assistant(
    assistant_id: uuid.UUID,
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove uma clínica de um assistente"""
    # Verifica se o assistente existe
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem remover
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para remover clínicas deste assistente"
        )
    
    success = AssistantClinicService.remove_clinic_from_assistant(db, assistant_id, company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação assistente-clínica não encontrada"
        )

# Endpoints para AssistantProfessional
@router.post("/{assistant_id}/professionals", response_model=AssistantProfessionalResponse, status_code=status.HTTP_201_CREATED)
def add_professional_to_assistant(
    assistant_id: uuid.UUID,
    professional_data: AssistantProfessionalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Adiciona um profissional a um assistente"""
    # Verifica se o assistente existe
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem adicionar profissionais
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para adicionar profissionais a este assistente"
        )
    
    return AssistantProfessionalService.add_professional_to_assistant(db, assistant_id, professional_data)

@router.get("/{assistant_id}/professionals", response_model=List[AssistantProfessionalWithDetailsResponse])
def get_assistant_professionals(
    assistant_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos os profissionais de um assistente"""
    # Verifica se o assistente existe
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem ver
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para ver os profissionais deste assistente"
        )
    
    return AssistantProfessionalService.get_assistant_professionals(db, assistant_id)

@router.delete("/{assistant_id}/professionals/{professional_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_professional_from_assistant(
    assistant_id: uuid.UUID,
    professional_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove um profissional de um assistente"""
    # Verifica se o assistente existe
    user_assistant = UserAssistantService.get_user_assistant_by_id(db, assistant_id)
    if not user_assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserAssistant não encontrado"
        )
    
    # Verifica permissão: apenas o próprio assistente, SUPER ou ADMIN podem remover
    if (current_user.role not in [UserRole.SUPER, UserRole.ADMIN] and 
        user_assistant.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para remover profissionais deste assistente"
        )
    
    success = AssistantProfessionalService.remove_professional_from_assistant(db, assistant_id, professional_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação assistente-profissional não encontrada"
        )

# Endpoint para listar assistentes de um profissional
@router.get("/professional/{professional_id}/assistants", response_model=List[AssistantProfessionalWithDetailsResponse])
def get_professional_assistants(
    professional_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos os assistentes de um profissional"""
    # Verifica permissão: apenas o próprio profissional, SUPER ou ADMIN podem ver
    if current_user.role not in [UserRole.SUPER, UserRole.ADMIN]:
        # Verifica se o profissional é o usuário atual
        professional = db.query(User).filter(User.id == professional_id).first()
        if not professional or professional.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para ver os assistentes deste profissional"
            )
    
    return AssistantProfessionalService.get_professional_assistants(db, professional_id) 