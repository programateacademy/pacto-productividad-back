from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session, Session

from service.contribution_text import contributiontextService as ContributiontextService
from schemas.contribution_text import ContributionText as ContributiontextSchema

# aca me traigo el token
from service.token import user_token as TokenService

contributiontext_router = APIRouter()

@contributiontext_router.get("/api/contributiontext/get",tags=['contribution'])
def get_contributiontext(db: session = Depends(ContributiontextService.get_db)):
    result = ContributiontextService(db).get_contributiontext()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@contributiontext_router.post("/api/contributiontext/post",tags=['contribution'],status_code=201,response_model=dict)
def create_contributiontext(contributiontext:ContributiontextSchema,db: session = Depends(ContributiontextService.get_db)):
    result=ContributiontextService(db).create_contributiontext(contributiontext)
    return JSONResponse(content={"message":'Se ha creado el contributiontext correctamente'})

@contributiontext_router.delete('/api/contributiontext/delete/{id}',tags=['contribution'])
def delete_contributiontext(id:int, db: session = Depends(ContributiontextService.get_db),current_user: ContributiontextSchema = Depends(TokenService.get_current_active_user)):
    success = ContributiontextService(db).delete_contributiontext(id)
    if success:
        return JSONResponse(status_code=202,content={"message":"contributiontext deleted"})
    else:
        return JSONResponse(content="contributiontext not found", status_code=404)


@contributiontext_router.put('/api/contributiontext/put/{id}',tags=['contribution'])
def update_contributiontext(id:int,contributiontext:ContributiontextSchema, db: session = Depends(ContributiontextService.get_db),current_user: ContributiontextSchema = Depends(TokenService.get_current_active_user)):
    result = ContributiontextService(db).update_contributiontext(id,contributiontext)
    if not result:
        return JSONResponse(content={"message":"No se ha encontrado ningun contributiontext","status_code":"404"})
    ContributiontextService(db).update_contributiontext(id,contributiontext)
    return JSONResponse(content={"message":'Se ha modificado el contributiontext'})
