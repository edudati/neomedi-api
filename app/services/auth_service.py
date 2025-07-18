import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import settings
from typing import Optional


class FirebaseAuthService:
    def __init__(self):
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Inicializa o Firebase Admin SDK"""
        try:
            # Verificar se já foi inicializado
            firebase_admin.get_app()
        except ValueError:
            # Inicializar com arquivo de credenciais
            from app.core.config import settings
            firebase_json_path = settings.firebase_credentials or "firebase_service_account.json"
            cred = credentials.Certificate(firebase_json_path)
            firebase_admin.initialize_app(cred)
    
    def verify_firebase_token(self, id_token: str) -> Optional[dict]:
        """Verifica um token do Firebase e retorna os dados do usuário"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return {
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email'),
                'email_verified': decoded_token.get('email_verified', False)
            }
        except Exception as e:
            print(f"Erro ao verificar token Firebase: {e}")
            return None
    
    def get_user_by_uid(self, uid: str) -> Optional[dict]:
        """Busca usuário no Firebase por UID"""
        try:
            user_record = auth.get_user(uid)
            return {
                'uid': user_record.uid,
                'email': user_record.email,
                'email_verified': user_record.email_verified
            }
        except Exception as e:
            print(f"Erro ao buscar usuário Firebase: {e}")
            return None 