from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Country(BaseModel):
    name: str

    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "name": "Introduzca un nuevo pais"
            }
        }