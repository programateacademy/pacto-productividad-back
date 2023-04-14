from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal

from models.city import City as CityModel
from models.departament import Departament as DepartamentModel
from models.country import Country as CountryModel


class LocationService():
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


# Función para obtener todos los países por id
    def get_countries(self, country_by_id: int):
        result = self.db.query(CountryModel).filter(CountryModel.id == country_by_id).first()
        if result is None:
            all_countries = self.db.query(CountryModel).all()
            country_ids = [str(country.id) for country in all_countries]
            message = f"No se encontró ningún país con el ID {country_by_id}. Los ID de los países disponibles son: {', '.join(country_ids)}"
            raise HTTPException(status_code=404, detail=message)
        return result
    
# Función para obtener los departamentos de un país específico
    def get_departments_by_country(self, country_id: int):
        result = self.db.query(DepartamentModel).filter(DepartamentModel.id_country == country_id).order_by(DepartamentModel.name).all()
        if not result:
            all_departments = self.db.query(DepartamentModel).all()
            department_names = [department.name for department in all_departments]
            message = f"No se encontraron departamentos para el país con ID {country_id}. Los departamentos disponibles son: {department_names}"
            raise HTTPException(status_code=404, detail=message)
        return result

# Función para obtener las ciudades de un departamento específico
    def get_cities_by_department(self, department_id: int):
        result = self.db.query(CityModel).filter(CityModel.id_department == department_id).order_by(CityModel.name).all()
        if not result:
            all_cities = self.db.query(CityModel).all()
            city_names = [city.name for city in all_cities]
            message = f"No se encontraron ciudades para el departamento con ID {department_id}. Las ciudades disponibles son: {city_names}"
            raise HTTPException(status_code=404, detail=message)
        return result
