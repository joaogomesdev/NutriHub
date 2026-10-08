from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Usuario(Base): 
    __tablename__= "usuarios" # Atributo especial do SQLAlchemy para saber o nome da tablela do bd.
    
    # Nossa classe usuario

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String) # Não ficará assim, implantaremos autenticação com o hash.

    def __init__(self, nome, email, senha): # Nossos atributos
        self.nome = nome
        self.email = email
        self.senha = senha

                                       
    def alterar_email(self, novo_email): # Nossos metodos 
        self.email = novo_email

    def validar_senha(self, senha):
        return self.senha == senha