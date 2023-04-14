from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session, Session

from service.contribution import ContributionService as ContributionService
from schemas.contribution import Contribution as ContributionSchema

# aca me traigo el token
from service.token import user_token as TokenService

contribution_router = APIRouter()

@contribution_router.get("/api/contribution/get",tags=['contribution'])
def get_contribution(db: session = Depends(ContributionService.get_db)):
    result = ContributionService(db).get_contribution()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@contribution_router.post("/api/contribution/post",tags=['contribution'],status_code=201,response_model=dict)
def create_contribution(contribution:ContributionSchema,db: session = Depends(ContributionService.get_db)):
    result=ContributionService(db).create_contribution(contribution)
    return JSONResponse(content={"message":'Se ha creado el contribution correctamente'})

@contribution_router.delete('/api/contribution/delete/{id}',tags=['contribution'])
def delete_contribution(id:int, db: session = Depends(ContributionService.get_db),current_user: ContributionSchema = Depends(TokenService.get_current_active_user)):
    success = ContributionService(db).delete_contribution(id)
    if success:
        return JSONResponse(status_code=202,content={"message":"contribution deleted"})
    else:
        return JSONResponse(content="contribution not found", status_code=404)


@contribution_router.put('/api/contribution/put/{id}',tags=['contribution'])
def update_contribution(id:int,contribution:ContributionSchema, db: session = Depends(ContributionService.get_db),current_user: ContributionSchema = Depends(TokenService.get_current_active_user)):
    result = ContributionService(db).update_contribution(id,contribution)
    if not result:
        return JSONResponse(content={"message":"No se ha encontrado ningun contribution","status_code":"404"})
    ContributionService(db).update_contribution(id,contribution)
    return JSONResponse(content={"message":'Se ha modificado el contribution'})
