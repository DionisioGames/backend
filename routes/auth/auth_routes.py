from fastapi import APIRouter, HTTPException

from main.models import Login

from main.data import usuarios

from main.security import verificar_senha

router = APIRouter(tags = ["Autenticado"])

@router.post("/login")
def login(dados: Login): 

    for usuario in usuarios:
        if usuario.email == dados.email and verificar_senha(
            dados.senha,  # senha digitada pelo usuário
            usuario.senha # senha armazenada no banco de dados(HASH)  
            ):
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