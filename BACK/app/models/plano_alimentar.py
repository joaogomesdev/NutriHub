from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from BD.database import Base

    # Molde que representa a nossa estrutura dentro do BD.


class PlanoAlimentar(Base):
    __tablename__ = "planos_alimentares"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    dieta_titulo = Column(String, nullable=False)
    dieta_descricao = Column(String, nullable=False)

    rotina_titulo = Column(String, nullable=False)
    rotina_descricao = Column(String, nullable=False)

    usuario = relationship(
        "Usuario",
        back_populates="plano_alimentar"
    )