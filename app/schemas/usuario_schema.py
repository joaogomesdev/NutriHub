from pydantic import BaseModel # Validação dos dados recebidos do front-end

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    model_config = {
        "from_attributes": True
    }