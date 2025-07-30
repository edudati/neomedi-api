from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.professional import Professional
from app.models.specialty import Specialty, ProfessionalSpecialty
from app.models.profession import Profession, ProfessionalProfession
from app.models.user import User, UserRole
from app.schemas.professional import ProfessionalCreate, ProfessionalUpdate
from app.schemas.specialty import SpecialtyCreate, ProfessionalSpecialtyCreate
from app.schemas.profession import ProfessionalProfessionCreate, ProfessionalProfessionUpdate


class ProfessionalService:
    """Serviço para gerenciar profissionais de saúde"""

    @staticmethod
    def create_professional(db: Session, professional_data: ProfessionalCreate) -> Professional:
        """Criar novo profissional"""
        db_professional = Professional(**professional_data.dict())
        db.add(db_professional)
        db.commit()
        db.refresh(db_professional)
        return db_professional

    @staticmethod
    def get_professional_by_id(db: Session, professional_id: UUID) -> Optional[Professional]:
        """Buscar profissional por ID"""
        return db.query(Professional).filter(Professional.id == professional_id).first()

    @staticmethod
    def get_professional_by_user_id(db: Session, user_id: UUID) -> Optional[Professional]:
        """Buscar profissional por user_id"""
        return db.query(Professional).filter(Professional.user_id == user_id).first()

    @staticmethod
    def get_professionals(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        profile_completed: Optional[bool] = None
    ) -> List[Professional]:
        """Listar profissionais com filtros opcionais"""
        query = db.query(Professional)
        
        if profile_completed is not None:
            query = query.filter(Professional.profile_completed == profile_completed)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_professional(db: Session, professional_id: UUID, professional_data: ProfessionalUpdate) -> Optional[Professional]:
        """Atualizar profissional"""
        db_professional = ProfessionalService.get_professional_by_id(db, professional_id)
        if not db_professional:
            return None
        
        update_data = professional_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_professional, field, value)
        
        db_professional.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_professional)
        return db_professional

    @staticmethod
    def get_professional_with_details(db: Session, professional_id: UUID) -> Optional[dict]:
        """Buscar profissional com especialidades e profissões"""
        db_professional = db.query(Professional).filter(Professional.id == professional_id).first()
        if not db_professional:
            return None
        
        # Buscar especialidades
        specialties = []
        for ps in db_professional.specialties:
            specialties.append({
                "id": ps.specialty.id,
                "name": ps.specialty.name,
                "slug": ps.specialty.slug,
                "category": ps.specialty.category,
                "description": ps.specialty.description,
                "is_public": ps.specialty.is_public,
                "is_visible": ps.specialty.is_visible,
                "created_at": ps.created_at
            })
        
        # Buscar profissões
        professions = []
        for pp in db_professional.professions:
            professions.append({
                "id": pp.profession.id,
                "name": pp.profession.name,
                "cbo_code": pp.profession.cbo_code,
                "council_type": pp.profession.council_type,
                "council_number": pp.council_number,
                "council_uf": pp.council_uf,
                "rqe_type": pp.rqe_type,
                "is_primary": pp.is_primary,
                "created_at": pp.created_at
            })
        
        return {
            "id": db_professional.id,
            "user_id": db_professional.user_id,
            "treatment_title": db_professional.treatment_title,
            "profile_completed": db_professional.profile_completed,
            "bio": db_professional.bio,
            "created_at": db_professional.created_at,
            "updated_at": db_professional.updated_at,
            "user": {
                "id": db_professional.user.id,
                "name": db_professional.user.name,
                "role": db_professional.user.role.value
            },
            "specialties": specialties,
            "professions": professions
        }


class SpecialtyService:
    """Serviço para gerenciar especialidades"""

    @staticmethod
    def create_specialty(db: Session, specialty_data: SpecialtyCreate) -> Specialty:
        """Criar nova especialidade"""
        # Verificar se o slug já existe
        existing_slug = db.query(Specialty).filter(Specialty.slug == specialty_data.slug).first()
        if existing_slug:
            raise ValueError(f"Slug '{specialty_data.slug}' já existe")
        
        # Verificar se o nome já existe
        existing_name = db.query(Specialty).filter(Specialty.name == specialty_data.name).first()
        if existing_name:
            raise ValueError(f"Nome '{specialty_data.name}' já existe")
        
        db_specialty = Specialty(**specialty_data.dict())
        db.add(db_specialty)
        db.commit()
        db.refresh(db_specialty)
        return db_specialty

    @staticmethod
    def get_specialty_by_id(db: Session, specialty_id: UUID) -> Optional[Specialty]:
        """Buscar especialidade por ID"""
        return db.query(Specialty).filter(Specialty.id == specialty_id).first()

    @staticmethod
    def get_specialty_by_slug(db: Session, slug: str) -> Optional[Specialty]:
        """Buscar especialidade por slug"""
        return db.query(Specialty).filter(Specialty.slug == slug).first()

    @staticmethod
    def get_specialties(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        is_public: Optional[bool] = None,
        is_visible: Optional[bool] = None,
        category: Optional[str] = None
    ) -> List[Specialty]:
        """Listar especialidades com filtros opcionais"""
        query = db.query(Specialty)
        
        if is_public is not None:
            query = query.filter(Specialty.is_public == is_public)
        
        if is_visible is not None:
            query = query.filter(Specialty.is_visible == is_visible)
        
        if category:
            query = query.filter(Specialty.category == category)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_specialty(db: Session, specialty_id: UUID, specialty_data: dict) -> Optional[Specialty]:
        """Atualizar especialidade"""
        db_specialty = SpecialtyService.get_specialty_by_id(db, specialty_id)
        if not db_specialty:
            return None
        
        for field, value in specialty_data.items():
            setattr(db_specialty, field, value)
        
        db_specialty.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_specialty)
        return db_specialty

    @staticmethod
    def add_specialty_to_professional(db: Session, professional_id: UUID, specialty_id: UUID) -> Optional[ProfessionalSpecialty]:
        """Adicionar especialidade ao profissional"""
        # Verificar se já existe
        existing = db.query(ProfessionalSpecialty).filter(
            and_(
                ProfessionalSpecialty.professional_id == professional_id,
                ProfessionalSpecialty.specialty_id == specialty_id
            )
        ).first()
        
        if existing:
            return existing
        
        db_professional_specialty = ProfessionalSpecialty(
            professional_id=professional_id,
            specialty_id=specialty_id
        )
        db.add(db_professional_specialty)
        db.commit()
        db.refresh(db_professional_specialty)
        return db_professional_specialty

    @staticmethod
    def remove_specialty_from_professional(db: Session, professional_id: UUID, specialty_id: UUID) -> bool:
        """Remover especialidade do profissional"""
        db_professional_specialty = db.query(ProfessionalSpecialty).filter(
            and_(
                ProfessionalSpecialty.professional_id == professional_id,
                ProfessionalSpecialty.specialty_id == specialty_id
            )
        ).first()
        
        if not db_professional_specialty:
            return False
        
        db.delete(db_professional_specialty)
        db.commit()
        return True


