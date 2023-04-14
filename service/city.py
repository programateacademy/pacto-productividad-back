from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.city import City as CityModel
from schemas.city import City as CitySchema

class CityService():
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

    def get_city(self):
        result = self.db.query(CityModel).all()
        return result
    
    def create_city(self, city:CityModel):
        # current_user = ServiceToken.get_current_active_userid()
        city_model = CityModel(
        id_department= city.id_department,
        name = city.name
        )
        self.db.add(city_model)
        self.db.commit()
        return
    
    def get_city_by_id(self,id:int):
        result = self.db.query(CityModel).filter(CityModel.id == id).first()
        return result
    
    def delete_city(self,id:int):
        city = self.get_city_by_id(id)
        if not city:
            return None
        self.db.delete(city)
        self.db.commit()
        return city

    
    def update_city(self,id:int, city_schema:CitySchema):
        city= self.db.query(CityModel).get(id)
        if city:
            city.id_department = city_schema.id_department
            city.name = city_schema.name
            self.db.commit()
            return True
        return False
    
