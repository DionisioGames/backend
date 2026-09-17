from pwdlib import PasswordHash

import jwt 
from datetime import datetime, timedelta, timezone


from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


password_hash = PasswordHash.recommended()


def gerar_hash_senha(senha: str):
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str):
    return password_hash.verify(senha, senha_hash)

#JWT
SECRET_KEY = "minha-chave-secreta"
ALGORITHM = "HS256"

security = HTTPBearer()


def criar_token(id_usuario: int, tipo: str):
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)

    dados_token = {
        "sub": str(id_usuario),
        "tipo": tipo,
        "exp": expiracao
    }

    token = jwt.encode(
        dados_token, #dados do token
        SECRET_KEY, #minha chave secreta
        algorithm=ALGORITHM
    )

    return token

def verificar_token(token: str):
    try: 
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return dados
    
    except jwt.ExpiredSignatureError:
        # Token está invalido por ter expirado
        return None

    except jwt.InvalidTokenError:
        # Token está errado ou foi mexido
        return None

def usuario_autenticado(
        credenciais: HTTPAuthorizationCredentials = Depends(security)
): 
    token = credenciais.credentials

    dados = verificar_token(token)

    if dados is None:
        raise HTTPException(
            status_code = 401, #401 Unauthorized Usuário não está autenticado ou login está incorreto
            detail = "Token inválido ou expirado. Faça o Login novamente."
        )
    return dados

