from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
import uuid
from app.models.user_assistant import UserAssistant, AssistantClinic, AssistantProfessional
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.professional import Professional
from app.schemas.user_assistant import (
    UserAssistantCreate, UserAssistantUpdate,
    AssistantClinicCreate, AssistantClinicUpdate,
    AssistantProfessionalCreate, AssistantProfessionalUpdate
)
from fastapi import HTTPException, status


class UserAssistantService:
    """Serviço para operações com UserAssistant"""

    @staticmethod
    def create_user_assistant(db: Session, user_assistant_data: UserAssistantCreate) -> UserAssistant:
        """Cria um novo UserAssistant"""
        # Verifica se o usuário existe e tem role ASSISTANT
        user = db.query(User).filter(User.id == user_assistant_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        if user.role != UserRole.ASSISTANT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas usuários com role ASSISTANT podem ter UserAssistant"
            )

        # Verifica se já existe um UserAssistant para este usuário
        existing_assistant = db.query(UserAssistant).filter(
            UserAssistant.user_id == user_assistant_data.user_id
        ).first()
        
        if existing_assistant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um UserAssistant para este usuário"
            )

        user_assistant = UserAssistant(**user_assistant_data.model_dump())
        db.add(user_assistant)
        db.commit()
        db.refresh(user_assistant)
        return user_assistant

    @staticmethod
    def get_user_assistant_by_id(db: Session, assistant_id: uuid.UUID) -> Optional[UserAssistant]:
        """Busca um UserAssistant por ID"""
        return db.query(UserAssistant).filter(UserAssistant.id == assistant_id).first()

    @staticmethod
    def get_user_assistant_by_user_id(db: Session, user_id: uuid.UUID) -> Optional[UserAssistant]:
        """Busca um UserAssistant por user_id"""
        return db.query(UserAssistant).filter(UserAssistant.user_id == user_id).first()

    @staticmethod
    def get_user_assistants(db: Session, skip: int = 0, limit: int = 100) -> List[UserAssistant]:
        """Lista todos os UserAssistants"""
        return db.query(UserAssistant).offset(skip).limit(limit).all()

    @staticmethod
    def update_user_assistant(
        db: Session, 
        assistant_id: uuid.UUID, 
        user_assistant_data: UserAssistantUpdate
    ) -> Optional[UserAssistant]:
        """Atualiza um UserAssistant"""
        user_assistant = db.query(UserAssistant).filter(UserAssistant.id == assistant_id).first()
        if not user_assistant:
            return None

        update_data = user_assistant_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user_assistant, field, value)

        db.commit()
        db.refresh(user_assistant)
        return user_assistant

    @staticmethod
    def delete_user_assistant(db: Session, assistant_id: uuid.UUID) -> bool:
        """Remove um UserAssistant"""
        user_assistant = db.query(UserAssistant).filter(UserAssistant.id == assistant_id).first()
        if not user_assistant:
            return False

        db.delete(user_assistant)
        db.commit()
        return True

    @staticmethod
    def get_user_assistant_with_details(db: Session, assistant_id: uuid.UUID) -> Optional[UserAssistant]:
        """Busca um UserAssistant com detalhes das clínicas e profissionais"""
        return db.query(UserAssistant).options(
            joinedload(UserAssistant.assistant_clinics).joinedload(AssistantClinic.company),
            joinedload(UserAssistant.assistant_professionals).joinedload(AssistantProfessional.professional).joinedload(Professional.user)
        ).filter(UserAssistant.id == assistant_id).first()


