from fastapi import APIRouter

from main.models import Login

from main.data import usuarios

router = APIRouter(tags = ["Autenticado"])

@router.post("/login")
def login(dados: Login):

    for usuario in usuarios:
        if usuario.email == dados.email and usuario.senha == dados.senha:
            return {
                "mensagem": "Login realizado com sucesso",
                "usuario": usuario
            }

    return {
        "mensagem": "E-mail ou senha incorretos"
    }