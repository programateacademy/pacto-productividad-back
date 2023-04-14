from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.country import Country as CountryModel
from schemas.country import Country as countrySchema

class CountryService():
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

    def get_country(self):
        result = self.db.query(CountryModel).all()
        return result
    
    def create_country(self, country:CountryModel):
        country_model = CountryModel(
        name = country.name
        )
        self.db.add(country_model)
        self.db.commit()
        return
    
    def get_country_by_id(self,id:int):
        result = self.db.query(CountryModel).filter(CountryModel.id == id).first()
        return result
    
    def delete_country(self,id:int):
        country = self.get_country_by_id(id)
        if not country:
            return None
        self.db.delete(country)
        self.db.commit()
        return country

    
    def update_country(self,id:int, country_schema:countrySchema):
        country= self.db.query(CountryModel).get(id)
        if country:
            country.name = country_schema.name
            self.db.commit()
            return True
        return False
    