class AssistantClinicService:
    """Serviço para operações com AssistantClinic"""

    @staticmethod
    def add_clinic_to_assistant(
        db: Session, 
        assistant_id: uuid.UUID, 
        clinic_data: AssistantClinicCreate
    ) -> AssistantClinic:
        """Adiciona uma clínica a um assistente"""
        # Verifica se o assistente existe
        assistant = db.query(UserAssistant).filter(UserAssistant.id == assistant_id).first()
        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assistente não encontrado"
            )

        # Verifica se a clínica existe
        company = db.query(Company).filter(Company.id == clinic_data.company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clínica não encontrada"
            )

        # Verifica se já existe a associação
        existing_association = db.query(AssistantClinic).filter(
            and_(
                AssistantClinic.assistant_id == assistant_id,
                AssistantClinic.company_id == clinic_data.company_id
            )
        ).first()

        if existing_association:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assistente já está vinculado a esta clínica"
            )

        assistant_clinic = AssistantClinic(
            assistant_id=assistant_id,
            **clinic_data.model_dump()
        )
        db.add(assistant_clinic)
        db.commit()
        db.refresh(assistant_clinic)
        return assistant_clinic

    @staticmethod
    def update_assistant_clinic(
        db: Session,
        assistant_id: uuid.UUID,
        company_id: uuid.UUID,
        clinic_data: AssistantClinicUpdate
    ) -> Optional[AssistantClinic]:
        """Atualiza uma associação assistente-clínica"""
        assistant_clinic = db.query(AssistantClinic).filter(
            and_(
                AssistantClinic.assistant_id == assistant_id,
                AssistantClinic.company_id == company_id
            )
        ).first()

        if not assistant_clinic:
            return None

        update_data = clinic_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assistant_clinic, field, value)

        db.commit()
        db.refresh(assistant_clinic)
        return assistant_clinic

    @staticmethod
    def remove_clinic_from_assistant(
        db: Session, 
        assistant_id: uuid.UUID, 
        company_id: uuid.UUID
    ) -> bool:
        """Remove uma clínica de um assistente"""
        assistant_clinic = db.query(AssistantClinic).filter(
            and_(
                AssistantClinic.assistant_id == assistant_id,
                AssistantClinic.company_id == company_id
            )
        ).first()

        if not assistant_clinic:
            return False

        db.delete(assistant_clinic)
        db.commit()
        return True

    @staticmethod
    def get_assistant_clinics(db: Session, assistant_id: uuid.UUID) -> List[AssistantClinic]:
        """Lista todas as clínicas de um assistente"""
        return db.query(AssistantClinic).options(
            joinedload(AssistantClinic.company)
        ).filter(AssistantClinic.assistant_id == assistant_id).all()

    @staticmethod
    def can_assistant_admin_clinic(db: Session, assistant_id: uuid.UUID, company_id: uuid.UUID) -> bool:
        """Verifica se um assistente tem permissão de admin para uma clínica"""
        assistant_clinic = db.query(AssistantClinic).filter(
            and_(
                AssistantClinic.assistant_id == assistant_id,
                AssistantClinic.company_id == company_id,
                AssistantClinic.is_admin == True
            )
        ).first()
        return assistant_clinic is not None


class AssistantProfessionalService:
    """Serviço para operações com AssistantProfessional"""

    @staticmethod
    def add_professional_to_assistant(
        db: Session, 
        assistant_id: uuid.UUID, 
        professional_data: AssistantProfessionalCreate
    ) -> AssistantProfessional:
        """Adiciona um profissional a um assistente"""
        # Verifica se o assistente existe
        assistant = db.query(UserAssistant).filter(UserAssistant.id == assistant_id).first()
        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assistente não encontrado"
            )

        # Verifica se o profissional existe
        professional = db.query(Professional).filter(Professional.id == professional_data.professional_id).first()
        if not professional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profissional não encontrado"
            )

        # Verifica se já existe a associação
        existing_association = db.query(AssistantProfessional).filter(
            and_(
                AssistantProfessional.assistant_id == assistant_id,
                AssistantProfessional.professional_id == professional_data.professional_id
            )
        ).first()

        if existing_association:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assistente já está vinculado a este profissional"
            )

        assistant_professional = AssistantProfessional(
            assistant_id=assistant_id,
            **professional_data.model_dump()
        )
        db.add(assistant_professional)
        db.commit()
        db.refresh(assistant_professional)
        return assistant_professional

    @staticmethod
    def remove_professional_from_assistant(
        db: Session, 
        assistant_id: uuid.UUID, 
        professional_id: uuid.UUID
    ) -> bool:
        """Remove um profissional de um assistente"""
        assistant_professional = db.query(AssistantProfessional).filter(
            and_(
                AssistantProfessional.assistant_id == assistant_id,
                AssistantProfessional.professional_id == professional_id
            )
        ).first()

        if not assistant_professional:
            return False

        db.delete(assistant_professional)
        db.commit()
        return True

    @staticmethod
    def get_assistant_professionals(db: Session, assistant_id: uuid.UUID) -> List[AssistantProfessional]:
        """Lista todos os profissionais de um assistente"""
        return db.query(AssistantProfessional).options(
            joinedload(AssistantProfessional.professional).joinedload(Professional.user)
        ).filter(AssistantProfessional.assistant_id == assistant_id).all()

    @staticmethod
    def get_professional_assistants(db: Session, professional_id: uuid.UUID) -> List[AssistantProfessional]:
        """Lista todos os assistentes de um profissional"""
        return db.query(AssistantProfessional).options(
            joinedload(AssistantProfessional.assistant).joinedload(UserAssistant.user)
        ).filter(AssistantProfessional.professional_id == professional_id).all() 