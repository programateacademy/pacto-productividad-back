from fastapi import HTTPException, Depends, status, FastAPI
from sqlalchemy.orm import session
from datetime import datetime, timedelta
import os

# HASHING AND JWT 
from jose import JWTError, jwt

import schemas.user as UserSchema

from service.user import UserService as UserService
from models.user import Users as UserModel


SECRET_KEY ="jwtsecretkey"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =15



class UserInDB(UserSchema.User):
    hashed_password: str

class user_token():
    @staticmethod   
    def get_user(db, username):
        user_model = db.query(UserModel).filter(UserModel.username == username).first()
        if user_model is not None:
            return user_model
    @staticmethod
    def decode_token( db, token):
        user = user_token.get_user(db, token)
        return user

    async def get_current_user(token = Depends(UserService.oauth2_scheme),  db: session = Depends(UserService.get_db)):
        # es el que extrae la info para loguearme
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
        try:
            payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            username=payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = UserSchema.TokenData(username=username)
        except JWTError:
        # Manejar la excepción aquí
            raise credentials_exception
        user = user_token.get_user(db,username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
    async def get_current_active_userid(db: session = Depends(UserService.get_db)):
        current_user= user_token.get_current_user()
        user_model = db.query(UserModel).filter(UserModel.username == current_user.username).first()
        return user_model.id
    
    async def get_current_active_user(current_user: UserSchema.User = Depends(get_current_user)):
        # una funcion que obtiene un usuario actual activo a partir del token
        if current_user.status == 10:
            raise HTTPException(status_code=400, detail="Inactive user")
        elif current_user.status == 5:
            raise HTTPException(status_code=400, detail="Usuario no validado por el Admin")
        return current_user
    
    # HASHED AND JWT
    def verify_password (plain_password: str, hashed_password: str)->bool:
        return UserService.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(password: str):
        return UserService.pwd_context.verify(password)
    
    def authenticate_user(db, username, password):
        user = user_token.get_user(db,username)
        if not user:
            return False
        if not user_token.verify_password(password, user.password):
            return False
        return user
    
    
    # CREA UN TOKEN DE ACCESO
    def create_access_token(data:dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp":expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt