from sqlalchemy.orm import Session
from database import Base, engine,SessionLocal
from models.type_actor import TypeActor
from models.city import City
from models.country import Country
from models.departament import Departament
from models.contributions import Contribution

from datetime import datetime

Base.metadata.create_all(bind=engine)

# Create type_actors
def create_type_actors(db_session: Session):
    type_actors = [
        {"type_actor": "Organización de personas con discapacidad", "status": 0},
        {"type_actor": "Empresas", "status": 0},
        {"type_actor": "Entidades de formación", "status": 0},
        {"type_actor": "Entidad de intermediación laboral", "status": 0},
        {"type_actor": "Entidad prestadora de servicios", "status": 0},
        {"type_actor": "Entidad territorial", "status": 0},
        {"type_actor": "Academia", "status": 0},
    ]

    for type_actor in type_actors:
        obj = db_session.query(TypeActor).filter_by(type_actor=type_actor["type_actor"]).first()
        if obj:
            print(f"{obj.type_actor} already exists!")
        else:
            obj = TypeActor(created_at=datetime.now(), updated_at=datetime.now(), **type_actor)
            db_session.add(obj)
            print(f"{obj.type_actor} created!")
    
    db_session.commit()

def create_location():
    session = SessionLocal()

# Verificar si ya existen registros
    countries_count = session.query(Country).count()
    if countries_count > 2:
        print(f"location already exists!")
        return
    
    print(f"creating locations!")

    # Crear países
    colombia = Country(name="Colombia")
    peru = Country(name="Peru")
    ecuador = Country(name="Ecuador")
    session.add_all([colombia, peru, ecuador])
    session.commit()

    # Crear departamentos colombia
    antioquia = Departament(name="Antioquia", id_country=colombia.id)
    atlantico = Departament(name="Atlántico", id_country=colombia.id)
    bogota = Departament(name="Bogotá", id_country=colombia.id)

    session.add_all([antioquia, atlantico, bogota])
    session.commit()
    
    # Crear departamentos peru
    amazonas_peru = Departament(name="Amazonas", id_country=peru.id)
    ancash = Departament(name="Ancash", id_country=peru.id)

    session.add_all([amazonas_peru, ancash])
    session.commit()

    # Crear departamentos ecuador
    azuay = Departament(name="Azuay", id_country=ecuador.id)
    bolivar = Departament(name="Bolivar", id_country=ecuador.id)

    session.add_all([azuay, bolivar])
    session.commit()

    # Crear ciudades en colombia
    medellin = City(name="Medellín", id_department=antioquia.id)
    barranquilla = City(name="Barranquilla", id_department=atlantico.id)
    bogota = City(name="Bogota DC", id_department=bogota.id)

    session.add_all([medellin, barranquilla, bogota])
    session.commit()

    # Crear ciudades en peru
    bagua_grande = City(name="Bagua Grande", id_department=amazonas_peru.id)
    corongo = City(name="Corongo", id_department=ancash.id)

    session.add_all([bagua_grande, corongo])
    session.commit()

    # Crear ciudades en ecuador
    cuenca = City(name="Cuenca", id_department=azuay.id)
    giron = City(name="Giron", id_department=azuay.id)
    caluma = City(name="Caluma", id_department=bolivar.id)

    session.add_all([cuenca,giron,caluma])
    session.commit()


    session.close()

def create_contributions(db_session: Session):
    contributions = ["Conocimiento", "Buenas prácticas", "Casos exitosos", "Ningún aporte"]
    for contribution in contributions:
        obj = db_session.query(Contribution).filter_by(name=contribution).first()
        if obj:
            print(f"{obj.name} already exists!")
        else:
            obj = Contribution(name=contribution)
            db_session.add(obj)
            print(f"{obj.name} created!")
    db_session.commit()