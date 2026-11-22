from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MetaSchema(BaseModel):
    titulo: str
    categoria: str
    alvo: float
    unidade: str
    frequencia: str = "diaria"


class MetaResponse(BaseModel):
    id: int
    titulo: str
    categoria: str
    alvo: float
    atual: float
    unidade: str
    frequencia: str
    concluida: bool
    criada_em: datetime

    model_config = ConfigDict(from_attributes=True)


class MetaConclusao(BaseModel):
    concluida: bool