from fastapi import APIRouter, HTTPException

from main.models import Reserva

from main.data import salas, reservas, historico_reservas, usuarios

router = APIRouter(tags=["Reservas"])

@router.post("/reservas", status_code = 201)
def criar_reserva(reserva: Reserva):

    sala_encontrada = False

    for sala in salas:
        if sala.id == reserva.id_sala:
            sala_encontrada = True
            break

    if sala_encontrada == False:
        raise HTTPException(
            status_code = 404, #404 Not Found Sala não encontrada
            detail = "Sala não encontrada. Verifique os dados e tente novamente."
        )

    professor_encontrado = False

    for usuario in usuarios:
        if usuario.id == reserva.id_professor and usuario.tipo == "professor":
            professor_encontrado = True
            break

    if professor_encontrado == False:
        raise HTTPException(
            status_code = 404, #404 Not Found Professor não encontrado
            detail = "Professor não encontrado. Verifique os dados e tente novamente."
        )

    if reserva.hora_inicio >= reserva.hora_fim:
        raise HTTPException(
            status_code = 400, #400 Bad Request Requisição está errada, hora de início é maior ou igual a hora de fim
            detail = "Erro ao criar a reserva. Verifique os dados e tente novamente."
        )

    for reserva_existente in reservas:
        if (
            reserva_existente.id_sala == reserva.id_sala
            and reserva_existente.data == reserva.data
            and reserva.hora_inicio < reserva_existente.hora_fim
            and reserva.hora_fim > reserva_existente.hora_inicio
        ):
            raise HTTPException(
                status_code = 409, #409 Conflict Conflito de requisição, já existe uma reserva nesse horário
                detail = "Erro ao criar a reserva. Verifique os dados e tente novamente."
            )

    reservas.append(reserva)
    return{
        "mensagem": "Reserva criada com sucesso",
        "reserva": reserva
    }

@router.get("/reservas")
def listar_reservas():
    return reservas

@router.get("/reservas/{id}")
def buscar_reserva(id: int):

    for reserva in reservas:
        if reserva.id == id:
            return reserva

    raise HTTPException(
        status_code = 404, #404 Not Found Reserva não encontrada
        detail = "Reserva não encontrada. Verifique os dados e tente novamente."
    )
@router.get("/historico/reservas")
def listar_historico_reservas():
    return historico_reservas

@router.patch("/reservas/{id}/aprovar")
def aprovar_reserva(id: int):

    for reserva in reservas:
        if reserva.id == id:

            if reserva.status != "pendente":
                raise HTTPException(
                    status_code = 409, #409 Conflict Conflito de requisição, reserva já foi analisada
                    detail = "Essa reserva já foi analisada. Verifique os dados e tente novamente."
                )

            reserva.status = "aprovada"

            return {
                "mensagem": "Reserva aprovada com sucesso",
                "reserva": reserva
            }

    raise HTTPException(
        status_code = 404, #404 Not Found Reserva não encontrada
    detail = "Reserva não encontrada. Verifique os dados e tente novamente."
    )

@router.patch("/reservas/{id}/rejeitar")
def rejeitar_reserva(id: int):

    for reserva in reservas:
        if reserva.id == id:

            if reserva.status != "pendente":
                raise HTTPException(
                    status_code = 409, #409 Conflict Conflito de requisição, reserva já foi analisada
                    detail = "Essa reserva já foi analisada. Verifique os dados e tente novamente."
                )

            reserva.status = "rejeitada"

            return {
                "mensagem": "Reserva rejeitada",
                "reserva": reserva
            }

    raise HTTPException(
        status_code = 404, #404 Not Found Reserva não encontrada
        detail = "Reserva não encontrada. Verifique os dados e tente novamente."
    )

@router.delete("/reservas/{id}")
def cancelar_reserva(id: int):

    for reserva in reservas:
        if reserva.id == id:

            reserva.status = "cancelada"

            historico_reservas.append(reserva)
            reservas.remove(reserva)

            return {
                "mensagem": "Reserva cancelada com sucesso",
                "reserva": reserva
            }

    raise HTTPException(
        status_code = 404, #404 Not Found Reserva não encontrada
        detail = "Reserva não encontrada. Verifique os dados e tente novamente."
    )