from fastapi import APIRouter

from main.models import Sala

from main.data import salas

router = APIRouter(tags=["Salas"])

@router.post("/salas")
def cadastrar_sala(sala: Sala):
    salas.append(sala)

    return {
        "mensagem": f"Sala {sala.nome} cadastrada com sucesso"
    }

@router.get("/salas")
def buscar_salas():
    return salas

@router.get("/salas/{id}")
def buscar_sala(id: int):
    for sala in salas:
        if sala.id == id:
            return sala

    return {"mensagem": "Sala não foi encontrada"}

