from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Criar engine do banco de dados
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG  # Log SQL queries em desenvolvimento
)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


def get_db():
    """Dependência para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine) 