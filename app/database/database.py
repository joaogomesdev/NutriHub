from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Preparando o ambiente e a comunicação do BD com o Back-End.

DATABASE_URL = "sqlite:///./nutrihub.db" # Nossa url do banco de dados.

engine = create_engine(  # Mecanismo de comunicação.
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    ) 

SessionLocal = sessionmaker(bind=engine) # Fábrica de sessões.

def get_db(): # nossa função de SESSÃO, pra comunicação temp com o BD.
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close

Base = declarative_base() # É a base que o SQLAlchemy usa para registrar nossos modelos.