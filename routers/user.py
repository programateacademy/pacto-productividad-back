from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session, Session
from PIL import Image
import os
import shutil


from models.user import Users as UserModel
from service.user import UserService as UserService
from schemas.user import User as UserSchema
from service.token import user_token as TokenService

# Creating an instance of the APIRouter class
user_router = APIRouter()

# Defining a GET route for getting all users
@user_router.get("/api/user/get", tags=['user'])
def read_api(db: Session = Depends(UserService.get_db)):
    try:
        # Calling the get_users() method from the UserService class to retrieve all users
        result = UserService(db).get_users()
        # Returning a JSON response with the retrieved users
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    except:
        # If something goes wrong, return a JSON response with an error message and a 500 status code
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)

# Defining a POST route for creating a new user
# ,current_user: PostSchema = Depends(TokenService.get_current_active_user)
@user_router.post("/api/user/post", tags=['user'], status_code=201, response_model=dict)
def create_user(user: UserSchema, db: Session = Depends(UserService.get_db)):
    try:
        # Calling the create_user() method from the UserService class to create a new user
        UserService(db).create_user(user)
        # Returning a JSON response with a message indicating that the user has been created
        return JSONResponse(content={"message": 'Se ha creado el usuario correctamente'})
    except:
        # If something goes wrong, return a JSON response with an error message and a 500 status code
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)

# Defining a DELETE route for deleting a user by id
@user_router.delete('/api/user/delete/{id}', tags=['user'])
def delete_user(id: int, db: Session = Depends(UserService.get_db),current_user: UserSchema = Depends(TokenService.get_current_active_user)):
    try:
        success = UserService(db).delete_user(id)
        if success:
            return JSONResponse(status_code=202, content={"message": "User deleted"})
        else:
            # If the user was not found, return a JSON response with a 404 status code
            return JSONResponse(content="User not found", status_code=404)
    except:
        # If something goes wrong, return a JSON response with an error message and a 500 status code
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)

# Defining a GET route for getting a user by their username
@user_router.get("/api/user/get/{username}", tags=['user'])
def get_user_by_username(username, db: Session = Depends(UserService.get_db)):
    try:
        user = UserService(db).get_user_by_username(username)
        if user:
            return user
        else:
            # If the user was not found, return a JSON response with a 404 status code
            return JSONResponse(content="User not found", status_code=404)
    except:
        # If something goes wrong, return a JSON response with an error message and a 500 status code
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)

# Defining a PUT route for updating a user by id
@user_router.put('/api/user/put/{id}', tags=['user'])
def update_user(id: int, user: UserSchema, db: Session = Depends(UserService.get_db)):
    result = UserService(db).update_user(id, user)
    if not result:
        return JSONResponse(content={"message": f"No se ha encontrado ningun usuario con id {id}"}, status_code=404)
    UserService(db).update_user(id, user)
    return JSONResponse(content={"message": f"Se ha modificado el usuario con id: {id}"}, status_code=200)

# subiendo imagenes

@user_router.post("/uploadfile/", tags=['user profile'])
async def create_upload_file(image: UploadFile = File(...)):
    print(image)
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"message": "Image uploaded successfully!"}


@user_router.get("/image_path/")
async def get_image_path():
    return {"image_path": os.path.abspath("image.jpg")}


@user_router.get("/api/user/getimageprofile/{username}", tags=['user'])
def read_api(username, db: Session = Depends(UserService.get_db)):
        user = UserService(db).get_user_by_username(username)
        return user.image_profile

