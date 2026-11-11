from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

        # Modelo da tabela Questionario do nosso banco de dados.

class Questionario(Base):
    __tablename__ = "questionarios"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="em_andamento"
    )

    bloco_atual = Column(
        Integer,
        nullable=False,
        default=1
    )

    pergunta_atual = Column(
        Integer,
        nullable=False,
        default=1
    )

    usuario = relationship(
        "Usuario",
        back_populates="questionario"
    )

    respostas = relationship(
        "RespostaQuestionario",
        back_populates="questionario",
        cascade="all, delete-orphan",
        passive_deletes=True
    )