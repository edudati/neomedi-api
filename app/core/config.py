import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    SECRET_KEY: str
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str
    
    # Firebase settings
    FIREBASE_PROJECT_ID: str
    FIREBASE_API_KEY: str
    FIREBASE_AUTH_DOMAIN: str
    FIREBASE_STORAGE_BUCKET: str
    FIREBASE_MESSAGING_SENDER_ID: str
    FIREBASE_APP_ID: str
    
    # Firebase service account
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str
    FIREBASE_AUTH_URI: str
    FIREBASE_TOKEN_URI: str
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str
    FIREBASE_CLIENT_X509_CERT_URL: str
    
    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int
    
    # Redis settings
    REDIS_URL: str
    
    # CORS settings
    ALLOWED_ORIGINS: List[str]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


# Global instance of settings
settings = Settings()
