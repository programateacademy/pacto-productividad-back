from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Comment (BaseModel):
    id_post: Optional[int] = None
    status: int
    description: str
    likes: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "status": 0,
                "description": "este es el texto de mi comentario",
                "likes": 0
            }
        }