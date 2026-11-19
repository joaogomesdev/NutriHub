from pydantic import BaseModel
from typing import Optional

class AlimentoRefeicaoSchema(BaseModel):
    nome: str
    porcao: Optional[str] = None
    calorias: float = 0

class AlimentoRefeicaoResponse(AlimentoRefeicaoSchema):
    id: int

    class Config:
        from_attributes = True