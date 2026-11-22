from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from BD.database import Base
from datetime import datetime


class Meta(Base):
    __tablename__ = "metas"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    titulo = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    alvo = Column(Float, nullable=False)
    atual = Column(Float, default=0)
    unidade = Column(String, nullable=False)
    frequencia = Column(String, default="diaria")
    concluida = Column(Boolean, default=False)
    criada_em = Column(DateTime, default=datetime.utcnow)

    usuario = relationship(
        "Usuario",
        back_populates="metas"
    )