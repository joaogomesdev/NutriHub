from pydantic import BaseModel # Validação dos dados recebidos do front-end

# Nosso tratamento de entrada e saída de dados do usuário.

class UsuarioSchema(BaseModel):  # Representa os dados necessários para cadastrar ou atualizar um usuário.
    nome: str
    email: str
    senha: str

class AlterarSenhaSchema(BaseModel):
    senha_atual: str
    nova_senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    questionario_concluido: bool

    model_config = {
        "from_attributes": True
    }

class UsuarioLogin(BaseModel):  # Para não misturar os dados de cadastro com os dados de entrada. Representa apenas os dados necessários para entrar na conta.
    email: str
    senha: str