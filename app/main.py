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

@app.get("/usuario", response_model=list[UsuarioResponse])
def obter_usuario(
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).all()

    return usuario

@app.get("/usuario/{usuario_id}", response_model=UsuarioResponse) # Funcao pra pegar o usuario pelo id
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first() # Esse "first" pega o primeiro resultado

    if not usuario:
        raise HTTPException(
                status_code=409,
                detail="Usuario não encontrado"
        )

    return usuario

@app.put("/usuario/{usuario_id}", response_model=UsuarioResponse) # Funcao para atualizar os dados do usuario.
def atualizar_usuario(
    usuario_id: int,
    usuario: UsuarioSchema,
    db: Session = Depends(get_db)
):

    usuario_existente = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario_existente:
        raise HTTPException(
            status_code=404,
            detail="Usuario não encontrado"
        )

    email_existente = db.query(Usuario).filter(
        Usuario.email == usuario.email,
        Usuario.id != usuario_id
    ).first()

    if email_existente:
        raise HTTPException(
            status_code=409,
            detail="Email já cadastrado por outro usuário"
        )

    usuario_existente.nome = usuario.nome
    usuario_existente.email = usuario.email
    usuario_existente.senha = criar_hash(usuario.senha)

    db.commit()
    db.refresh(usuario_existente)

    return usuario_existente

@app.post("/usuario", response_model=UsuarioResponse) # Funcao para criar nosso usuario
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