from sqlalchemy import Column, Integer, String,ForeignKey,ARRAY
from database import Base
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    departments = relationship("Departament", back_populates="country")