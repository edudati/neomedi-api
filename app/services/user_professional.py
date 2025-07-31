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

    @staticmethod
    def create_user_professional(db: Session, firebase_token: str, company_name: str, address_fields=None, **user_fields) -> UserProfessional:
        from app.services.auth import AuthService
        from app.services.user import UserService
        from app.services.company import CompanyService
        from app.services.address import AddressService
        from app.models.user import UserRole
        
        print("1. Iniciando criação de user professional...")
        
        # 1. Cria AuthUser
        auth_user = AuthService.create_auth_user_from_firebase(db, firebase_token)
        print(f"2. AuthUser criado: {auth_user.id}")
        
        # 2. Cria User com role PROFESSIONAL
        user = UserService.create_user(db, auth_user, UserRole.PROFESSIONAL, **user_fields)
        print(f"3. User criado: {user.id}")
        
        # 3. Cria Address em branco para o User
        AddressService.create_address(db, user_id=user.id, street="", number="", neighbourhood="", city="", state="", zip_code="", country="Brasil")
        print("4. Address do User criado")
        
        # 4. Cria UserProfessional em branco vinculado ao User
        user_professional = UserProfessional(user_id=user.id)
        db.add(user_professional)
        db.commit()
        db.refresh(user_professional)
        print(f"5. UserProfessional criado: {user_professional.user_id}")
        
        # 5. Cria Company vinculada ao UserProfessional
        company = CompanyService.create_company(db, name=company_name, user_professional_id=user_professional.user_id, address_fields={
            "street": "",
            "number": "",
            "neighbourhood": "",
            "city": "",
            "state": "",
            "zip_code": "",
            "country": "Brasil"
        })
        print(f"6. Company criada: {company.id}")
        
        return user_professional 