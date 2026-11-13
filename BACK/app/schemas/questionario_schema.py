from pydantic import BaseModel, Field


# Dados recebidos ao responder uma pergunta.
class RespostaQuestionarioSchema(BaseModel):

    pergunta_codigo: str = Field(
        pattern=r"^q([1-9]|1[0-9]|2[0-7])$"
    )

    resposta: str = Field(min_length=1)


# Dados devolvidos pela API.
class RespostaQuestionarioResponse(BaseModel):

    id: int
    questionario_id: int
    pergunta_codigo: str
    resposta: str

    model_config = {"from_attributes": True}
    

# Dados devolvidos ao consultar o questionário.
class QuestionarioResponse(BaseModel):

    id: int
    usuario_id: int
    status: str
    bloco_atual: int
    pergunta_atual: int

    respostas: list[RespostaQuestionarioResponse] = Field(
        default_factory=list
    )

    model_config = {"from_attributes": True}