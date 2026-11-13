from sqlalchemy import Column, Integer, String, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from BD.database import Base


class RespostaQuestionario(Base):
    __tablename__ = "respostas_questionario"

    id = Column(Integer, primary_key=True, index=True)

    questionario_id = Column(
        Integer,
        ForeignKey("questionarios.id", ondelete="CASCADE"),
        nullable=False
    )

    pergunta_codigo = Column(String, nullable=False) # É a forma de identificar para qual coluna vai a resposta.

    resposta = Column(JSON, nullable=False) # É a forma de receber as respostas, usando JSON para armazenar diferentes formatos.

    __table_args__ = (
        UniqueConstraint(
            "questionario_id",
            "pergunta_codigo",
            name="uq_questionario_pergunta"
        ),
    )

    questionario = relationship(
        "Questionario",
        back_populates="respostas"
    )