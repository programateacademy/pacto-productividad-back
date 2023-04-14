from pydantic import BaseModel

class Contribution(BaseModel):
    name: str

    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "name": "nombre de contribucion",
            }
        }