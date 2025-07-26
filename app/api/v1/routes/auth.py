from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import (
    verify_firebase_token,
    create_jwt_token,
    create_refresh_token,
    refresh_access_token,
    get_current_user
)
from app.core.config import settings
from app.db.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import (
    FirebaseTokenRequest,
    JWTTokenResponse,
    RefreshTokenRequest,
    LogoutResponse,
    TokenValidationResponse,
    UserInfo
)
from app.schemas.auth_user import (
    SignupRequest,
    SignupResponse,
    LoginResponse,
    AuthUserResponse
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=SignupResponse)
async def signup_with_firebase(
    request: SignupRequest,
    db: Session = Depends(get_db)
):
    """
    Signup usando token do Firebase.
    
    Fluxo:
    1. Recebe token do Firebase do frontend
    2. Verifica o token com Firebase
    3. Cria novo auth_user no banco
    4. Retorna dados do usuário criado + tokens JWT
    """
    print(f"🔐 Recebendo requisição de signup")
    try:
        print(f"🔐 Processando token Firebase...")
        # Processar token e criar/atualizar usuário + gerar tokens
        user, is_new_user, access_token, refresh_token = AuthService.process_firebase_token(db, request.firebase_token)
        
        if not is_new_user:
            print(f"⚠️ Usuário já existe")
            return SignupResponse(
                success=False,
                message="Usuário já existe. Use o endpoint /login",
                is_new_user=False
            )
        
        print(f"✅ Usuário criado com sucesso: {user.email}")
        return SignupResponse(
            success=True,
            message="Usuário criado com sucesso",
            user=AuthUserResponse.from_orm(user),
            is_new_user=True,
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except HTTPException as e:
        print(f"❌ HTTPException no signup: {e.detail}")
        return SignupResponse(
            success=False,
            message=f"Erro no signup: {e.detail}",
            is_new_user=False
        )
    except Exception as e:
        print(f"❌ Exception no signup: {str(e)}")
        return SignupResponse(
            success=False,
            message=f"Erro interno: {str(e)}",
            is_new_user=False
        )


@router.post("/login", response_model=LoginResponse)
async def login_with_firebase(
    request: FirebaseTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Login usando token do Firebase.
    
    Fluxo:
    1. Recebe token do Firebase do frontend
    2. Verifica o token com Firebase
    3. Busca/atualiza auth_user no banco
    4. Cria JWT local com expiração de 15 min
    5. Cria refresh token com expiração de 7 dias
    """
    try:
        # Processar token e buscar/atualizar usuário + gerar tokens
        user, is_new_user, access_token, refresh_token = AuthService.process_firebase_token(db, request.firebase_token)
        
        if is_new_user:
            return LoginResponse(
                success=False,
                message="Usuário não encontrado. Use o endpoint /signup primeiro",
                user=None
            )
        
        return LoginResponse(
            success=True,
            message="Login realizado com sucesso",
            user=AuthUserResponse.from_orm(user),
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except HTTPException as e:
        return LoginResponse(
            success=False,
            message=f"Erro no login: {e.detail}",
            user=None
        )
    except Exception as e:
        return LoginResponse(
            success=False,
            message=f"Erro interno: {str(e)}",
            user=None
        )


@router.post("/refresh", response_model=JWTTokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Renova o access token usando o refresh token.
    
    Usado quando o access token expira (a cada 15 min).
    """
    try:
        # Renovar access token
        new_access_token = refresh_access_token(request.refresh_token)
        
        # Decodificar o token para obter dados do usuário
        from app.core.security import verify_jwt_token
        user_data = verify_jwt_token(new_access_token)
        
        return JWTTokenResponse(
            access_token=new_access_token,
            refresh_token=request.refresh_token,  # Mantém o mesmo refresh token
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_data
        )
        
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout do usuário.
    
    No futuro, pode implementar blacklist de tokens.
    """
    return LogoutResponse(
        success=True,
        message="Logout realizado com sucesso"
    )


@router.get("/me", response_model=AuthUserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna informações do usuário atual.
    """
    # Buscar usuário no banco
    user = AuthService.get_user_by_firebase_uid(db, current_user.get("firebase_uid"))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return AuthUserResponse.from_orm(user)


@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(request: FirebaseTokenRequest):
    """
    Valida um token (Firebase ou JWT local).
    
    Útil para verificar se um token ainda é válido.
    """
    try:
        # Tentar validar como JWT local primeiro
        from app.core.security import verify_jwt_token
        user_data = verify_jwt_token(request.firebase_token)
        
        return TokenValidationResponse(
            valid=True,
            user=UserInfo(
                uid=user_data.get("firebase_uid"),
                email=user_data.get("email"),
                email_verified=user_data.get("email_verified", False),
                name=user_data.get("display_name"),
                picture=None
            ),
            message="Token JWT válido"
        )
        
    except HTTPException:
        try:
            # Tentar validar como token Firebase
            user_data = verify_firebase_token(request.firebase_token)
            
            return TokenValidationResponse(
                valid=True,
                user=UserInfo(
                    uid=user_data.get("uid"),
                    email=user_data.get("email"),
                    email_verified=user_data.get("email_verified", False),
                    name=user_data.get("name"),
                    picture=user_data.get("picture")
                ),
                message="Token Firebase válido"
            )
            
        except HTTPException:
            return TokenValidationResponse(
                valid=False,
                message="Token inválido"
            )


@router.get("/health")
async def auth_health_check():
    """
    Health check para o sistema de autenticação.
    """
    return {
        "status": "healthy",
        "service": "authentication",
        "firebase_project": settings.FIREBASE_PROJECT_ID,
        "jwt_algorithm": settings.JWT_ALGORITHM,
        "access_token_expiry": f"{settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES} minutes",
        "refresh_token_expiry": f"{settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS} days"
    } 