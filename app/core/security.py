import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import firebase_admin
from firebase_admin import credentials, auth
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

# Inicializar Firebase Admin SDK
def initialize_firebase():
    """Inicializa o Firebase Admin SDK com as credenciais do service account"""
    try:
        # Configuração do service account
        service_account_info = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "client_id": settings.FIREBASE_CLIENT_ID,
            "auth_uri": settings.FIREBASE_AUTH_URI,
            "token_uri": settings.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL
        }
        
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin SDK inicializado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar Firebase: {e}")
        raise

# Verificar token Firebase
def verify_firebase_token(firebase_token: str) -> Dict[str, Any]:
    """Verifica um token do Firebase e retorna os dados do usuário"""
    try:
        # Verificar se Firebase está inicializado
        if not firebase_admin._apps:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Firebase não está configurado"
            )
        
        decoded_token = auth.verify_id_token(firebase_token)
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
            "firebase_claims": decoded_token
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token Firebase inválido: {str(e)}"
        )

# Criar JWT local
def create_jwt_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Cria um JWT token local"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

# Verificar JWT local
def verify_jwt_token(token: str) -> Dict[str, Any]:
    """Verifica um JWT token local"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token JWT inválido"
        )

# Criar refresh token
def create_refresh_token(data: Dict[str, Any]) -> str:
    """Cria um refresh token com expiração mais longa"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

# Dependência para extrair token do header
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependência para obter o usuário atual baseado no token"""
    token = credentials.credentials
    
    # Primeiro tenta verificar como JWT local
    try:
        payload = verify_jwt_token(token)
        return payload
    except HTTPException:
        # Se falhar, tenta como token Firebase
        try:
            user_data = verify_firebase_token(token)
            # Cria um JWT local a partir do token Firebase
            jwt_token = create_jwt_token(user_data)
            return {"user": user_data, "jwt_token": jwt_token}
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

# Função para renovar token
def refresh_access_token(refresh_token: str) -> str:
    """Renova um access token usando um refresh token"""
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token não é um refresh token"
            )
        
        # Remove campos específicos do refresh token
        user_data = {k: v for k, v in payload.items() if k not in ["exp", "type"]}
        
        # Cria novo access token
        return create_jwt_token(user_data)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido"
        )

# Inicializar Firebase quando o módulo for importado
try:
    initialize_firebase()
except Exception as e:
    print(f"⚠️ Firebase não inicializado: {e}")
    print("⚠️ A aplicação continuará funcionando, mas autenticação Firebase não estará disponível")
