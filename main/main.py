# para rodar o codigo, executar no terminal: uvicorn main.main:app --reload
# para desabilitar o servidor coloque no terminal e digite o comando  (ctrl + c)

from fastapi import FastAPI

from main.models import Sala, Reserva

app = FastAPI()

Salas = []

Reservas = []

@app.post("/salas")
def cadastrar_sala(sala: Sala):
    Salas.append(sala)

    return {
        "mensagem": f"Sala {sala.nome} cadastrada com sucesso"
    }

@app.get("/salas")
def buscar_salas():
    return Salas

@app.get("/salas/{id}")
def buscar_sala(id: int):
    for sala in Salas:
        if sala.id == id:
            return sala

    return {"mensagem": "Sala não foi encontrada"}

@app.post("/reservas")
def criar_reserva(reserva: Reserva):

    sala_encontrada = False

    for sala in Salas:
        if sala.id == reserva.id_sala:
            sala_encontrada = True
            break

    if sala_encontrada == False:
        return {"mensagem": "Sala não encontrada"}

    if reserva.hora_inicio >= reserva.hora_fim:
        return {
            "mensagem": "O horário inicial deve ser menor que o horário final"
        }

    for reserva_existente in Reservas:
        if (
            reserva_existente.id_sala == reserva.id_sala
            and reserva_existente.data == reserva.data
            and reserva.hora_inicio < reserva_existente.hora_fim
            and reserva.hora_fim > reserva_existente.hora_inicio
        ):
            return {"mensagem": "Já existe uma reserva nesse horário"}

    Reservas.append(reserva)

    return {
        "mensagem": "Solicitação de reserva criada com sucesso",
        "reserva": reserva
    }

@app.get("/reservas")
def listar_reservas():
    return Reservas

@app.get("/reservas/{id}")
def buscar_reserva(id: int):

    for reserva in Reservas:
        if reserva.id == id:
            return reserva

    return {"mensagem": "Reserva não encontrada"}