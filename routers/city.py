from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session, Session

from service.city import CityService as CityService
from schemas.city import City as CitySchema

# aca me traigo el token
from service.token import user_token as TokenService

city_router = APIRouter()

@city_router.get("/api/city/get",tags=['city'])
def get_city(db: session = Depends(CityService.get_db)):
    result = CityService(db).get_city()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@city_router.post("/api/city/post",tags=['city'],status_code=201,response_model=dict)
def create_city(city:CitySchema,db: session = Depends(CityService.get_db)):
    result=CityService(db).create_city(city)
    return JSONResponse(content={"message":'Se ha creado el city correctamente'})

@city_router.delete('/api/city/delete/{id}',tags=['city'])
def delete_city(id:int, db: session = Depends(CityService.get_db),current_user: CitySchema = Depends(TokenService.get_current_active_user)):
    success = CityService(db).delete_city(id)
    if success:
        return JSONResponse(status_code=202,content={"message":"city deleted"})
    else:
        return JSONResponse(content="city not found", status_code=404)


@city_router.put('/api/city/put/{id}',tags=['city'])
def update_city(id:int,city:CitySchema, db: session = Depends(CityService.get_db),current_user: CitySchema = Depends(TokenService.get_current_active_user)):
    result = CityService(db).update_city(id,city)
    if not result:
        return JSONResponse(content={"message":"No se ha encontrado ningun city","status_code":"404"})
    CityService(db).update_city(id,city)
    return JSONResponse(content={"message":'Se ha modificado el city'})
