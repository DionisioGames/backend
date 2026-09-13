from fastapi import APIRouter, HTTPException

from main.models import Sala

from main.data import salas

router = APIRouter(tags=["Salas"])

@router.post("/salas", status_code = 201)
def cadastrar_sala(sala: Sala):
    salas.append(sala)
    return {
        "mensagem": "Sala cadastrada com sucesso",
        "sala": sala
    }
    
@router.get("/salas")
def buscar_salas():
    return salas

@router.get("/salas/{id}")
def buscar_sala(id: int):
    for sala in salas:
        if sala.id == id:
            return sala
    raise HTTPException(
        status_code = 404, #404 Not Found Sala não encontrada
        detail = "Sala não foi encontrada. Verifique os dados e tente novamente."
    )