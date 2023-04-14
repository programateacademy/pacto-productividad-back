from fastapi import  HTTPException, Depends,  APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta


import service.token as Token_service
from service.user import UserService as UserService
from schemas.user import User as UserSchema
from service.token import user_token as TokenService

# Create a new API router instance
token_router = APIRouter()

# Route for user authentication and token creation
@token_router.post("/token/",tags=['token'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(UserService.get_db)):
    # Authenticate user using the credentials provided
    user = TokenService.authenticate_user(db, form_data.username, form_data.password)
    # If the user is not authenticated, raise an HTTP exception
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    # If the user is authenticated, create a new access token for the user
    access_token_expires = timedelta(minutes=Token_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenService.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    # Return the access token with token type
    return{"access_token": access_token, "token_type": "bearer"}

# Route for getting the current user
@token_router.get("/api/users/me",tags=['token'])
async def read_users_me(current_user: UserSchema = Depends(TokenService.get_current_active_user)):
    # Return the current user
    return current_user

# Route for getting items belonging to the current user
@token_router.get("/api/users/me/items/",tags=['token'])
async def read_users_me_items(current_user: UserSchema = Depends(TokenService.get_current_active_user)):
    # Route for getting items belonging to the current user
    return [{"item_id": "Foo", "owner": current_user.username}]
