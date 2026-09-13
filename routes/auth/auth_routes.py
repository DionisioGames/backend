from fastapi import APIRouter, HTTPException

from main.models import Login

from main.data import usuarios

router = APIRouter(tags = ["Autenticado"])

@router.post("/login")
def login(dados: Login): 

    for usuario in usuarios:
        if usuario.email == dados.email and usuario.senha == dados.senha:
            return {
                "mensagem": "Login realizado com sucesso",
                "usuario": {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "telefone": usuario.telefone,
                    "tipo": usuario.tipo    
                }
            }
    raise HTTPException(
        status_code = 401, #401 Unauthorized Usuário não está autenticado ou login está incorreto
        detail = "Erro ao realizar login. Verifique os dados e tente novamente."
    ) 