from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import session

from service.locations import LocationService as LocationService

# aca me traigo el token

locations_router = APIRouter()

@locations_router.get("/api/countries/", tags=['location'])
def read_countries(country_id: int = None, db: session = Depends(LocationService.get_db)):
    countries = LocationService(db).get_countries(country_id)
    return JSONResponse(content=jsonable_encoder(countries), status_code=200)

@locations_router.get("/api/countries/{country_id}/departments/", tags=['location'])
def read_departments(country_id: int, db: session = Depends(LocationService.get_db)):
    departments = LocationService(db).get_departments_by_country(country_id=country_id)
    return departments

@locations_router.get("/api/departments/{department_id}/cities/", tags=['location'])
def read_cities(department_id: int, db: session = Depends(LocationService.get_db)):
    cities = LocationService(db).get_cities_by_department(department_id=department_id)
    return cities
