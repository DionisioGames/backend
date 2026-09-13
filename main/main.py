# para rodar o codigo, executar no terminal: uvicorn main.main:app --reload
# para desabilitar o servidor coloque no terminal e digite o comando  (ctrl + c)

from fastapi import FastAPI

from routes.auth.auth_routes import router as auth_router
from main.sala_routes import router as sala_router
from main.reserva_routes import router as reserva_router
from main.usuario_routes import router as usuario_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(sala_router)
app.include_router(reserva_router)
app.include_router(usuario_router)