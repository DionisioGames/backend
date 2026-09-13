from fastapi import APIRouter, HTTPException

from main.models import Usuario, UsuarioResponse

from main.data import usuarios

from main.security import gerar_hash_senha

router = APIRouter(tags = ["Usuários"])

@router.post("/usuarios", status_code = 201)
def cadastrar_usuario(usuario: Usuario):

    if usuario.tipo != "professor" and usuario.tipo != "secretaria":
        raise HTTPException(
            status_code = 400, #400 Bad Request Tipo de usuário inválido
            detail = "Erro ao criar o usuário. Verifique os dados e tente novamente."
        )

    for usuario_existente in usuarios:
        if usuario_existente.email == usuario.email:
           raise HTTPException(
               status_code = 409, #409 Conflict Conflito de requisição, já existe um usuário com esse email
               detail = "Erro ao criar o usuário. Verifique os dados e tente novamente."
           )
    usuario.senha = gerar_hash_senha(usuario.senha)
        
    usuarios.append(usuario)

    return {
        "mensagem": "Usuário cadastrado com sucesso",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "tipo": usuario.tipo
        }
    } 

@router.get("/usuarios", response_model = list[UsuarioResponse])
def listar_usuarios():
    return usuarios

@router.get("/usuarios/{id}", response_model=UsuarioResponse)
def buscar_usuario(id: int):

    for usuario in usuarios:
        if usuario.id == id:
            return usuario

    raise HTTPException(
        status_code = 404, #404 Not Found Usuário não encontrado
        detail = "Usuário não encontrado. Verifique os dados e tente novamente."
    )