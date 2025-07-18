from pydantic_settings import BaseSettings
from typing import Optional
import json
import os


class Settings(BaseSettings):
    # Database
    database_url: Optional[str] = None
    
    # Firebase (Fase 2)
    firebase_credentials: Optional[str] = None
    firebase_project_id: Optional[str] = None
    firebase_private_key_id: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_client_email: Optional[str] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_firebase_credentials()
    
    def _load_firebase_credentials(self):
        """Carrega credenciais do Firebase do arquivo JSON"""
        firebase_json_path = self.firebase_credentials or "firebase_service_account.json"
        if firebase_json_path and os.path.exists(firebase_json_path):
            try:
                with open(firebase_json_path, 'r') as f:
                    firebase_creds = json.load(f)
                
                self.firebase_project_id = firebase_creds.get('project_id')
                self.firebase_private_key_id = firebase_creds.get('private_key_id')
                self.firebase_private_key = firebase_creds.get('private_key')
                self.firebase_client_email = firebase_creds.get('client_email')
            except Exception as e:
                print(f"Erro ao carregar credenciais Firebase: {e}")
    
    # JWT (Fase 2)
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    app_name: str = "Neomedi API"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignora campos extras no .env


settings = Settings() 