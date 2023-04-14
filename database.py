from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy.ext.declarative import declarative_base

# set the URL for the SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# create an engine instance with the database URL and disable thread checking
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# create a session factory to manage sessions with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# configure mappers to avoid any runtime overhead in queries
configure_mappers()

# create a base class for declarative class definitions (for models)
Base = declarative_base()
            

            