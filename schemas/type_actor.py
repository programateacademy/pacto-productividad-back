from pydantic import BaseModel, Field
from typing import Optional
import datetime

class TypeActor (BaseModel):
    status: int
    type_actor: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "status": 0,
                "type_actor": "aca escribo el tipo de actor social"
            }
        }