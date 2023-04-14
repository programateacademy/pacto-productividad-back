from fastapi import FastAPI, APIRouter, Request, Response
from random import randint
import time

middleware_router = APIRouter()

# @middleware_router.middleware("http")
# async def add_process_time_header(request:Request, call_next):
#     # esto añade tiempo de procesamiento de la peticion
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"]= str(process_time)
#     return response

@middleware_router.get("/updating-date")
# simula la carga de datos, 
async def updating_date():
    time.sleep(randint(2,6))
    datos={"datos":"cargados"}
    return datos