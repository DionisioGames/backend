from fastapi import APIRouter

from main.models import Usuario, UsuarioResponse

from main.data import usuarios

router = APIRouter(tags = ["Usuários"])

@router.post("/usuarios")
def cadastrar_usuario(usuario: Usuario):

    if usuario.tipo != "professor" and usuario.tipo != "secretaria":
        return {
            "mensagem": "Tipo de usuário inválido"
        }

    for usuario_existente in usuarios:
        if usuario_existente.email == usuario.email:
            return {
                "mensagem": "Já existe um usuário com esse e-mail"
            }

    usuarios.append(usuario)

    return {
        "mensagem": "Usuário cadastrado com sucesso",
        "usuario": usuario
    }

@router.get("/usuarios")
def listar_usuarios():
    return usuarios

@router.get("/usuarios/{id}", response_model=UsuarioResponse)
def buscar_usuario(id: int):

    for usuario in usuarios:
        if usuario.id == id:
            return usuario

    return {
        "mensagem": "Usuário não encontrado"
    }