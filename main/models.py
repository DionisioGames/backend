from pydantic import BaseModel, EmailStr
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
    id_professor: int | None = None
    data: date
    hora_inicio: time
    hora_fim: time
    status: str = "pendente"
    status_cancelamento: str = "nenhum"

class ReservaCreate(BaseModel):
    id: int
    id_sala: int
    data: date
    hora_inicio: time
    hora_fim: time
    id_professor: int | None = None

class Usuario(BaseModel):
    id: int
    nome: str
    email: EmailStr
    senha: str
    telefone: str
    tipo: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str
    tipo: str

class Login(BaseModel):
    email: EmailStr
    senha: str