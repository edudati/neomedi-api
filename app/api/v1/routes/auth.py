from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.security import (
    verify_firebase_token,
    create_jwt_token,
    create_refresh_token,
    refresh_access_token,
    get_current_user
)
from app.core.config import settings
from app.db.database import get_db
from app.services.auth import AuthService
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
    Signup using Firebase token.
    """
    try:
        from app.services.user_professional import UserProfessionalService
        # Criar user professional completo
        user_professional = UserProfessionalService.create_user_professional(
            db=db,
            firebase_token=request.firebase_token,
            company_name="Empresa Padrão"  # Nome padrão para a empresa
        )
        
        # Buscar o AuthUser criado para gerar tokens
        from app.services.auth import AuthService
        auth_user = AuthService.get_user_by_firebase_uid(db, user_professional.user.auth_user.firebase_uid)
        access_token, refresh_token = AuthService.create_auth_tokens(auth_user, db)
        
        return SignupResponse(
            success=True,
            message="Signup successful",
            is_new_user=True,
            access_token=access_token,
            refresh_token=refresh_token,
            email_verified=auth_user.email_verified,
            is_active=auth_user.user.is_active if auth_user.user else True,
            created_at=auth_user.created_at
        )
    except HTTPException as e:
        return SignupResponse(
            success=False,
            message=f"Signup error: {e.detail}",
            is_new_user=False
        )
    except Exception as e:
        return SignupResponse(
            success=False,
            message=f"Internal error: {str(e)}",
            is_new_user=False
        )


@router.post("/login", response_model=LoginResponse)
async def login_with_firebase(
    request: FirebaseTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Login using Firebase token.
    
    Flow:
    1. Receive Firebase token from frontend
    2. Verify token with Firebase
    3. Search/update auth_user in database (create if not exists)
    4. Create local JWT with 15 min expiration
    5. Create refresh token with 7 days expiration
    """
    try:
        # Process token and search/update user + generate tokens
        user, is_new_user, access_token, refresh_token = AuthService.process_firebase_token(db, request.firebase_token)
        
        return LoginResponse(
            success=True,
            message="Login successful" if not is_new_user else "New user created during login",
            access_token=access_token,
            refresh_token=refresh_token,
            email_verified=user.email_verified,
            is_active=user.user.is_active if user.user else True,
            created_at=user.created_at
        )
        
    except HTTPException as e:
        return LoginResponse(
            success=False,
            message=f"Login error: {e.detail}"
        )
    except Exception as e:
        return LoginResponse(
            success=False,
            message=f"Internal error: {str(e)}"
        )


@router.post("/refresh", response_model=JWTTokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Renew access token using refresh token.
    
    Used when access token expires (every 15 min).
    """
    try:
        # Renew access token
        new_access_token = refresh_access_token(request.refresh_token)
        
        return JWTTokenResponse(
            access_token=new_access_token,
            refresh_token=request.refresh_token,  # Keep the same refresh token
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: dict = Depends(get_current_user)):
    """
    User Logout
    """
    return LogoutResponse(
        success=True,
        message="Logout successful"
    )


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Return current user information based on JWT.
    
    The frontend can use this endpoint to extract email, name and user_uid from JWT.
    """
    return UserInfo(
        uid=current_user.get("user_uid"),
        email=current_user.get("email"),
        email_verified=current_user.get("email_verified", False),
        name=current_user.get("name"),
        user_uid=current_user.get("user_uid"),
        picture=None
    )


@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(request: FirebaseTokenRequest):
    """
    Validate a token (Firebase or local JWT).
    
    Useful to check if a token is still valid.
    """
    try:
        # Try to validate as local JWT first
        from app.core.security import verify_jwt_token
        user_data = verify_jwt_token(request.firebase_token)
        
        return TokenValidationResponse(
            valid=True,
            user=UserInfo(
                uid=user_data.get("user_uid"),
                email=user_data.get("email"),
                email_verified=user_data.get("email_verified", False),
                name=user_data.get("name"),
                user_uid=user_data.get("user_uid"),
                picture=None
            ),
            message="Valid JWT token"
        )
        
    except HTTPException:
        try:
            # Try to validate as Firebase token
            user_data = verify_firebase_token(request.firebase_token)
            
            return TokenValidationResponse(
                valid=True,
                user=UserInfo(
                    uid=user_data.get("uid"),
                    email=user_data.get("email"),
                    email_verified=user_data.get("email_verified", False),
                    name=user_data.get("name"),
                    user_uid=None,  # Firebase doesn't have system user_uid
                    picture=user_data.get("picture")
                ),
                message="Valid Firebase token"
            )
            
        except HTTPException:
            return TokenValidationResponse(
                valid=False,
                message="Invalid token"
            )


@router.get("/health")
async def auth_health_check():
    """
    Health check for authentication system.
    """
    return {
        "status": "healthy",
        "service": "authentication",
        "firebase_project": settings.FIREBASE_PROJECT_ID,
        "jwt_algorithm": settings.JWT_ALGORITHM,
        "access_token_expiry": f"{settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES} minutes",
        "refresh_token_expiry": f"{settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS} days"
    } 