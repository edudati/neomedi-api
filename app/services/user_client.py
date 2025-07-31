from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user_client import UserClient
from app.models.client_professional_company import ClientProfessionalCompany
from app.models.user import UserRole

class UserClientService:
    @staticmethod
    def create_user_client(
        db: Session, 
        firebase_token: str, 
        professional_id: UUID, 
        company_id: UUID, 
        address_fields=None, 
        **user_fields
    ) -> UserClient:
        from app.services.auth import AuthService
        from app.services.user import UserService
        from app.services.address import AddressService
        
        # 1. Cria AuthUser
        auth_user = AuthService.create_auth_user_from_firebase(db, firebase_token)
        
        # 2. Cria User com role CLIENT
        user = UserService.create_user(db, auth_user, UserRole.CLIENT, **user_fields)
        
        # 3. Cria Address para o User (sempre em branco)
        AddressService.create_address(db, user_id=user.id, street="", number="", neighbourhood="", city="", state="", zip_code="", country="Brasil")
        
        # 4. Cria UserClient em branco vinculado ao User
        user_client = UserClient(user_id=user.id)
        db.add(user_client)
        db.commit()
        db.refresh(user_client)
        
        # 5. Cria associação ClientProfessionalCompany
        client_professional_company = ClientProfessionalCompany(
            client_id=user_client.user_id,
            professional_id=professional_id,
            company_id=company_id
        )
        db.add(client_professional_company)
        db.commit()
        
        return user_client 