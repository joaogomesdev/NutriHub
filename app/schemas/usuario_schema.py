from pydantic import BaseModel # Validação dos dados recebidos do front-end

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str