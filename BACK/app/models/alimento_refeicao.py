from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from BD.database import Base

class AlimentoRefeicao(Base):
    __tablename__ = "alimentos_refeicao"

    id = Column(Integer, primary_key=True, index=True)

    refeicao_id = Column(
        Integer,
        ForeignKey("refeicoes.id", ondelete="CASCADE"),
        nullable=False
    )

    nome = Column(String, nullable=False)
    porcao = Column(String, nullable=True)
    calorias = Column(Float, default=0)

    refeicao = relationship(
        "Refeicao",
        back_populates="alimentos"
    )