from fastapi import FastAPI, Depends, HTTPException, Security # Importando o FastAPI da biblioteca fastapi
from sqlalchemy.orm import Session
from app.models.usuario import Usuario # Importando nossa classe "Usuario"
from app.schemas.usuario_schema import UsuarioSchema, UsuarioResponse
from app.database.database import Base, engine, get_db
from app.utils.senha import criar_hash
from app.schemas.usuario_schema import UsuarioLogin
from app.utils.senha import verificar_senha
from app.utils.auth import criar_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from app.utils.auth import validar_token
from app.models.objetivo_nutricional import ObjetivoNutricional
from app.schemas.objetivo_schema import (ObjetivoNutricionalSchema, ObjetivoNutricionalResponse)
from app.models.questionario import Questionario
from app.schemas.questionario_schema import (QuestionarioSchema, QuestionarioResponse)

app = FastAPI() # Criando um objeto da classe FastAPI

security = HTTPBearer(auto_error=False)


def obter_usuario_autenticado(  # Função para autenticar o usuário usando o id e o token.
    credenciais: HTTPAuthorizationCredentials | None = Security(security),
    db: Session = Depends(get_db)
):
    if credenciais is None:
        raise HTTPException(
            status_code=401,
            detail="Token não fornecido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        dados_token = validar_token(credenciais.credentials)
        usuario_id = int(dados_token["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return usuario

Base.metadata.create_all(bind=engine)

@app.get("/") # Quando alguém acessar o endereço "/" usando GET, execute a função que vem logo abaixo.
def inicio():
    return {"mensagem": "Olá! nosso projeto Nutri começou!"}

@app.get("/usuario/{usuario_id}", response_model=UsuarioResponse) # Funcao pra pegar o usuario pelo id
def obter_usuario_por_id(
    usuario_id: int,
    usuario_atual: Usuario = Depends(obter_usuario_autenticado)
):
    if  usuario_id != usuario_atual.id:
        raise HTTPException(
                status_code=403,
                detail="Você não tem permisão para acessar esse usuário"
        )

    return usuario_atual

@app.put("/usuario/{usuario_id}", response_model=UsuarioResponse) # Funcao para atualizar os dados do usuario.
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioSchema,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_autenticado)
):
    if usuario_id != usuario_atual.id:
        raise HTTPException(
                status_code=403,
                detail="Você não tem permisão para alterar esse usuário"
        )
    
    email_existente = db.query(Usuario).filter(
        Usuario.email == dados.email,
        Usuario.id != usuario_atual.id
    ).first()

    if email_existente:
        raise HTTPException(
            status_code=409,
            detail="Email já cadastrado por outro usuário"
        )

    usuario_atual.nome = dados.nome
    usuario_atual.email = dados.email
    usuario_atual.senha = criar_hash(dados.senha)

    db.commit()
    db.refresh(usuario_atual)

    return usuario_atual

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
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario


@app.delete("/usuario/{usuario_id}")
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_autenticado)
):
    if usuario_id != usuario_atual.id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para excluir este usuário"
        )

    try:
        # Exclui o questionário associado à conta, se existir.
        questionario = db.query(Questionario).filter(
            Questionario.usuario_id == usuario_atual.id
        ).first()

        if questionario:
            db.delete(questionario)

        # Exclui o objetivo nutricional associado, se existir.
        objetivo = db.query(ObjetivoNutricional).filter(
            ObjetivoNutricional.usuario_id == usuario_atual.id
        ).first()

        if objetivo:
            db.delete(objetivo)

        # Por último, exclui a conta.
        db.delete(usuario_atual)
        db.commit()

        return {"mensagem": "Usuário excluído com sucesso"}

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Não foi possível excluir a conta"
        )

@app.post("/login")  # Funcao de login com uma conta já criada.
def login(
    dados: UsuarioLogin,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario or not verificar_senha(
        dados.senha, usuario.senha
    ):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )

    token = criar_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/me", response_model=UsuarioResponse)
def meu_usuario(
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    return usuario


    # Rotas para o objetivo Nutricional


@app.post(  # Função para cadastrar o Objetivo Nutricional
    "/objetivo-nutricional",
    response_model=ObjetivoNutricionalResponse
)
def criar_objetivo(
    dados: ObjetivoNutricionalSchema,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    objetivo_existente = db.query(ObjetivoNutricional).filter(
        ObjetivoNutricional.usuario_id == usuario.id
    ).first()

    if objetivo_existente:
        raise HTTPException(
            status_code=409,
            detail="Você já possui um objetivo cadastrado"
        )

    novo_objetivo = ObjetivoNutricional(
        usuario_id=usuario.id,
        objetivo=dados.objetivo
    )

    db.add(novo_objetivo)
    db.commit()
    db.refresh(novo_objetivo)

    return novo_objetivo


@app.get(  # Função para pegar o Objetivo Nutricional
    "/objetivo-nutricional",
    response_model=ObjetivoNutricionalResponse
)
def obter_objetivo(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    objetivo = db.query(ObjetivoNutricional).filter(
        ObjetivoNutricional.usuario_id == usuario.id
    ).first()

    if not objetivo:
        raise HTTPException(
            status_code=404,
            detail="Objetivo nutricional não encontrado"
        )

    return objetivo


@app.put(  # Funcao para atualizar o Objetivo Nutricional
    "/objetivo-nutricional",
    response_model=ObjetivoNutricionalResponse
)
def atualizar_objetivo(
    dados: ObjetivoNutricionalSchema,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    objetivo = db.query(ObjetivoNutricional).filter(
        ObjetivoNutricional.usuario_id == usuario.id
    ).first()

    if not objetivo:
        raise HTTPException(
            status_code=404,
            detail="Objetivo nutricional não encontrado"
        )

    objetivo.objetivo = dados.objetivo

    db.commit()
    db.refresh(objetivo)

    return objetivo


    # Rotas para o Qustionario.


@app.post(  # Função para autenticar o usuário que está fazendo o Questionario.
    "/questionario",
    response_model=QuestionarioResponse,
    status_code=201
)
def criar_questionario(
    dados: QuestionarioSchema,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    if usuario.questionario_concluido:
        raise HTTPException(
            status_code=409,
            detail="O questionário já foi concluído."
        )

    questionario_existente = db.query(Questionario).filter(
        Questionario.usuario_id == usuario.id
    ).first()

    if questionario_existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe um questionário para este usuário."
        )

    novo_questionario = Questionario(
        usuario_id=usuario.id,
        idade=dados.idade,
        peso=dados.peso,
        altura=dados.altura,
        nivel_atividade=dados.nivel_atividade.value,
        restricao_alimentar=dados.restricao_alimentar.value,
        refeicoes_por_dia=dados.refeicoes_por_dia
    )

    db.add(novo_questionario)
    usuario.questionario_concluido = True

    db.commit()
    db.refresh(novo_questionario)

    return novo_questionario