from pydantic import BaseModel, Field
from typing import Optional
import datetime

class User(BaseModel):
    id_type_actor: Optional[int]=None
    name_user: Optional[str] = None
    id_city: Optional[int]=None
    id_contribution: Optional[int]=None
    lastname: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    cohabitation_agreement: Optional[bool] = None
    type_user: Optional[int]=None
    name_enti:Optional[str] = None
    contribution_text: Optional[str] = None
    hashed_password: Optional[str] = None
    status: Optional[int] = 1
    description: Optional[str] = None
    knowledge_interests: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    forgot_password: Optional[bool] = False
    image_profile: Optional[str] = None
    phone_number: Optional[str] = None
    class Config:
        # Allows using ORM mode to read from the database
        orm_mode=True
        # Defines an example schema for the User model
        schema_extra = {
            "example": {
                "name_user": "edwin",
                "lastname": "hernandez",
                "email": "edwin.jhnsn@gmail.com",
                "username": "edwinjhs",
                "password": "12345678",
                "entidad": "colegio monseñor",
                "hashed_password": "",
                "cohabitation_agreement": True,
                "type_user": 0,
                "name_enti":"ledcorp",
                "contribution_text":"mis contribuciones han sido ....",
                "status": 0,
                "description": "backend iasdas",
                "knowledge_interests": "conocimiento, etc",
                "forgot_password": False,
                "image_profile": "../image/profile1.jpg",
                "phone_number": "3213943876"
            }
        }
class Token(BaseModel):
    # JWT access token
    access_token: str
    # Type of token (usually "bearer")
    token_type: str

class TokenData(BaseModel):
    # Username associated with the token
    username:str
