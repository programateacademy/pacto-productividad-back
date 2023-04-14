from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.type_actor import TypeActor as TAModel
from schemas.type_actor import TypeActor as TASchema

class TypeActorService():
    def __init__(self, db: Session):
        if not isinstance(db, Session):
            raise TypeError("db must be a Session instance")
        self.db = db

    @staticmethod
    def get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()

    def get_typeactor(self):
        result = self.db.query(TAModel).all()
        return result
    
    def create_typeactor(self, typeactor:TAModel):
        # current_user = ServiceToken.get_current_active_userid()
        typeactor_model = TAModel(
        status = typeactor.status,
        type_actor = typeactor.type_actor,
        created_at = typeactor.created_at,
        updated_at = typeactor.updated_at,
        )
        self.db.add(typeactor_model)
        self.db.commit()
        return
    
    def get_typeactor_by_id(self,id:int):
        result = self.db.query(TAModel).filter(TAModel.id == id).first()
        return result
    
    def delete_typeactor(self,id:int):
        typeactor = self.get_typeactor_by_id(id)
        if not typeactor:
            return None
        self.db.delete(typeactor)
        self.db.commit()
        return typeactor

    
    def update_typeactor(self,id:int, typeactor_schema:TASchema):
        typeactor= self.db.query(TAModel).get(id)
        if typeactor:
            typeactor.status = typeactor_schema.status
            typeactor.type_actor = typeactor_schema.type_actor
            typeactor.created_at = typeactor_schema.created_at
            typeactor.updated_at = typeactor_schema.updated_at
            self.db.commit()
            return True
        return False
    
