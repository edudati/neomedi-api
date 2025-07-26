#!/usr/bin/env python3
"""
Script de teste para verificar a estrutura do JWT
"""

import jwt
import json
from datetime import datetime, timedelta

# Dados de exemplo (substitua pelos dados reais do seu sistema)
JWT_SECRET_KEY = "your-secret-key-here"
JWT_ALGORITHM = "HS256"

def create_test_jwt():
    """Cria um JWT de teste com a estrutura esperada"""
    
    # Dados do usuário (exemplo)
    user_data = {
        "id": 1,
        "firebase_uid": "firebase_uid_example",
        "email": "user@example.com",
        "name": "João Silva",
        "user_uid": "550e8400-e29b-41d4-a716-446655440000",
        "display_name": "João Silva",
        "email_verified": True,
        "picture": "https://example.com/photo.jpg",
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    
    # Criar JWT
    token = jwt.encode(user_data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    print("🔐 JWT Token criado:")
    print(token)
    print("\n" + "="*50)
    
    # Decodificar para verificar
    try:
        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        print("📋 JWT Decodificado:")
        print(json.dumps(decoded, indent=2, default=str))
        
        print("\n" + "="*50)
        print("✅ Informações principais:")
        print(f"Email: {decoded.get('email')}")
        print(f"Name: {decoded.get('name')}")
        print(f"User UID: {decoded.get('user_uid')}")
        print(f"Firebase UID: {decoded.get('firebase_uid')}")
        
    except jwt.ExpiredSignatureError:
        print("❌ Token expirado")
    except jwt.InvalidTokenError as e:
        print(f"❌ Token inválido: {e}")

def decode_jwt_manual(token):
    """Decodifica JWT manualmente (como seria no frontend)"""
    try:
        # Separar as partes do JWT
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("JWT deve ter 3 partes")
        
        # Decodificar o payload (parte do meio)
        import base64
        import urllib.parse
        
        # Adicionar padding se necessário
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        
        # Decodificar base64
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Parse JSON
        payload_data = json.loads(decoded_str)
        
        print("\n🔍 Decodificação manual (como no frontend):")
        print(json.dumps(payload_data, indent=2, default=str))
        
        return payload_data
        
    except Exception as e:
        print(f"❌ Erro na decodificação manual: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testando estrutura do JWT")
    print("="*50)
    
    # Criar JWT de teste
    test_token = create_test_jwt()
    
    # Decodificar manualmente
    decode_jwt_manual(test_token)
    
    print("\n" + "="*50)
    print("✅ Teste concluído!")
    print("\n📝 Para usar no frontend:")
    print("1. Instale: npm install jwt-decode")
    print("2. Use: const decoded = jwtDecode(token)")
    print("3. Acesse: decoded.email, decoded.name, decoded.user_uid") 