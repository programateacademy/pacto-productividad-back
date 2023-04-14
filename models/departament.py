from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY
from database import Base
from sqlalchemy.orm import relationship


class Departament(Base):
    __tablename__ = "departament"

    id = Column(Integer, primary_key=True, index=True)
    id_country = Column(Integer, ForeignKey("country.id"))
    name = Column(String)
    
    cities = relationship("City", back_populates="department")

    country = relationship("Country", back_populates="departments")