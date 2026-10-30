from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, event

# Preparando o ambiente e a comunicação do BD com o Back-End.

DATABASE_URL = "sqlite:///./nutrihub.db" # Nossa url do banco de dados.

engine = create_engine(  # Mecanismo de comunicação.
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    ) 

@event.listens_for(engine, "connect") # Ativar a fiscalicacao de chaves segundarias.
def ativar_chaves_estrangeiras(conexao, registro):
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(bind=engine) # Fábrica de sessões.

def get_db(): # nossa função de SESSÃO, pra comunicação temp com o BD.
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close

Base = declarative_base() # É a base que o SQLAlchemy usa para registrar nossos modelos.