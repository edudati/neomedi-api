from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.routes import auth, company, professional, user_assistant, user
from app.db.database import create_tables
from app.models import (  # Importar modelos para criar tabelas
    auth_user,
    company as company_model,
    professional as professional_model,
    specialty as specialty_model,
    profession as profession_model,
    user_assistant as user_assistant_model
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle da aplicação"""
    # Startup
    print("Neomedi API starting...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Firebase Project: {settings.FIREBASE_PROJECT_ID}")
    
    # Criar tabelas do banco
    try:
        create_tables()
        print("Database tables verification completed!")
    except Exception as e:
        print(f"Error verifying/creating tables: {e}")
    
    yield
    
    # Shutdown
    print("Neomedi API shutting down...")


# Criar aplicação FastAPI
app = FastAPI(
    title="Neomedi API",
    description="API para gestão de clínicas de saúde integrativa",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
print(f"CORS configured with allowed origins: {settings.ALLOWED_ORIGINS}")
print(f"Allowed methods: GET, POST, PUT, DELETE, OPTIONS, PATCH")
print(f"Allowed headers: *")

# Configuração CORS mais permissiva para desenvolvimento
if settings.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite todas as origens em desenvolvimento
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos os métodos
        allow_headers=["*"],  # Permite todos os headers
        expose_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

print("CORS configured successfully!")

# Incluir rotas
app.include_router(auth.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(company.router, prefix="/api/v1/companies", tags=["companies"])
app.include_router(professional.router, prefix="/api/v1/professionals", tags=["professionals"])
app.include_router(user_assistant.router, prefix="/api/v1/user-assistants", tags=["user-assistants"])


@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Welcome to Neomedi API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check da aplicação"""
    return {
        "status": "healthy",
        "service": "neomedi-api",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


@app.get("/test-cors")
async def test_cors():
    """Endpoint de teste para CORS"""
    return {
        "message": "CORS is working!",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.post("/test-cors")
async def test_cors_post():
    """Endpoint POST de teste para CORS"""
    return {
        "message": "CORS POST is working!",
        "timestamp": "2024-01-01T00:00:00Z"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
