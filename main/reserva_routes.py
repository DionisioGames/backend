from fastapi import APIRouter

from main.models import Reserva

from main.data import salas, reservas, historico_reservas, usuarios

router = APIRouter(tags=["Reservas"])

@router.post("/reservas")
def criar_reserva(reserva: Reserva):

    sala_encontrada = False

    for sala in salas:
        if sala.id == reserva.id_sala:
            sala_encontrada = True
            break

    if sala_encontrada == False:
        return {
            "mensagem": "Sala não encontrada"
        }

    professor_encontrado = False

    for usuario in usuarios:
        if usuario.id == reserva.id_professor and usuario.tipo == "professor":
            professor_encontrado = True
            break

    if professor_encontrado == False:
        return {
            "mensagem": "Professor não encontrado"
        }

    if reserva.hora_inicio >= reserva.hora_fim:
        return {
            "mensagem": "O horário inicial deve ser menor que o horário final"
        }

    for reserva_existente in reservas:
        if (
            reserva_existente.id_sala == reserva.id_sala
            and reserva_existente.data == reserva.data
            and reserva.hora_inicio < reserva_existente.hora_fim
            and reserva.hora_fim > reserva_existente.hora_inicio
        ):
            return {
                "mensagem": "Já existe uma reserva nesse horário"
            }

    reservas.append(reserva)

    return {
        "mensagem": "Solicitação de reserva criada com sucesso",
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

    return {"mensagem": "Reserva não encontrada"}

@router.get("/historico/reservas")
def listar_historico_reservas():
    return historico_reservas

@router.patch("/reservas/{id}/aprovar")
def aprovar_reserva(id: int):

    for reserva in reservas:
        if reserva.id == id:

            if reserva.status != "pendente":
                return {
                    "mensagem": "Essa reserva já foi analisada"
                }

            reserva.status = "aprovada"

            return {
                "mensagem": "Reserva aprovada com sucesso",
                "reserva": reserva
            }

    return {"mensagem": "Reserva não encontrada"}

@router.patch("/reservas/{id}/rejeitar")
def rejeitar_reserva(id: int):

    for reserva in reservas:
        if reserva.id == id:

            if reserva.status != "pendente":
                return {
                    "mensagem": "Essa reserva já foi analisada"
                }

            reserva.status = "rejeitada"

            return {
                "mensagem": "Reserva rejeitada",
                "reserva": reserva
            }

    return {"mensagem": "Reserva não encontrada"}

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

    return {"mensagem": "Reserva não encontrada"}

