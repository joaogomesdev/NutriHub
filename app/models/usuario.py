
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)

    questionario_concluido = Column(
        Boolean,
        nullable=False,
        default=False
    )

    objetivo_nutricional = relationship(
        "ObjetivoNutricional",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    questionario = relationship(
        "Questionario",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def alterar_email(self, novo_email):
        self.email = novo_email

    def validar_senha(self, senha):
        return self.senha == senha
