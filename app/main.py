from fastapi import FastAPI, Depends, HTTPException # Importando o FastAPI da biblioteca fastapi
from sqlalchemy.orm import Session
from app.models.usuario import Usuario # Importando nossa classe "Usuario"
from app.schemas.usuario_schema import UsuarioSchema, UsuarioResponse
from app.database.database import Base, engine, get_db
from app.utils.senha import criar_hash

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

@app.post("/usuario", response_model=UsuarioResponse) # Criando nosso usuario
def criar_usuario(
    usuario: UsuarioSchema,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=409,
            detail="Email já cadastrado"
        )
    
    senha_hash = criar_hash(usuario.senha)
    
    novo_usuario = Usuario( # Objeto da nossa classe Usuario
        usuario.nome,
        usuario.email,
        senha_hash
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario