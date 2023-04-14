from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session, Session

from service.comment import CommentService as CommentService
from schemas.comment import Comment as CommentSchema

# aca me traigo el token
from service.token import user_token as TokenService

comment_router = APIRouter()

@comment_router.get("/api/comment",tags=['comment'])
def read_api(db: session = Depends(CommentService.get_db)):
    result = CommentService(db).get_comments()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@comment_router.post("/api/comment/new",tags=['comment'],status_code=201,response_model=dict)
def create_comment(comment:CommentSchema,db: session = Depends(CommentService.get_db),current_user: CommentSchema = Depends(TokenService.get_current_active_user)):
    result=CommentService(db).create_comment(comment)
    return JSONResponse(content={"message":'Se ha creado el comment correctamente'})

@comment_router.delete('/api/comment/delete/{id}',tags=['comment'])
def delete_comment(id:int, db: session = Depends(CommentService.get_db),current_user: CommentSchema = Depends(TokenService.get_current_active_user)):
    success = CommentService(db).delete_comment(id)
    if success:
        return JSONResponse(status_code=202,content={"message":"comment deleted"})
    else:
        return JSONResponse(content="Comment not found", status_code=404)

@comment_router.get("/api/comment/getstatus/{status}",tags=['comment'])
def get_comment_by_status(status, db: Session = Depends(CommentService.get_db),current_user: CommentSchema = Depends(TokenService.get_current_active_user)):
    comment = CommentService(db).get_comment_by_status(status)
    return comment

@comment_router.put('/api/comment/put/{id}',tags=['comment'])
def update_comment(id:int,comment:CommentSchema, db: session = Depends(CommentService.get_db),current_user: CommentSchema = Depends(TokenService.get_current_active_user)):
    result = CommentService(db).update_comment(id,comment)
    if not result:
        return JSONResponse(content={"message":"No se ha encontrado ningun comentario","status_code":"404"})
    CommentService(db).update_comment(id,comment)
    return JSONResponse(content={"message":'Se ha modificado el comentario'})
