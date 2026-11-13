
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from BD.database import Base


class ObjetivoNutricional(Base):
    __tablename__ = "objetivos_nutricionais"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    objetivo = Column(String, nullable=False)

    usuario = relationship(
        "Usuario",
        back_populates="objetivo_nutricional"
    )
