from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from BD.database import Base


class Perfil(Base):
    __tablename__ = "perfis"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    data_nascimento = Column(String, nullable=True)
    genero = Column(String, nullable=True)
    nivel_atividade = Column(String, nullable=True)
    peso_atual = Column(Float, nullable=True)
    meta_peso = Column(Float, nullable=True)
    altura = Column(Float, nullable=True)
    atualizado_em = Column(DateTime, nullable=True)

    usuario = relationship(
        "Usuario",
        back_populates="perfil"
    )