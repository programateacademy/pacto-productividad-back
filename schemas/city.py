from pydantic import BaseModel, Field
from typing import Optional
import datetime

class City(BaseModel):
    name: str
    id_department: int

    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "id_department": 1,
                "name": "ciudad(manizales), -> id_department=1antioquia,2atlantico,3BogotaDc,4Amazonas_peru,5ancash,6azuay,7bolivar,8antofagasta",

            }
        }