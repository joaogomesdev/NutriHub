from pydantic import BaseModel, Field
from typing import List, Optional

from BACK.app.schemas.alimento_refeicao_schema import AlimentoRefeicaoSchema
from BACK.app.schemas.alimento_refeicao_schema import (
    AlimentoRefeicaoSchema,
    AlimentoRefeicaoResponse
)

        # Como os dados serâo recebido para a tabela de Refeição.

class RefeicaoSchema(BaseModel):
    data: str
    horario: str
    tipo: str
    titulo: str
    descricao: Optional[str] = None
    local: Optional[str] = None
    calorias: float = 0
    quantidade_agua: float = 0

    alimentos: List[AlimentoRefeicaoSchema] = Field(default_factory=list)

class RefeicaoResponse(RefeicaoSchema):
    id: int
    alimentos: List[AlimentoRefeicaoResponse]

    class Config:
        from_attributes = True