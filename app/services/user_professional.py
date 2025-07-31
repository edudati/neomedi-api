from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user_professional import UserProfessional
from app.models.user import UserRole
from app.schemas.user_professional import UserProfessionalUpdate

class UserProfessionalService:
    @staticmethod
    def get_by_user_id(db: Session, user_id: UUID):
        return db.query(UserProfessional).filter(UserProfessional.user_id == user_id).first()

    @staticmethod
    def edit_user_professional(db: Session, user_id: UUID, update_data: UserProfessionalUpdate, current_user):
        if current_user.role != UserRole.PROFESSIONAL:
            raise PermissionError("Apenas profissionais podem editar o perfil profissional.")
        prof = db.query(UserProfessional).filter(UserProfessional.user_id == user_id).first()
        if not prof:
            raise ValueError("Perfil profissional não encontrado.")
        update_fields = update_data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(prof, field, value)
        db.commit()
        db.refresh(prof)
        return prof 