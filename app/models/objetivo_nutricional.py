from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

        # Tebela para registrar o objetivo do usuário.

class ObjetivoNutricional(Base):
    __tablename__ = "objetivos_nutricionais"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        unique=True,
        nullable=False
    )

    objetivo = Column(String, nullable=False)