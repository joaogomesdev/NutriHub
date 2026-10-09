from pydantic import BaseModel

        # Tratamento de dados do objetivo do usuário com o sistema.

class ObjetivoNutricionalSchema(BaseModel):
    objetivo: str


class ObjetivoNutricionalResponse(BaseModel):
    id: int
    usuario_id: int
    objetivo: str

    model_config = {
        "from_attributes": True
    }