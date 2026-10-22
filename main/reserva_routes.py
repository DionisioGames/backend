from fastapi import APIRouter, HTTPException, Depends

from main.models import Reserva, ReservaCreate

from main.data import salas, reservas, historico_reservas, usuarios

from main.security import usuario_autenticado

router = APIRouter(tags=["Reservas"])

@router.post("/reservas", status_code = 201)
def criar_reserva(
    dados_reserva: ReservaCreate,
    dados_token: dict = Depends(usuario_autenticado) # ele vai primereiro exucutar a função usuario_autenticado e vai passar o resultado dela para a variavel dados_token

    ):
    tipo_usuario = dados_token["tipo"]
    id_usuario_logado = int(dados_token["sub"])
   
    if tipo_usuario not in ["professor", "secretaria"]:
            raise HTTPException(
                status_code = 403, #403 Forbidden Usuário não tem permissão para acessar essa rota
                detail = "Você não tem permissão para criar uma reserva."
            )

    if tipo_usuario == "professor":
        id_professor = id_usuario_logado

    else:
        id_professor = dados_reserva.id_professor

    if tipo_usuario == "secretaria":
        status_inicial = "aprovada"
    else:
        status_inicial = "pendente"

    reserva = Reserva(
            id = dados_reserva.id,
            id_sala = dados_reserva.id_sala,
            id_professor = id_professor,
            data = dados_reserva.data,
            hora_inicio = dados_reserva.hora_inicio,
            hora_fim = dados_reserva.hora_fim,
            status = status_inicial
        )

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

    if reserva.id_professor is not None:
    
        professor_encontrado = False

        for usuario in usuarios:
            if (usuario.id == reserva.id_professor and usuario.tipo == "professor"):
                professor_encontrado = True
                break

        if not professor_encontrado:
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
def aprovar_reserva(
    id: int,
    dados_token: dict = Depends(usuario_autenticado) # ele vai primereiro exucutar a função usuario_autenticado e vai passar o resultado dela para a variavel dados_token

    ):
    if dados_token["tipo"] != "secretaria":
        raise HTTPException(
            status_code = 403, #403 Forbidden Usuário não tem permissão para acessar essa rota
            detail = "Apenas a secretaria pode aprovar reservas."
        )

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
def rejeitar_reserva(
    id: int,
    dados_token: dict = Depends(usuario_autenticado)

    ):
    if dados_token["tipo"] != "secretaria":
        raise HTTPException(
            status_code = 403, #403 Forbidden Usuário não tem permissão para acessar essa rota
            detail = "Apenas a secretaria pode rejeitar reservas."
        )

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

@router.patch("/reservas/{id}/solicitar-cancelamento")
def solicitar_cancelamento(
    id: int,
    dados_token: dict = Depends(usuario_autenticado)
):
    if dados_token["tipo"] != "professor":
        raise HTTPException(
            status_code=403,
            detail="Apenas professores podem solicitar cancelamentos."
        )

    id_professor_logado = int(dados_token["sub"])

    for reserva in reservas:
        if reserva.id == id:

            if reserva.id_professor != id_professor_logado:
                raise HTTPException(
                    status_code=403,
                    detail="Você não pode solicitar o cancelamento de uma reserva de outro professor."
                )

            if reserva.status != "aprovada":
                raise HTTPException(
                    status_code=409,
                    detail="Somente reservas aprovadas podem ter cancelamento solicitado."
                )

            if reserva.status_cancelamento == "pendente":
                raise HTTPException(
                    status_code=409,
                    detail="Já existe uma solicitação de cancelamento pendente."
                )

            reserva.status_cancelamento = "pendente"

            return {
                "mensagem": "Solicitação de cancelamento enviada à secretaria.",
                "reserva": reserva
            }

    raise HTTPException(
        status_code=404,
        detail="Reserva não encontrada."
    )

@router.patch("/reservas/{id}/aprovar-cancelamento")
def aprovar_cancelamento(
    id: int,
    dados_token: dict = Depends(usuario_autenticado)
):
    if dados_token["tipo"] != "secretaria":
        raise HTTPException(
            status_code=403,
            detail="Apenas a secretaria pode aprovar cancelamentos."
        )

    for reserva in reservas:
        if reserva.id == id:

            if reserva.status_cancelamento != "pendente":
                raise HTTPException(
                    status_code=409,
                    detail="Não existe solicitação de cancelamento pendente."
                )

            reserva.status_cancelamento = "aprovado"
            reserva.status = "cancelada"

            historico_reservas.append(reserva)
            reservas.remove(reserva)

            return {
                "mensagem": "Cancelamento aprovado pela secretaria.",
                "reserva": reserva
            }

    raise HTTPException(
        status_code=404,
        detail="Reserva não encontrada."
    )

@router.patch("/reservas/{id}/rejeitar-cancelamento")
def rejeitar_cancelamento(
    id: int,
    dados_token: dict = Depends(usuario_autenticado)
):
    if dados_token["tipo"] != "secretaria":
        raise HTTPException(
            status_code=403,
            detail="Apenas a secretaria pode rejeitar cancelamentos."
        )

    for reserva in reservas:
        if reserva.id == id:

            if reserva.status_cancelamento != "pendente":
                raise HTTPException(
                    status_code=409,
                    detail="Não existe solicitação de cancelamento pendente."
                )

            reserva.status_cancelamento = "rejeitado"

            return {
                "mensagem": "Solicitação de cancelamento rejeitada.",
                "reserva": reserva
            }

    raise HTTPException(
        status_code=404,
        detail="Reserva não encontrada."
    )