class ProfessionService:
    """Serviço para gerenciar profissões"""

    @staticmethod
    def create_profession(db: Session, profession_data: dict) -> Profession:
        """Criar nova profissão"""
        db_profession = Profession(**profession_data)
        db.add(db_profession)
        db.commit()
        db.refresh(db_profession)
        return db_profession

    @staticmethod
    def get_profession_by_id(db: Session, profession_id: UUID) -> Optional[Profession]:
        """Buscar profissão por ID"""
        return db.query(Profession).filter(Profession.id == profession_id).first()

    @staticmethod
    def get_professions(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Profession]:
        """Listar profissões com filtros opcionais"""
        query = db.query(Profession)
        
        if is_active is not None:
            query = query.filter(Profession.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def add_profession_to_professional(db: Session, professional_id: UUID, profession_data: ProfessionalProfessionCreate) -> Optional[ProfessionalProfession]:
        """Adicionar profissão ao profissional"""
        # Verificar se já existe
        existing = db.query(ProfessionalProfession).filter(
            and_(
                ProfessionalProfession.professional_id == professional_id,
                ProfessionalProfession.profession_id == profession_data.profession_id
            )
        ).first()
        
        if existing:
            return existing
        
        # Se for a primeira profissão, definir como primária
        existing_professions = db.query(ProfessionalProfession).filter(
            ProfessionalProfession.professional_id == professional_id
        ).count()
        
        if existing_professions == 0:
            profession_data.is_primary = True
        
        db_professional_profession = ProfessionalProfession(**profession_data.dict())
        db.add(db_professional_profession)
        db.commit()
        db.refresh(db_professional_profession)
        return db_professional_profession

    @staticmethod
    def update_professional_profession(db: Session, professional_id: UUID, profession_id: UUID, profession_data: ProfessionalProfessionUpdate) -> Optional[ProfessionalProfession]:
        """Atualizar profissão do profissional"""
        db_professional_profession = db.query(ProfessionalProfession).filter(
            and_(
                ProfessionalProfession.professional_id == professional_id,
                ProfessionalProfession.profession_id == profession_id
            )
        ).first()
        
        if not db_professional_profession:
            return None
        
        update_data = profession_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_professional_profession, field, value)
        
        db_professional_profession.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_professional_profession)
        return db_professional_profession

    @staticmethod
    def remove_profession_from_professional(db: Session, professional_id: UUID, profession_id: UUID) -> bool:
        """Remover profissão do profissional"""
        db_professional_profession = db.query(ProfessionalProfession).filter(
            and_(
                ProfessionalProfession.professional_id == professional_id,
                ProfessionalProfession.profession_id == profession_id
            )
        ).first()
        
        if not db_professional_profession:
            return False
        
        # Se for a profissão primária e houver outras, definir a próxima como primária
        if db_professional_profession.is_primary:
            other_professions = db.query(ProfessionalProfession).filter(
                and_(
                    ProfessionalProfession.professional_id == professional_id,
                    ProfessionalProfession.profession_id != profession_id
                )
            ).all()
            
            if other_professions:
                # Definir a primeira como primária
                other_professions[0].is_primary = True
                other_professions[0].updated_at = datetime.utcnow()
        
        db.delete(db_professional_profession)
        db.commit()
        return True

    @staticmethod
    def set_primary_profession(db: Session, professional_id: UUID, profession_id: UUID) -> bool:
        """Definir profissão como primária"""
        # Remover primária de todas as profissões do profissional
        db.query(ProfessionalProfession).filter(
            ProfessionalProfession.professional_id == professional_id
        ).update({"is_primary": False, "updated_at": datetime.utcnow()})
        
        # Definir a nova como primária
        db_professional_profession = db.query(ProfessionalProfession).filter(
            and_(
                ProfessionalProfession.professional_id == professional_id,
                ProfessionalProfession.profession_id == profession_id
            )
        ).first()
        
        if not db_professional_profession:
            return False
        
        db_professional_profession.is_primary = True
        db_professional_profession.updated_at = datetime.utcnow()
        db.commit()
        return True 