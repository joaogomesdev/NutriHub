from enum import Enum
from pydantic import BaseModel, Field

        # Validação do dados para o questionario.

class NivelAtividadeEnum(str, Enum):
    SEDENTARIO = "sedentario"
    LEVE = "leve"
    MODERADO = "moderado"
    INTENSO = "intenso"


class RestricaoAlimentarEnum(str, Enum):
    NENHUMA = "nenhuma"
    VEGETARIANO = "vegetariano"
    VEGANO = "vegano"
    SEM_LACTOSE = "sem_lactose"


class QuestionarioSchema(BaseModel):
    idade: int = Field(gt=0, le=120)
    peso: float = Field(gt=0, le=500)
    altura: float = Field(gt=0, le=2.8)
    nivel_atividade: NivelAtividadeEnum
    restricao_alimentar: RestricaoAlimentarEnum
    refeicoes_por_dia: int = Field(ge=1, le=10)


class QuestionarioResponse(BaseModel):
    id: int
    usuario_id: int
    idade: int
    peso: float
    altura: float
    nivel_atividade: NivelAtividadeEnum
    restricao_alimentar: RestricaoAlimentarEnum
    refeicoes_por_dia: int

    model_config = {"from_attributes": True}