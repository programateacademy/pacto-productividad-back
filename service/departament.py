from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.departament import Departament as DepartamentModel
from schemas.departament import Departament as DepartamentSchema

class DepartamentService():
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

    def get_departament(self):
        result = self.db.query(DepartamentModel).all()
        return result
    
    def create_departament(self, departament:DepartamentModel):
        # current_user = ServiceToken.get_current_active_userid()
        departament_model = DepartamentModel(
        id_country= departament.id_country,
        name = departament.name
        )
        self.db.add(departament_model)
        self.db.commit()
        return
    
    def get_departament_by_id(self,id:int):
        result = self.db.query(DepartamentModel).filter(DepartamentModel.id == id).first()
        return result
    
    def delete_departament(self,id:int):
        departament = self.get_departament_by_id(id)
        if not departament:
            return None
        self.db.delete(departament)
        self.db.commit()
        return departament

    
    def update_departament(self,id:int, departament_schema:DepartamentSchema):
        departament= self.db.query(DepartamentModel).get(id)
        if departament:
            departament.id_country = departament_schema.id_country
            departament.name = departament_schema.name
            self.db.commit()
            return True
        return False
    
