from pydantic import BaseModel
from datetime import date, time

class Sala(BaseModel):
    id : int
    nome: str
    bloco: str
    tipo: str
    andar: int
    capacidade: int
    disponivel: bool = True

class Reserva(BaseModel):
    id: int
    id_sala: int
    id_professor: int
    data: date
    hora_inicio: time
    hora_fim: time
    status: str = "pendente"