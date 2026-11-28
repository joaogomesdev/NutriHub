from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

# Preparando a comunicação do banco de dados com o Back-End.

import os
if os.getenv("VERCEL"):
    DATABASE_URL = "sqlite:////tmp/nutrihub.db"
else:
    DATABASE_URL = "sqlite:///./nutrihub.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Ativando a fiscalização das chaves estrangeiras.
@event.listens_for(engine, "connect")
def ativar_chaves_estrangeiras(conexao, registro):
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Fábrica de sessões.
SessionLocal = sessionmaker(bind=engine)


# Gerenciando a sessão do banco de dados.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Base utilizada pelo SQLAlchemy para registrar os modelos.
Base = declarative_base()
