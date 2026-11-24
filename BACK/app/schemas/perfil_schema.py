from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PerfilSchema(BaseModel):
    data_nascimento: Optional[str] = None
    genero: Optional[str] = None
    nivel_atividade: Optional[str] = None
    peso_atual: Optional[float] = None
    meta_peso: Optional[float] = None
    altura: Optional[float] = None


class PerfilResponse(PerfilSchema):
    id: int
    usuario_id: int
    atualizado_em: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }