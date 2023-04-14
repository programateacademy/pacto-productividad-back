from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session, Session

from service.type_actor import TypeActorService as TAService
from schemas.type_actor import TypeActor as TASchema

# aca me traigo el token
from service.token import user_token as TokenService

type_actor_router = APIRouter()

@type_actor_router.get("/api/typeactor/get",tags=['TypeActor'])
def read_api(db: session = Depends(TAService.get_db)):
    result = TAService(db).get_typeactor()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@type_actor_router.post("/api/typeactor/post",tags=['TypeActor'],status_code=201,response_model=dict)
def create_typeactor(typeactor:TASchema,db: session = Depends(TAService.get_db)):
    result=TAService(db).create_typeactor(typeactor)
    return JSONResponse(content={"message":'Se ha creado el typeactor correctamente'})

@type_actor_router.delete('/api/typeactor/delete/{id}',tags=['TypeActor'])
def delete_typeactor(id:int, db: session = Depends(TAService.get_db),current_user: TASchema = Depends(TokenService.get_current_active_user)):
    success = TAService(db).delete_typeactor(id)
    if success:
        return JSONResponse(status_code=202,content={"message":"typeactor deleted"})
    else:
        return JSONResponse(content="typeactor not found", status_code=404)


@type_actor_router.put('/api/typeactor/put/{id}',tags=['TypeActor'])
def update_typeactor(id:int,typeactor:TASchema, db: session = Depends(TAService.get_db),current_user: TASchema = Depends(TokenService.get_current_active_user)):
    result = TAService(db).update_typeactor(id,typeactor)
    if not result:
        return JSONResponse(content={"message":"No se ha encontrado ningun typeactor","status_code":"404"})
    TAService(db).update_typeactor(id,typeactor)
    return JSONResponse(content={"message":'Se ha modificado el typeactor'})
