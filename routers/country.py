from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session, Session

from service.country import CountryService as CountryService
from schemas.country import Country as CountrySchema

# aca me traigo el token
from service.token import user_token as TokenService

country_router = APIRouter()

@country_router.get("/api/country/get",tags=['country'])
def get_country(db: session = Depends(CountryService.get_db)):
    result = CountryService(db).get_country()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@country_router.post("/api/country/post",tags=['country'],status_code=201,response_model=dict)
def create_country(country:CountrySchema,db: session = Depends(CountryService.get_db)):
    result=CountryService(db).create_country(country)
    return JSONResponse(content={"message":'Se ha creado el country correctamente'})

@country_router.delete('/api/country/delete/{id}',tags=['country'])
def delete_country(id:int, db: session = Depends(CountryService.get_db),current_user: CountrySchema = Depends(TokenService.get_current_active_user)):
    success = CountryService(db).delete_country(id)
    if success:
        return JSONResponse(status_code=202,content={"message":"country deleted"})
    else:
        return JSONResponse(content="country not found", status_code=404)


@country_router.put('/api/country/put/{id}',tags=['country'])
def update_country(id:int,country:CountrySchema, db: session = Depends(CountryService.get_db),current_user: CountrySchema = Depends(TokenService.get_current_active_user)):
    result = CountryService(db).update_country(id,country)
    if not result:
        return JSONResponse(content={"message":"No se ha encontrado ningun country","status_code":"404"})
    CountryService(db).update_country(id,country)
    return JSONResponse(content={"message":'Se ha modificado el country'})
