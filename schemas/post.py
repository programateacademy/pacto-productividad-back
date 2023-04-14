from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Post (BaseModel):
    id_user: Optional[int] = None
    status: int
    description: str
    likes: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    image_post: str
    document_post: str
    video_post: str
    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "status": 0,
                "description": "este es el texto de mi post",
                "image_post": "../image/profile1.jpg",
                "document_post": "link de documento",
                "video_post": "link de video"
            }
        }