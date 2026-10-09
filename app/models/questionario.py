from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database.database import Base


class Questionario(Base):
    __tablename__ = "questionarios"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        unique=True,
        nullable=False
    )

    idade = Column(Integer, nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    nivel_atividade = Column(String, nullable=False)
    restricao_alimentar = Column(String, nullable=False)
    refeicoes_por_dia = Column(Integer, nullable=False)