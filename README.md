# Neomedi API

API REST construída com FastAPI, PostgreSQL e autenticação Firebase.

## Estrutura do Projeto

```
neomedi-api/
├── app/
│   ├── core/           # Configurações e conexões
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # DTOs (Pydantic models)
│   ├── services/       # Lógica de negócio
│   └── api/           # Endpoints da API
├── env.example        # Exemplo de variáveis de ambiente
└── README.md
```

## Setup

1. **Criar ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

2. **Instalar dependências:**
```bash
pip install fastapi uvicorn
pip install sqlalchemy alembic psycopg2-binary
pip install pydantic pydantic-settings python-dotenv email-validator
```

3. **Configurar variáveis de ambiente:**
```bash
cp env.example .env
# Editar .env com suas configurações do PostgreSQL
```

4. **Executar a aplicação:**
```bash
uvicorn app.main:app --host localhost --port 8000 --reload
```

## Endpoints Disponíveis

### Fase 1 - Signup
- `POST /api/v1/auth/signup` - Criar novo usuário

### Documentação
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## Exemplo de Uso

### Criar usuário
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "usuario@exemplo.com",
       "firebase_uid": "firebase_user_id_123"
     }'
```

## Próximas Fases

- **Fase 2**: Autenticação com Firebase e JWT
- **Fase 3**: Middleware de autenticação
- **Fase 4**: Funcionalidades avançadas 