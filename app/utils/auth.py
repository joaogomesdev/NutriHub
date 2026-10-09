import os
from datetime import datetime, timedelta, timezone

        # Modulo de geração de tokens para autenticação.

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não configurada no arquivo .env")
ALGORITHM = "HS256"
TEMPO_EXPIRACAO = 30


def criar_token(usuario_id: int):
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=TEMPO_EXPIRACAO
    )

    dados_token = {
        "sub": str(usuario_id),
        "exp": expiracao
    }

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def validar_token(token: str):
    dados = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return dados