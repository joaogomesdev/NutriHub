from enum import Enum
from pydantic import BaseModel


class ObjetivoEnum(str, Enum):
    EMAGRECER = "emagrecer"
    GANHAR_MASSA_MUSCULAR = "ganhar_massa_muscular"
    MANTER_PESO = "manter_peso"
    MELHORAR_HABITOS = "melhorar_habitos"


class ObjetivoNutricionalSchema(BaseModel):
    objetivo: ObjetivoEnum


class ObjetivoNutricionalResponse(BaseModel):
    id: int
    usuario_id: int
    objetivo: ObjetivoEnum

    model_config = {
        "from_attributes": True
    }