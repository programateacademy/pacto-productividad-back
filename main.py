from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import time

# Import the database engine, session, and base
from database import engine, Base, SessionLocal

# Import the routers
from routers.user import user_router
from routers.token import token_router
from routers.post import post_router
from routers.comments import comment_router
from routers.type_actor import type_actor_router
from routers.city import city_router
from routers.country import country_router
from routers.departament import departament_router
from routers.contribution import contribution_router
from routers.contribution_text import contributiontext_router
from routers.locations import locations_router
from routers.reset_password import reset_pw_router

from models.user import Users as UserModel
from service.user import UserService as UserService
# Import database auto-creation functions
from auto_db import create_type_actors, create_location, create_contributions

# Import middleware and CORS
# El middleware CORS permite a los navegadores web restringir las solicitudes HTTP realizadas por scripts del lado del cliente 
# en un dominio diferente al del servidor. Esto significa que el middleware CORS ayuda a mejorar la seguridad de la aplicación 
# web al restringir el acceso a los recursos del servidor solo a los sitios web autorizados.

# Sin el middleware CORS, un sitio web malintencionado podría hacer solicitudes HTTP a un servidor sin la aprobación explícita 
# del servidor, lo que podría provocar ataques de seguridad. Por lo tanto, es importante tener middleware CORS configurado 
# correctamente para garantizar que solo se permitan solicitudes HTTP de los sitios web autorizados y evitar posibles vulnerabilidades 
# de seguridad en la aplicación web.
from middleware.middleware import middleware_router
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app
app = FastAPI()
app.title = "PACTO con FastAPI"
app.version = "0.0.1"


# Configurar el middleware CORS
origins = [
    "http://localhost:3000",  
    # Add here the origin of your React application
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers in the app
app.include_router(user_router)
app.include_router(post_router)
app.include_router(token_router)
app.include_router(comment_router)
app.include_router(type_actor_router)
app.include_router(city_router)
app.include_router(country_router)
app.include_router(departament_router)
app.include_router(contribution_router)
app.include_router(contributiontext_router)
app.include_router(locations_router)
app.include_router(reset_pw_router)


# Include the middleware in the app
app.include_router(middleware_router)

# Create the database tables when the app starts
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    # Create the tables in the database    
    Base.metadata.create_all(bind=engine)

    # Create the default type actors, locations and contributions    
    with SessionLocal() as session:
        create_type_actors(session)
        create_location()
        create_contributions(session)
        
# Add middleware to add processing time to the request header
@app.middleware("http")
async def add_process_time_header(request:Request, call_next):
# add time for process 
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"]= str(process_time)
    return response

# Create a home page route
@app.get('/',tags=['home'])
def message():
    return HTMLResponse('<h1>This is from the backend. If you can read this in React, it\'s connected!</h1>')


