from fastapi import FastAPI # Importando o FastAPI da biblioteca fastapi
from app.models.usuario import Usuario # Importando nossa classe "Usuario"
from app.schemas.usuario_schema import UsuarioSchema
from app.database.database import Base, engine

app = FastAPI() # Criando um objeto da classe FastAPI

Base.metadata.create_all(bind=engine)

@app.get("/") # Quando alguém acessar o endereço "/" usando GET, execute a função que vem logo abaixo.
def inicio():
    return {"mensagem": "Olá! nosso projeto Nutri começou!"}

@app.get("/usuario")
def obter_usuario():
    usuario = Usuario(
        "Asafe",
        "asafe@gmail.com",
        "123456"
    )

    return {
        "nome": usuario.nome,
        "email": usuario.email
    }

@app.post("/usuario")
def criar_usuario(usuario: UsuarioSchema):
    return usuario