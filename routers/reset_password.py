from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import session
from fastapi.responses import JSONResponse

from models.user import Users as UserModel
from service.user import UserService as UserService

reset_pw_router = APIRouter()
# To do: created service
@reset_pw_router.post("/restablecer-pw", tags=['RESET PW'])
async def restablecer_contraseña(request: Request, db: session = Depends(UserService.get_db)):
    email_json = await request.json()
    email = email_json['email']
    # Consulta si el correo existe en la base de datos
    usuario = db.query(UserModel).filter(UserModel.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="No se encontró el correo electrónico en la base de datos")
    # Genera una nueva contraseña y actualiza el registro del usuario
    nueva_contraseña = UserService.generar_contraseña_aleatoria()
    usuario.password = nueva_contraseña
    db.commit()

    # Envía la nueva contraseña por correo electrónico
    UserService.enviar_correo(email_json, nueva_contraseña)

    # Agrega la cabecera CORS en la respuesta
    return JSONResponse(content={"message": "Se ha enviado una nueva contraseña a su correo electrónico."}, headers={"Access-Control-Allow-Origin": "*"})
