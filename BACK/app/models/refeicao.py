from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from BD.database import Base

        # Molde da tabela Refeição no BD.

class Refeicao(Base):
    __tablename__ = "refeicoes"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    data = Column(String, nullable=False)
    horario = Column(String, nullable=False)

    tipo = Column(String, nullable=False)
    titulo = Column(String, nullable=False)

    descricao = Column(String, nullable=True)
    local = Column(String, nullable=True)

    calorias = Column(Float, default=0)
    quantidade_agua = Column(Float, default=0)

    usuario = relationship(
        "Usuario",
        back_populates="refeicoes"
    )

    alimentos = relationship(
        "AlimentoRefeicao",
        back_populates="refeicao",
        cascade="all, delete-orphan"
    )