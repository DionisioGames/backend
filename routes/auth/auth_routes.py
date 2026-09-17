from fastapi import APIRouter, HTTPException, Depends

from main.models import Login

from main.data import usuarios

from main.security import verificar_senha, criar_token, usuario_autenticado

router = APIRouter(tags = ["Autenticado"])

@router.post("/login")
def login(dados: Login): 

    for usuario in usuarios:
        if usuario.email == dados.email and verificar_senha(
            dados.senha,  # senha digitada pelo usuário
            usuario.senha # senha armazenada no banco de dados(HASH)  
            ):

                token = criar_token(
                     usuario.id, # id da poha do usuario
                     usuario.tipo # tipo do usuario(professor ou secretaria)
                )

                return {
                "mensagem": "Login realizado com sucesso",
                "token": token,
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

@router.get("/teste-protegido")
def teste_protegido(
     dados_token: dict = Depends(usuario_autenticado) # O fastapi vai chamar a função usuario_autenticado e vai passar o resultado dela para a variavel dados_token
):
     return {
          "mensagem": "Você está autenticado e pode acessar essa rota",
          "dados_token": dados_token 
     }

@router.get("/teste-secretaria")
def teste_secretaria(
    dados_token: dict = Depends(usuario_autenticado) # Chama a função usuario_autenticado.
):
    if dados_token["tipo"] != "secretaria": #Exemplo de como verificar o tipo do usuário. Se o tipo do usuário não for "secretaria", ele não terá acesso a essa rota.
        raise HTTPException(
            status_code=403,
            detail="Apenas a secretaria pode acessar esta rota."
        )

    return {
        "mensagem": "Acesso autorizado para a secretaria!"
    }