from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Departament(BaseModel):
    name: str
    id_country: int

    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "name": "ciudad(BogotaDC), -> id_country=1colombia,2peru,3ecuador",
                "id_country": 1
            }
        }