from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session

from service.departament import DepartamentService as DepartamentService
from schemas.departament import Departament as DepartamentSchema

# aca me traigo el token
from service.token import user_token as TokenService

departament_router = APIRouter()

@departament_router.get("/api/departament/get",tags=['Departament'])
def get_departament(db: session = Depends(DepartamentService.get_db)):
    result = DepartamentService(db).get_departament()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@departament_router.post("/api/departament/post",tags=['Departament'],status_code=201,response_model=dict)
def create_departament(departament:DepartamentSchema,db: session = Depends(DepartamentService.get_db)):
    result=DepartamentService(db).create_departament(departament)
    return JSONResponse(content={"message":'Se ha creado el departament correctamente'})

@departament_router.delete('/api/departament/delete/{id}',tags=['Departament'])
def delete_departament(id:int, db: session = Depends(DepartamentService.get_db),current_user: DepartamentSchema = Depends(TokenService.get_current_active_user)):
    success = DepartamentService(db).delete_departament(id)
    if success:
        return JSONResponse(status_code=202,content={"message":"departament deleted"})
    else:
        return JSONResponse(content="departament not found", status_code=404)


@departament_router.put('/api/departament/put/{id}',tags=['Departament'])
def update_departament(id:int,departament:DepartamentSchema, db: session = Depends(DepartamentService.get_db),current_user: DepartamentSchema = Depends(TokenService.get_current_active_user)):
    result = DepartamentService(db).update_departament(id,departament)
    if not result:
        return JSONResponse(content={"message":"No se ha encontrado ningun departament","status_code":"404"})
    DepartamentService(db).update_departament(id,departament)
    return JSONResponse(content={"message":'Se ha modificado el departament'})
