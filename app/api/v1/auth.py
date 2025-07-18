from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import SignupRequest, SignupResponse
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.services.auth_service import FirebaseAuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    """
    Endpoint para criar novo usuário
    """
    # Verificar se usuário já existe com mensagem específica
    existing_info = UserService.get_existing_user_info(db, user_data.email, user_data.firebase_uid)
    if existing_info["error"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=existing_info["error"]
        )
    
    # Validação obrigatória do Firebase via token
    try:
        firebase_service = FirebaseAuthService()
        
        # Verificar token do Firebase
        token_data = firebase_service.verify_firebase_token(user_data.firebase_token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token do Firebase inválido"
            )
        
        # Verificar se o UID do token corresponde ao enviado
        if token_data['uid'] != user_data.firebase_uid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Firebase UID não corresponde ao token"
            )
        
        # Verificar se o email do token corresponde ao enviado
        if token_data['email'] != user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email não corresponde ao token do Firebase"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao verificar usuário no Firebase"
        )
    
    # Criar usuário
    user_create = UserCreate(email=user_data.email, firebase_uid=user_data.firebase_uid)
    new_user = UserService.create_user(db, user_create)
    
    return SignupResponse(
        id=new_user.id,
        email=new_user.email,
        firebase_uid=new_user.firebase_uid,
        created_at=new_user.created_at,
        is_active=new_user.is_active,
        message="Usuário criado com sucesso"
    ) 