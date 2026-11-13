# ==========================================
# 1. BIBLIOTECAS EXTERNAS
# ==========================================

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from jwt import InvalidTokenError
from sqlalchemy.orm import Session


# ==========================================
# 2. BANCO DE DADOS
# ==========================================

from BD.database import Base, engine, get_db


# ==========================================
# 3. MODELS
# ==========================================

from BACK.app.models.usuario import Usuario
from BACK.app.models.objetivo_nutricional import ObjetivoNutricional
from BACK.app.models.questionario import Questionario
from BACK.app.models.resposta_questionario import RespostaQuestionario


# ==========================================
# 4. SCHEMAS
# ==========================================

from BACK.app.schemas.usuario_schema import (
    UsuarioLogin,
    UsuarioSchema,
    UsuarioResponse
)

from BACK.app.schemas.objetivo_schema import (
    ObjetivoNutricionalSchema,
    ObjetivoNutricionalResponse
)

from BACK.app.schemas.questionario_schema import (
    QuestionarioResponse,
    RespostaQuestionarioSchema
)


# ==========================================
# 5. UTILITÁRIOS
# ==========================================

from BACK.app.utils.senha import criar_hash, verificar_senha
from BACK.app.utils.auth import criar_token, validar_token

# ==========================================

app = FastAPI() # Criando um objeto da classe FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

    
Base.metadata.create_all(bind=engine) # Cria tabelas que ainda não existem


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


@app.post("/objetivo-nutricional", response_model=ObjetivoNutricionalResponse) # Função para cadastrar o Objetivo Nutricional
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


@app.put("/objetivo-nutricional", response_model=ObjetivoNutricionalResponse) # Funcao para atualizar o Objetivo Nutricional
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

@app.post("/questionario", response_model=QuestionarioResponse)
def criar_questionario(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    questionario_existente = db.query(Questionario).filter(
        Questionario.usuario_id == usuario.id
    ).first()

    if questionario_existente:
        return questionario_existente

    novo_questionario = Questionario(
        usuario_id=usuario.id
    )

    db.add(novo_questionario)
    db.commit()
    db.refresh(novo_questionario)

    return novo_questionario


@app.get("/questionario", response_model=QuestionarioResponse)
def obter_questionario(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    questionario = db.query(Questionario).filter(
        Questionario.usuario_id == usuario.id
    ).first()

    if not questionario:
        raise HTTPException(
            status_code=404,
            detail="Questionário não encontrado"
        )

    return questionario


@app.put("/questionario/resposta")
def salvar_resposta(
    dados: RespostaQuestionarioSchema,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    # 1. Busca o questionário do usuário.
    questionario = db.query(Questionario).filter(
        Questionario.usuario_id == usuario.id
    ).first()

    if not questionario:
        raise HTTPException(
            status_code=404,
            detail="Questionário não encontrado. Inicie primeiro."
        )

    if questionario.status == "concluido":
        raise HTTPException(
            status_code=409,
            detail="Este questionário já foi concluído."
        )

    # 2. Descobre o número da pergunta.
    numero_pergunta = int(dados.pergunta_codigo[1:])

    # Não permite responder perguntas futuras.
    if numero_pergunta > questionario.pergunta_atual:
        raise HTTPException(
            status_code=409,
            detail="Responda as perguntas na ordem correta."
        )

    # 3. Procura uma resposta já cadastrada.
    resposta_existente = db.query(RespostaQuestionario).filter(
        RespostaQuestionario.questionario_id == questionario.id,
        RespostaQuestionario.pergunta_codigo == dados.pergunta_codigo
    ).first()

    # 4. Atualiza ou cria a resposta.
    if resposta_existente:
        resposta_existente.resposta = dados.resposta
    else:
        nova_resposta = RespostaQuestionario(
            questionario_id=questionario.id,
            pergunta_codigo=dados.pergunta_codigo,
            resposta=dados.resposta
        )

        db.add(nova_resposta)

    # 5. Atualiza o progresso somente se for a pergunta atual.
    if numero_pergunta == questionario.pergunta_atual:

        if numero_pergunta < 27:
            questionario.pergunta_atual += 1

        # Atualiza o bloco conforme a próxima pergunta.
        if questionario.pergunta_atual <= 4:
            questionario.bloco_atual = 1
        elif questionario.pergunta_atual <= 8:
            questionario.bloco_atual = 2
        elif questionario.pergunta_atual <= 13:
            questionario.bloco_atual = 3
        elif questionario.pergunta_atual <= 18:
            questionario.bloco_atual = 4
        elif questionario.pergunta_atual <= 23:
            questionario.bloco_atual = 5
        else:
            questionario.bloco_atual = 6

    db.commit()

    return {
        "mensagem": "Resposta salva com sucesso!",
        "pergunta_codigo": dados.pergunta_codigo,
        "proxima_pergunta": questionario.pergunta_atual,
        "bloco_atual": questionario.bloco_atual
    }


@app.post("/questionario/concluir") # Chegar se o questionário foi concluído.
def concluir_questionario(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_autenticado)
):
    # 1. Busca o questionário do usuário.
    questionario = db.query(Questionario).filter(
        Questionario.usuario_id == usuario.id
    ).first()

    if not questionario:
        raise HTTPException(
            status_code=404,
            detail="Questionário não encontrado."
        )

    # 2. Verifica se já foi concluído.
    if questionario.status == "concluido":
        raise HTTPException(
            status_code=409,
            detail="Este questionário já foi concluído."
        )

    # 3. Conta quantas perguntas foram respondidas.
    total_respostas = db.query(RespostaQuestionario).filter(
        RespostaQuestionario.questionario_id == questionario.id
    ).count()

    if total_respostas < 27:
        raise HTTPException(
            status_code=409,
            detail="Responda todas as 27 perguntas antes de concluir."
        )

    # 4. Atualiza o status do questionário e do usuário.
    questionario.status = "concluido"
    usuario.questionario_concluido = True

    db.commit()

    return {
        "mensagem": "Questionário concluído com sucesso!"
    }